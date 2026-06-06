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


def apply_timestamped_output_dir(raw_config: dict[str, Any], base_dir: str = "outputs") -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_dir = Path(base_dir) / timestamp
    output_cfg = raw_config.get("output", {})
    for key, current_path in list(output_cfg.items()):
        file_name = Path(str(current_path)).name
        output_cfg[key] = str(output_dir / file_name)
    raw_config["output"] = output_cfg
    return str(output_dir)

