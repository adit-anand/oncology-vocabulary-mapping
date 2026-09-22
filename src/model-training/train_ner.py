import argparse
import json
import logging
from pathlib import Path
from typing import Any

import spacy
from spacy.cli.train import train
from spacy.training import Corpus

REPO_ROOT = Path(__file__).resolve().parents[2]
TRAIN_SPACY_DIR = REPO_ROOT / "data" / "annotations" / "train_spacy"
TEST_SPACY_DIR = REPO_ROOT / "data" / "annotations" / "test_spacy"
DEFAULT_CONFIG = Path(__file__).resolve().parent / "spancat_config.cfg"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "model"

logger = logging.getLogger(__name__)


def parse_override(raw: str) -> tuple[str, Any]:
    """Parse a `key=value` CLI override into a (dotted config key, JSON-decoded value)
    pair, matching how `spacy train --key value` overrides are decoded (spacy.cli._util._parse_override)."""
    key, sep, value = raw.partition("=")
    if not sep:
        raise argparse.ArgumentTypeError(f"override {raw!r} must be in KEY=VALUE form")
    try:
        value = json.loads(value)
    except ValueError:
        pass
    return key, value


def main(config_path: Path, output_dir: Path, overrides: dict[str, Any]) -> None:
    train_overrides = {
        "paths.train": str(TRAIN_SPACY_DIR),
        "paths.dev": str(TEST_SPACY_DIR),
        **overrides,
    }
    logger.info("Training spancat model: config=%s output=%s overrides=%s", config_path, output_dir, train_overrides)
    train(config_path, output_path=output_dir, overrides=train_overrides, use_gpu=-1)

    model_best_dir = output_dir / "model-best"
    meta = json.loads((model_best_dir / "meta.json").read_text(encoding="utf-8"))
    performance = meta["performance"]
    logger.info(
        "Aggregate dev performance: spans_sc_p=%.4f spans_sc_r=%.4f spans_sc_f=%.4f",
        performance["spans_sc_p"],
        performance["spans_sc_r"],
        performance["spans_sc_f"],
    )

    nlp = spacy.load(model_best_dir)
    dev_corpus = Corpus(TEST_SPACY_DIR)
    scores = nlp.evaluate(list(dev_corpus(nlp)))
    logger.info("Per-label dev performance (spans_sc_per_type): %s", json.dumps(scores["spans_sc_per_type"], indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Train a spancat NER model on the Chia eligibility-criteria corpus.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to the spaCy training config.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to write model-best/model-last into. Overwrites any existing contents on each run.",
    )
    parser.add_argument(
        "--overrides",
        type=parse_override,
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Repeatable dotted-path config override, e.g. --overrides training.dropout=0.2",
    )
    args = parser.parse_args()

    main(args.config, args.output, dict(args.overrides))
