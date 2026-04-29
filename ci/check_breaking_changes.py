import json
import sys
from pathlib import Path
import argparse

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent
SNAPSHOT_DIR = SCRIPT_DIR / "snapshots"
CURRENT_DIR = SCRIPT_DIR.parent / "schema"

def get_nested_type(props, key):
    """Recursively find types in nested schemas."""
    prop = props.get(key, {})
    if "type" in prop:
        return prop["type"]
    if "$ref" in prop:
        return "ref"
    if "anyOf" in prop:
        return "union"
    return "unknown"

def compare_schemas(old_schema, new_schema, name):
    """Compares two JSON schemas for breaking changes."""
    errors = []
    
    old_props = old_schema.get("properties", {})
    new_props = new_schema.get("properties", {})
    
    # 1. Check for removed fields
    for field in old_props:
        if field not in new_props:
            errors.append(f"BREAKING: Field '{field}' was removed from model '{name}'")
            continue
            
        # 2. Check for type changes
        old_type = get_nested_type(old_props, field)
        new_type = get_nested_type(new_props, field)
        
        if old_type != new_type:
            errors.append(f"BREAKING: Type changed for field '{field}' in model '{name}': {old_type} -> {new_type}")

    # 3. Check required-field drift
    old_required = set(old_schema.get("required", []))
    new_required = set(new_schema.get("required", []))
    removed_required = old_required - new_required
    if removed_required:
        errors.append(f"BREAKING: Required fields removed from '{name}': {sorted(removed_required)}")

    # 4. Check top-level additionalProperties contract drift
    if old_schema.get("additionalProperties", True) != new_schema.get("additionalProperties", True):
        errors.append(
            f"BREAKING: additionalProperties changed in '{name}': "
            f"{old_schema.get('additionalProperties', True)} -> {new_schema.get('additionalProperties', True)}"
        )

    # 5. Check for enum changes (if applicable)
    if "enum" in old_schema:
        old_enums = set(old_schema["enum"])
        new_enums = set(new_schema.get("enum", []))
        removed_enums = old_enums - new_enums
        if removed_enums:
            errors.append(f"BREAKING: Enum values removed from '{name}': {removed_enums}")

    return errors

def create_snapshots():
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    for schema_file in CURRENT_DIR.glob("*.json"):
        target = SNAPSHOT_DIR / schema_file.name
        with open(schema_file, "r") as src, open(target, "w") as dst:
            dst.write(src.read())
    print(f"Snapshots created in {SNAPSHOT_DIR}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", action="store_true", help="Create new snapshots from current contracts")
    args = parser.parse_args()

    if args.snapshot:
        create_snapshots()
        return

    if not SNAPSHOT_DIR.exists():
        print(f"ERROR: Snapshot directory {SNAPSHOT_DIR} not found. Run with --snapshot first.")
        sys.exit(1)

    total_errors = []
    current_schema_names = {p.name for p in CURRENT_DIR.glob("*.json")}

    for snapshot_file in SNAPSHOT_DIR.glob("*.json"):
        current_file = CURRENT_DIR / snapshot_file.name
        if not current_file.exists():
            total_errors.append(f"BREAKING: Current schema for {snapshot_file.name} is missing.")
            continue
            
        with open(snapshot_file, "r") as f:
            old_schema = json.load(f)
        with open(current_file, "r") as f:
            new_schema = json.load(f)
            
        errors = compare_schemas(old_schema, new_schema, snapshot_file.stem)
        total_errors.extend(errors)

    # New schema files are additive (allowed), but surface signal for governance.
    snapshot_names = {p.name for p in SNAPSHOT_DIR.glob("*.json")}
    added = sorted(current_schema_names - snapshot_names)
    if added:
        print(f"INFO: New schema files detected (additive): {added}")

    if total_errors:
        print("\n--- PROTOCOL VIOLATION DETECTED ---")
        for err in total_errors:
            print(err)
        print("\nFix the breaking changes or if intentional, run a major version bump and re-snapshot.")
        sys.exit(1)
    else:
        print("Success: No breaking changes detected in aureon-contracts.")

if __name__ == "__main__":
    main()
