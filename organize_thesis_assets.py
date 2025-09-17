"""Script to consolidate existing project outputs into unified thesis_images folder.

Run once (or as needed) to migrate/copy current artifacts into the standardized
structure used by ThesisAssetManager.

Safe to re-run: it will overwrite existing standardized copies but will not
delete originals.
"""
from pathlib import Path
import json
import shutil
from thesis_asset_manager import ThesisAssetManager


PROJECT_ROOT = Path(__file__).parent
ASSET_MANAGER = ThesisAssetManager()

# Mapping of source directories to handler metadata
FIGURE_SOURCES = [PROJECT_ROOT / "figures", PROJECT_ROOT / "exports"]
TABLE_SOURCES = [PROJECT_ROOT / "exports", PROJECT_ROOT / "results"]
MODEL_SOURCES = [PROJECT_ROOT / "models"]


def copy_if_exists(src: Path, dst: Path):
    if src.exists():
        shutil.copy2(src, dst)


def organize_figures():
    figure_exts = {".png", ".svg", ".pdf"}
    for folder in FIGURE_SOURCES:
        if not folder.exists():
            continue
        for f in folder.iterdir():
            if f.suffix.lower() in figure_exts and f.is_file():
                # Derive section from filename heuristics
                stem = f.stem.lower()
                if "causal" in stem:
                    section = "causal_inference"
                elif "lstm" in stem or "forecast" in stem:
                    section = "forecasting"
                elif "vat" in stem or "policy" in stem or "impact" in stem:
                    section = "policy_analysis"
                else:
                    section = "general"
                name = stem
                try:
                    # Use manager to register by temporarily loading figure? Not possible. Just copy.
                    out_name = f"{section}__{name}__v1.0{f.suffix.lower()}"
                    out_path = ASSET_MANAGER.subdirs["figures"] / out_name
                    shutil.copy2(f, out_path)
                    ASSET_MANAGER._register(
                        category="figure",
                        section=section,
                        name=name,
                        version="v1.0",
                        filename=out_name,
                        path=out_path,
                        tags=[section],
                        description=f"Imported existing figure from {f.relative_to(PROJECT_ROOT)}",
                        source_code_reference=None,
                    )
                except Exception as e:
                    print(f"[WARN] Could not import figure {f}: {e}")


def organize_tables():
    csv_ext = ".csv"
    for folder in TABLE_SOURCES:
        if not folder.exists():
            continue
        for f in folder.iterdir():
            if f.suffix.lower() == csv_ext and f.is_file():
                stem = f.stem.lower()
                if any(k in stem for k in ["performance", "validation", "stability"]):
                    section = "model_evaluation"
                elif any(k in stem for k in ["policy", "vat", "impact", "scenario"]):
                    section = "policy_analysis"
                elif any(k in stem for k in ["feature_importance", "heterogeneous", "causal_forest", "dml"]):
                    section = "causal_inference"
                elif any(k in stem for k in ["forecast", "lstm", "economic_forecasts"]):
                    section = "forecasting"
                else:
                    section = "general"
                name = stem
                out_name = f"{section}__{name}__v1.0.csv"
                out_path = ASSET_MANAGER.subdirs["tables"] / out_name
                try:
                    shutil.copy2(f, out_path)
                    # We won't parse CSV here to avoid pandas dependency at script run.
                    ASSET_MANAGER._register(
                        category="table",
                        section=section,
                        name=name,
                        version="v1.0",
                        filename=out_name,
                        path=out_path,
                        tags=[section],
                        description=f"Imported existing table from {f.relative_to(PROJECT_ROOT)}",
                        source_code_reference=None,
                    )
                except Exception as e:
                    print(f"[WARN] Could not import table {f}: {e}")


def organize_models():
    for folder in MODEL_SOURCES:
        if not folder.exists():
            continue
        for f in folder.iterdir():
            if f.is_file():
                stem = f.stem.lower()
                if "lstm" in stem:
                    section = "forecasting"
                else:
                    section = "models"
                name = stem
                ext = f.suffix.lower().lstrip('.') or 'bin'
                out_name = f"{section}__{name}__v1.0.{ext}"
                out_path = ASSET_MANAGER.subdirs["models"] / out_name
                try:
                    shutil.copy2(f, out_path)
                    ASSET_MANAGER._register(
                        category="model",
                        section=section,
                        name=name,
                        version="v1.0",
                        filename=out_name,
                        path=out_path,
                        tags=[section],
                        description=f"Imported existing model artifact from {f.relative_to(PROJECT_ROOT)}",
                        source_code_reference=None,
                    )
                except Exception as e:
                    print(f"[WARN] Could not import model {f}: {e}")


def main():
    print("Organizing existing thesis assets...")
    organize_figures()
    organize_tables()
    organize_models()
    print("Done. Manifest entries:", len(ASSET_MANAGER.list()))
    print(f"Manifest JSON: {ASSET_MANAGER.manifest_path}")
    print(f"Manifest CSV: {ASSET_MANAGER.manifest_csv_path}")


if __name__ == "__main__":
    main()
