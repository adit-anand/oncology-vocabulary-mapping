import logging
import os
import shutil
from pathlib import Path

import spacy
from spacy.tokens import Doc, DocBin, Span

REPO_ROOT = Path(__file__).resolve().parents[2]
ANNOTATIONS_DIR = REPO_ROOT / "data" / "annotations" / "chia-files"
TRAIN_DIR = REPO_ROOT / "data" / "annotations" / "train"
TEST_DIR = REPO_ROOT / "data" / "annotations" / "test"
TRAIN_SPACY_DIR = REPO_ROOT / "data" / "annotations" / "train_spacy"
TEST_SPACY_DIR = REPO_ROOT / "data" / "annotations" / "test_spacy"
ANNOTATION_CONF = REPO_ROOT / "data" / "annotations" / "annotation.conf"

logger = logging.getLogger(__name__)


def load_ner_labels(conf_path: Path) -> set[str]:
    """Parse the `!CONCEPTS` entity labels out of a brat annotation.conf file."""
    labels: set[str] = set()
    in_concepts = False
    with open(conf_path, encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip("\n")
            if not stripped:
                continue
            if stripped.startswith("!"):
                in_concepts = stripped == "!CONCEPTS"
                continue
            if stripped.startswith("["):
                in_concepts = False
                continue
            if in_concepts:
                labels.add(stripped.strip())
    return labels


def parse_ann_file(ann_path: Path) -> list[tuple[list[tuple[int, int]], str, str]]:
    """Parse brat `T` (entity) lines into (fragments, label, entity_id) tuples."""
    entities: list[tuple[list[tuple[int, int]], str, str]] = []
    with open(ann_path, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("T"):
                continue
            entity_id, label_and_offsets, *_ = line.rstrip("\n").split("\t")
            label, offset_str = label_and_offsets.split(" ", 1)
            fragments = []
            for fragment in offset_str.split(";"):
                start_str, end_str = fragment.split(" ")
                fragments.append((int(start_str), int(end_str)))
            entities.append((fragments, label, entity_id))
    return entities


def build_doc(
    nlp,
    text: str,
    ann_entities: list[tuple[list[tuple[int, int]], str, str]],
    keep_labels: set[str],
    source_name: str,
) -> Doc:
    """Build a Doc with every aligned brat fragment as a Span in doc.spans["sc"]."""
    doc = nlp.make_doc(text)
    spans: list[Span] = []
    for fragments, label, entity_id in ann_entities:
        if label not in keep_labels:
            logger.info(
                "%s: excluding entity %s (label %r not in !CONCEPTS)",
                source_name,
                entity_id,
                label,
            )
            continue
        for start, end in fragments:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                logger.warning(
                    "%s: dropping fragment of entity %s at [%d, %d) (%r) "
                    "- token boundary misalignment",
                    source_name,
                    entity_id,
                    start,
                    end,
                    text[start:end],
                )
                continue
            span._.ann_id = entity_id
            spans.append(span)
    doc.spans["sc"] = spans
    return doc


def convert_split(txt_ann_dir: Path, out_dir: Path, nlp, keep_labels: set[str]) -> None:
    """Convert every .txt/.ann pair in txt_ann_dir into a .spacy file in out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)

    files_processed = 0
    entities_kept = 0
    entities_excluded = 0
    fragments_kept = 0
    fragments_dropped = 0

    for txt_path in sorted(txt_ann_dir.glob("*.txt")):
        stem = txt_path.stem
        ann_path = txt_ann_dir / f"{stem}.ann"
        if not ann_path.exists():
            logger.warning("%s: missing .ann file, skipping", txt_path.name)
            continue

        with open(txt_path, encoding="utf-8", newline="") as f:
            text = f.read()

        ann_entities = parse_ann_file(ann_path)
        doc = build_doc(nlp, text, ann_entities, keep_labels, txt_path.name)

        doc_bin = DocBin(store_user_data=True)
        doc_bin.add(doc)
        doc_bin.to_disk(out_dir / f"{stem}.spacy")
        files_processed += 1

        kept_fragments_requested = sum(
            len(fragments) for fragments, label, _ in ann_entities if label in keep_labels
        )
        entities_kept += sum(1 for _, label, _ in ann_entities if label in keep_labels)
        entities_excluded += sum(1 for _, label, _ in ann_entities if label not in keep_labels)
        fragments_kept += len(doc.spans["sc"])
        fragments_dropped += kept_fragments_requested - len(doc.spans["sc"])

    logger.info(
        "%s: processed %d files, entities kept=%d excluded=%d, fragments kept=%d dropped=%d",
        out_dir.name,
        files_processed,
        entities_kept,
        entities_excluded,
        fragments_kept,
        fragments_dropped,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    if not Span.has_extension("ann_id"):
        Span.set_extension("ann_id", default=None)

    # Remove and recreate any existing train/test directories
    shutil.rmtree(TRAIN_DIR)
    shutil.rmtree(TEST_DIR)
    os.mkdir(TRAIN_DIR)
    os.mkdir(TEST_DIR)
    # Get list of Chia annotation filenames
    file_list = os.listdir(ANNOTATIONS_DIR)
    # Get a list of the NCT IDs
    nct_ids = set()
    for filename in file_list:
        # First 11 characters of the file name contain the NCT ID
        nct_id = filename[0:11]
        nct_ids.add(nct_id)
    # Convert set to list
    nct_ids = list(nct_ids)
    # Designate NCT IDs for training and testing data
    train_nct_ids = nct_ids[0 : int(len(nct_ids) * 0.8)]
    test_nct_ids = nct_ids[int(len(nct_ids) * 0.8) : len(nct_ids)]
    # Copy training data files
    for nct_id in train_nct_ids:
        # Filter down files relevant to the current trial
        trial_files = [filename for filename in file_list if nct_id in filename]
        # Copy files to the train directory
        for filename in trial_files:
            shutil.copy2(ANNOTATIONS_DIR / filename, TRAIN_DIR)
    # Copy testing data files
    for nct_id in test_nct_ids:
        # Filter down files relevant to the current trial
        trial_files = [filename for filename in file_list if nct_id in filename]
        # Copy files to the test directory
        for filename in trial_files:
            shutil.copy2(ANNOTATIONS_DIR / filename, TEST_DIR)

    nlp = spacy.load("en_core_web_sm")
    keep_labels = load_ner_labels(ANNOTATION_CONF)

    convert_split(TRAIN_DIR, TRAIN_SPACY_DIR, nlp, keep_labels)
    convert_split(TEST_DIR, TEST_SPACY_DIR, nlp, keep_labels)


if __name__ == "__main__":
    main()
