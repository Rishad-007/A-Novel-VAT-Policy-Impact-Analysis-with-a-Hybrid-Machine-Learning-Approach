"""Thesis Asset Manager
=======================

Utility functions to standardize saving of all thesis artifacts (figures, tables,
data extracts, model objects, and summaries) into a single cohesive folder
hierarchy with a machine-readable manifest for easy referencing inside the
manuscript.

Folder Layout (root: thesis_images/)
------------------------------------
figures/            -> All static images (.png, .svg, optionally .pdf)
tables/             -> Tabular data exported as CSV + accompanying JSON metadata
data_snapshots/     -> Aggregated or intermediate dataset snapshots (CSV/Parquet)
models/             -> Serialized model artifacts (e.g., .h5, .pkl)
summaries/          -> Narrative or executive summary JSON/TXT
manifests/          -> Auto-generated manifest + index files

Naming Convention
-----------------
<section>__<short_descriptor>__v<major.minor>.<ext>
Examples:
  forecasting__lstm_training_history__v1.0.png
  causal_inference__feature_importance_cf__v1.0.csv

The manifest (JSON + CSV) tracks:
  id, category, section, name, version, filename, path, created_at, tags, description, source_code_reference

Usage Pattern in Notebook
-------------------------
from thesis_asset_manager import ThesisAssetManager
assets = ThesisAssetManager()
fig, ax = plt.subplots(); ...; assets.save_figure(fig, section="forecasting", name="hybrid_model_results", description="Comparison of model performance")

This module is intentionally lightweight (stdlib + optional pandas/matplotlib awareness) to avoid heavy deps.
"""
from __future__ import annotations

import json
import os
import shutil
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - optional
    pd = None  # type: ignore

try:  # for type hints only; not mandatory
    import matplotlib.pyplot as plt  # type: ignore
    from matplotlib.figure import Figure  # type: ignore
except Exception:  # pragma: no cover
    Figure = Any  # type: ignore


ROOT_DIR_NAME = "thesis_images"


