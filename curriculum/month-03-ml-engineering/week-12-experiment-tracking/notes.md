# Notes - Week 12 Experiment Tracking

Once you start training models repeatedly, memory is not enough. You need a record of what you ran, with which parameters, on which data, and what happened. Otherwise, you will quickly ask questions like: Which model produced this artifact? Why did last Tuesday's accuracy look better? Did I change the train/test split or the vectorizer settings?

Experiment tracking is the discipline of storing that information for every run. A run record usually contains:
- a unique run ID
- timestamp
- parameters such as `max_features` or classifier type
- metrics such as accuracy or F1
- artifact paths, for example the saved model file
- dataset version or data source reference

Even a lightweight JSON-based tracker is valuable.

```python
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class ExperimentRun:
    run_id: str
    params: dict[str, str | int | float]
    metrics: dict[str, float]
    artifact_path: str
```

```python
def save_run(run: ExperimentRun, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{run.run_id}.json"
    path.write_text(json.dumps(run.__dict__, indent=2), encoding="utf-8")
    return path
```

The goal is reproducibility. Reproducibility does not mean every stochastic model must produce bit-for-bit identical results forever. It means you can reconstruct the important conditions of a run and understand how it was produced.

Versioning matters here. If you save model artifacts as `model.joblib` every time, you lose history. Prefer run-specific paths such as `artifacts/models/topic-classifier-2024-09-15T1030.joblib` or a UUID-based filename. Then store that artifact path in the run record.

Training code should not rely on a human remembering to log results manually. The tracker should be integrated into the training pipeline so it always records a run when training completes, ideally even on partial failures if that is useful.

A good run record makes comparison easy. Two runs can be compared by classifier choice, feature count, dataset slice, or metrics. This matters because model improvement is rarely linear. Sometimes a "better" configuration only improved one metric while hurting another.

Be careful with what you store. Parameters should be serializable and human-readable. Metrics should be explicit about split or dataset. Artifact references should be durable paths. If the dataset comes from a CSV or SQLite query, store a meaningful reference such as file path, hash, or query description.

Tests this week should verify that training creates a run record, that required keys exist, and that the artifact path in the record actually points to a saved model. This is not glamorous work, but it is foundational for reliable ML engineering.

The broader lesson is that experiments are software outputs, not private lab notes. If the project cannot answer "what changed between these two runs?" then it is not yet mature enough for iterative model work. This week gives ResearchOps the memory it needs.
