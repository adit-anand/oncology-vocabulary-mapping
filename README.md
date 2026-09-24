# ohdsi-2026

Trains a spaCy `spancat` model to recognize clinical entities (Condition, Drug,
Observation, Measurement, Procedure) in clinical trial eligibility criteria,
using the Chia corpus of brat-annotated eligibility criteria as training data.

## Prerequisites

- Python 3.13 (see `.python-version`)
- [`uv`](https://docs.astral.sh/uv/) for dependency management and running scripts

If you're using the provided devcontainer (`.devcontainer/devcontainer.json`), both are
already installed.

## Setup

1. Clone the repo and install dependencies:

   ```
   uv sync
   ```

   This installs `spacy`, `medspacy`, `spacy-transformers`, and the
   [`en_core_sci_scibert`](https://allenai.github.io/scispacy/) pipeline (pinned to a
   source-URL dependency in `pyproject.toml`) into a local `.venv`. `en_core_sci_scibert`
   is a ~1.4 GB download (it bundles SciBERT transformer weights), so the first `uv sync`
   can take a while.

2. Set up the data directories. `data/` is gitignored, so it isn't checked into
   version control and must be populated locally:

   ```
   data/
     annotations/
       annotation.conf       # brat config declaring entity labels (!CONCEPTS section)
       chia-files/            # raw Chia corpus: <NCT_ID>_inc.txt/.ann, <NCT_ID>_exc.txt/.ann pairs
     model/                    # created by training/evaluation scripts
   ```

   Obtain the [Chia dataset](https://figshare.com/articles/dataset/Chia_Annotated_Datasets/11855817)
   (brat-format `.txt`/`.ann` pairs of clinical trial inclusion/exclusion criteria)
   and place the files directly under `data/annotations/chia-files/`. Also place the
   brat `annotation.conf` for the dataset at `data/annotations/annotation.conf`.

## Pipeline

Run each step with `uv run`, from the repo root.

1. **Split into train/test and convert to spaCy format.** Splits `chia-files/` 80/20
   by clinical trial (NCT) id into `data/annotations/train/` and `test/`, then
   converts each brat `.txt`/`.ann` pair into a `.spacy` `DocBin` file (entities
   stored as overlapping spans in `doc.spans["sc"]`) under `train_spacy/` and
   `test_spacy/`:

   ```
   uv run python src/data-preparation/train_test_split.py
   ```

2. **Train the model.** Trains a `spancat` pipeline (config at
   `src/model-training/spancat_config.cfg`, fine-tuning the SciBERT transformer that
   backs `en_core_sci_scibert`) on `train_spacy/`, evaluating against `test_spacy/`
   as it goes. Writes
   `model-best`/`model-last` to `data/model/`:

   ```
   uv run python src/model-training/train_ner.py
   ```

   Pass `--config`, `--output`, or `--overrides KEY=VALUE` (repeatable) to override
   the config path, output directory, or individual config values.

3. **Evaluate the trained model.** Scores `data/model/model-best` against
   `test_spacy/` and writes `evaluation_report.json`/`.txt` to `data/model/`:

   ```
   uv run python src/model-training/evaluate_model.py
   ```

4. **Run inference on sample text.**

   ```
   uv run python src/model-training/predict_example.py
   ```
