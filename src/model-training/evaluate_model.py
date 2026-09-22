import json
import logging
from pathlib import Path
from typing import Any

import spacy
from spacy.scorer import PRFScore
from spacy.training import Corpus

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = REPO_ROOT / "data" / "model" / "model-best"
TEST_SPACY_DIR = REPO_ROOT / "data" / "annotations" / "test_spacy"
OUTPUT_JSON = REPO_ROOT / "data" / "model" / "evaluation_report.json"
OUTPUT_TXT = REPO_ROOT / "data" / "model" / "evaluation_report.txt"

SPANS_KEY = "sc"

logger = logging.getLogger(__name__)


def score_spans(examples: list) -> dict[str, Any]:
    """Score predicted doc.spans["sc"] against gold, aligned the same way
    spacy.pipeline.spancat.spancat_score does, but also keeping tp/fp/fn counts so
    accuracy (tp / (tp + fp + fn), i.e. exact-match rate over the union of predicted
    and gold spans - there's no well-defined "true negative" span to base a
    conventional accuracy on) can be reported alongside precision/recall/F1.
    """
    overall = PRFScore()
    per_label: dict[str, PRFScore] = {}

    for example in examples:
        gold_spans = {
            (span.label_, span.start, span.end - 1)
            for span in example.reference.spans.get(SPANS_KEY, [])
        }
        aligned_pred_spans = example.get_aligned_spans_x2y(
            example.predicted.spans.get(SPANS_KEY, []), allow_overlap=True
        )
        pred_spans = {(span.label_, span.start, span.end - 1) for span in aligned_pred_spans}

        labels = {label for label, _, _ in gold_spans | pred_spans}
        for label in labels:
            per_label.setdefault(label, PRFScore())
            gold_label = {s for s in gold_spans if s[0] == label}
            pred_label = {s for s in pred_spans if s[0] == label}
            per_label[label].tp += len(pred_label & gold_label)
            per_label[label].fp += len(pred_label - gold_label)
            per_label[label].fn += len(gold_label - pred_label)

        overall.tp += len(pred_spans & gold_spans)
        overall.fp += len(pred_spans - gold_spans)
        overall.fn += len(gold_spans - pred_spans)

    def to_report(score: PRFScore) -> dict[str, float]:
        return {
            "accuracy": score.tp / (score.tp + score.fp + score.fn) if len(score) else 0.0,
            "precision": score.precision,
            "recall": score.recall,
            "f1": score.fscore,
        }

    return {
        "overall": to_report(overall),
        "per_label": {label: to_report(score) for label, score in sorted(per_label.items())},
    }


def main() -> None:
    logger.info("Loading model from %s", MODEL_DIR)
    nlp = spacy.load(MODEL_DIR)

    logger.info("Loading test corpus from %s", TEST_SPACY_DIR)
    examples = list(Corpus(TEST_SPACY_DIR)(nlp))
    docs = nlp.pipe(eg.predicted for eg in examples)
    for eg, doc in zip(examples, docs):
        eg.predicted = doc

    report = score_spans(examples)

    OUTPUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        f"Evaluation of {MODEL_DIR.relative_to(REPO_ROOT)} "
        f"against {TEST_SPACY_DIR.relative_to(REPO_ROOT)}",
        "",
        "Overall:",
        f"  Accuracy:  {report['overall']['accuracy']:.4f}",
        f"  Precision: {report['overall']['precision']:.4f}",
        f"  Recall:    {report['overall']['recall']:.4f}",
        f"  F1:        {report['overall']['f1']:.4f}",
        "",
        "Per label:",
    ]
    for label, scores in report["per_label"].items():
        lines.append(
            f"  {label:<12} accuracy={scores['accuracy']:.4f} "
            f"precision={scores['precision']:.4f} recall={scores['recall']:.4f} "
            f"f1={scores['f1']:.4f}"
        )
    OUTPUT_TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    logger.info("Wrote %s and %s", OUTPUT_JSON, OUTPUT_TXT)
    logger.info("Overall: %s", report["overall"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
