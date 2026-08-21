"""
MkDocs hook: convert libraries/*.yml -> doc/assets/data/*.json before each build.
"""

import json
import logging
import os

import yaml

log = logging.getLogger("mkdocs.plugins.yaml_to_json")

# Points to the blob view (rendered) rather than the raw view.
GITHUB_BASE = "https://github.com/AntaresSimulatorTeam/GEMS/blob/main/libraries"

def on_pre_build(config):
    """Called by MkDocs before the build starts (also on every `mkdocs serve` reload)."""
    # config["docs_dir"] is the absolute path to the doc/ directory.
    # The libraries/ folder sits one level up, at the project root.
    docs_dir = config["docs_dir"]
    project_root = os.path.dirname(docs_dir)
    libraries_dir = os.path.join(project_root, "libraries")
    output_dir = os.path.join(docs_dir, "assets", "data")

    if not os.path.isdir(libraries_dir):
        log.debug("yaml_to_json: libraries/ not found, skipping")
        return

    yml_files = [f for f in os.listdir(libraries_dir) if f.endswith(".yml")]
    if not yml_files:
        log.debug("yaml_to_json: no .yml files in libraries/, skipping")
        return

    # Create the output directory if it does not exist yet (first build).
    os.makedirs(output_dir, exist_ok=True)

    for filename in yml_files:
        yml_path = os.path.join(libraries_dir, filename)
        stem = os.path.splitext(filename)[0]
        json_path = os.path.join(output_dir, f"{stem}.json")

        try:
            with open(yml_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            # Inject the GitHub URL into the JSON payload so yaml-loader.js can
            # read it directly instead of reconstructing it from the asset URL.
            data["_github_url"] = f"{GITHUB_BASE}/{filename}"

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            log.debug("yaml_to_json: %s → %s", filename, json_path)
        except Exception as exc:
            log.warning("yaml_to_json: failed to convert %s: %s", filename, exc)