@dataclass
class AssetRecord:
    id: str
    category: str
    section: str
    name: str
    version: str
    filename: str
    path: str
    created_at: str
    tags: List[str]
    description: str
    source_code_reference: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ThesisAssetManager:
    def __init__(self, root: Union[str, Path] = ROOT_DIR_NAME, auto_create: bool = True):
        self.root = Path(root)
        self.subdirs = {
            "figures": self.root / "figures",
            "tables": self.root / "tables",
            "data_snapshots": self.root / "data_snapshots",
            "models": self.root / "models",
            "summaries": self.root / "summaries",
            "manifests": self.root / "manifests",
        }
        if auto_create:
            self._ensure_dirs()
        self.manifest_path = self.subdirs["manifests"] / "asset_manifest.json"
        self.manifest_csv_path = self.subdirs["manifests"] / "asset_manifest.csv"
        self._manifest: List[AssetRecord] = []
        if self.manifest_path.exists():
            self._load_manifest()

    # ---------------- Directory & Manifest Handling -----------------
    def _ensure_dirs(self) -> None:
        for p in self.subdirs.values():
            p.mkdir(parents=True, exist_ok=True)

    def _load_manifest(self) -> None:
        try:
            data = json.loads(self.manifest_path.read_text())
            self._manifest = [AssetRecord(**row) for row in data]
        except Exception:
            self._manifest = []

    def _write_manifest(self) -> None:
        serializable = [r.to_dict() for r in self._manifest]
        self.manifest_path.write_text(json.dumps(serializable, indent=2))
        # Also write CSV for quick viewing
        if pd is not None and serializable:
            pd.DataFrame(serializable).to_csv(self.manifest_csv_path, index=False)

    # ---------------- Helper Methods -----------------
    @staticmethod
    def _normalize(text: str) -> str:
        return (
            text.strip().lower()
            .replace(" ", "_")
            .replace("/", "-")
            .replace("__", "_")
        )

    def _build_filename(self, section: str, name: str, version: str, ext: str) -> str:
        section_n = self._normalize(section)
        name_n = self._normalize(name)
        ver = version if version.startswith("v") else f"v{version}"
        return f"{section_n}__{name_n}__{ver}.{ext}"

    def _register(self, category: str, section: str, name: str, version: str, filename: str, path: Path, tags: Optional[List[str]], description: str, source_code_reference: Optional[str]) -> AssetRecord:
        rec = AssetRecord(
            id=str(uuid.uuid4()),
            category=category,
            section=self._normalize(section),
            name=self._normalize(name),
            version=version if version.startswith("v") else f"v{version}",
            filename=filename,
            path=str(path.relative_to(self.root)),
            created_at=datetime.utcnow().isoformat() + "Z",
            tags=sorted(set([self._normalize(t) for t in (tags or [])])),
            description=description,
            source_code_reference=source_code_reference,
        )
        # Deduplicate by category/section/name/version
        self._manifest = [m for m in self._manifest if not (
            m.category == rec.category and m.section == rec.section and m.name == rec.name and m.version == rec.version
        )]
        self._manifest.append(rec)
        self._write_manifest()
        return rec

    # ---------------- Public Save Methods -----------------
    def save_figure(self, fig: 'Figure', section: str, name: str, version: str = "1.0", tags: Optional[List[str]] = None, description: str = "", source_code_reference: Optional[str] = None, formats: Optional[List[str]] = None, dpi: int = 300) -> List[AssetRecord]:
        """Save a matplotlib figure in one or more formats and register.

        Returns list of AssetRecord for each saved format.
        """
        if formats is None:
            formats = ["png"]
        records = []
        for fmt in formats:
            filename = self._build_filename(section, name, version, fmt)
            out_path = self.subdirs["figures"] / filename
            fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
            records.append(self._register(
                category="figure",
                section=section,
                name=name,
                version=f"v{version}" if not version.startswith("v") else version,
                filename=filename,
                path=out_path,
                tags=tags,
                description=description,
                source_code_reference=source_code_reference,
            ))
        return records

    def save_table(self, df: 'pd.DataFrame', section: str, name: str, version: str = "1.0", tags: Optional[List[str]] = None, description: str = "", source_code_reference: Optional[str] = None, include_json: bool = True) -> AssetRecord:
        if pd is None:
            raise RuntimeError("pandas not available; cannot save table")
        filename = self._build_filename(section, name, version, "csv")
        out_path = self.subdirs["tables"] / filename
        df.to_csv(out_path, index=False)
        if include_json:
            meta = {
                "columns": list(df.columns),
                "shape": list(df.shape),
                "preview": df.head(10).to_dict(orient="records"),
                "description": description,
            }
            json_name = filename.replace(".csv", ".meta.json")
            (self.subdirs["tables"] / json_name).write_text(json.dumps(meta, indent=2))
        return self._register(
            category="table",
            section=section,
            name=name,
            version=f"v{version}" if not version.startswith("v") else version,
            filename=filename,
            path=out_path,
            tags=tags,
            description=description,
            source_code_reference=source_code_reference,
        )

    def save_data_snapshot(self, df: 'pd.DataFrame', section: str, name: str, version: str = "1.0", tags: Optional[List[str]] = None, description: str = "", source_code_reference: Optional[str] = None) -> AssetRecord:
        if pd is None:
            raise RuntimeError("pandas not available; cannot save data snapshot")
        filename = self._build_filename(section, name, version, "csv")
        out_path = self.subdirs["data_snapshots"] / filename
        df.to_csv(out_path, index=False)
        return self._register(
            category="data_snapshot",
            section=section,
            name=name,
            version=f"v{version}" if not version.startswith("v") else version,
            filename=filename,
            path=out_path,
            tags=tags,
            description=description,
            source_code_reference=source_code_reference,
        )

    def save_summary(self, content: Union[str, Dict[str, Any]], section: str, name: str, version: str = "1.0", tags: Optional[List[str]] = None, description: str = "", source_code_reference: Optional[str] = None) -> AssetRecord:
        if isinstance(content, dict):
            ext = "json"
            filename = self._build_filename(section, name, version, ext)
            out_path = self.subdirs["summaries"] / filename
            out_path.write_text(json.dumps(content, indent=2))
        else:
            ext = "txt"
            filename = self._build_filename(section, name, version, ext)
            out_path = self.subdirs["summaries"] / filename
            out_path.write_text(content)
        return self._register(
            category="summary",
            section=section,
            name=name,
            version=f"v{version}" if not version.startswith("v") else version,
            filename=filename,
            path=out_path,
            tags=tags,
            description=description,
            source_code_reference=source_code_reference,
        )

    def save_model(self, source_path: Union[str, Path], section: str, name: str, version: str = "1.0", tags: Optional[List[str]] = None, description: str = "", source_code_reference: Optional[str] = None, copy: bool = True) -> AssetRecord:
        src = Path(source_path)
        if not src.exists():
            raise FileNotFoundError(f"Model artifact not found: {src}")
        ext = src.suffix.lstrip('.') or 'bin'
        filename = self._build_filename(section, name, version, ext)
        out_path = self.subdirs["models"] / filename
        if copy:
            shutil.copy2(src, out_path)
        else:
            # create a lightweight reference file
            out_path.write_text(f"REFERENCE -> {src}")
        return self._register(
            category="model",
            section=section,
            name=name,
            version=f"v{version}" if not version.startswith("v") else version,
            filename=filename,
            path=out_path,
            tags=tags,
            description=description,
            source_code_reference=source_code_reference,
        )

    # ---------------- Query Methods -----------------
    def list(self, category: Optional[str] = None, section: Optional[str] = None) -> List[AssetRecord]:
        items = self._manifest
        if category:
            items = [i for i in items if i.category == self._normalize(category)]
        if section:
            items = [i for i in items if i.section == self._normalize(section)]
        return items

    def to_dataframe(self):  # type: ignore
        if pd is None:
            raise RuntimeError("pandas not available")
        return pd.DataFrame([r.to_dict() for r in self._manifest])

    # ---------------- Convenience -----------------
    def ensure(self):
        self._ensure_dirs()
        return self

__all__ = ["ThesisAssetManager", "AssetRecord"]
