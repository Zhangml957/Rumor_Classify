from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def ensure_parent(path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


def write_json(path: str | Path, payload: dict) -> None:
    out = ensure_parent(path)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: str | Path, df: pd.DataFrame) -> None:
    out = ensure_parent(path)
    df.to_csv(out, index=False)


def _find_latest_timestamped_checkpoint(base_dir: Path, checkpoint_name: str) -> Path | None:
    if not base_dir.exists():
        return None
    run_dirs = sorted((p for p in base_dir.iterdir() if p.is_dir()), key=lambda p: p.name, reverse=True)
    for run_dir in run_dirs:
        candidate = run_dir / "checkpoints" / checkpoint_name
        if (candidate / "config.json").exists():
            return candidate
    return None


def apply_timestamped_output_dir(
    raw_config: dict[str, Any],
    base_dir: str = "outputs",
    checkpoint_mode: str = "new",
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_dir = Path(base_dir) / timestamp
    output_cfg = raw_config.get("output", {})
    for key, current_path in list(output_cfg.items()):
        file_name = Path(str(current_path)).name
        output_cfg[key] = str(output_dir / file_name)
    raw_config["output"] = output_cfg

    model_cfg = raw_config.get("model", {})
    checkpoint_dir = model_cfg.get("checkpoint_dir")
    if checkpoint_dir:
        checkpoint_name = Path(str(checkpoint_dir).rstrip("/\\")).name or "model"
        if checkpoint_mode == "new":
            model_cfg["checkpoint_dir"] = str(output_dir / "checkpoints" / checkpoint_name)
        elif checkpoint_mode == "latest":
            latest_ckpt = _find_latest_timestamped_checkpoint(Path(base_dir), checkpoint_name)
            if latest_ckpt is not None:
                model_cfg["checkpoint_dir"] = str(latest_ckpt)
        raw_config["model"] = model_cfg

    return str(output_dir)

