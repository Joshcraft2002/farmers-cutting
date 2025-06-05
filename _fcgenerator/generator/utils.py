from pathlib import Path
import json
import shutil

CLEANUP_DIRS = ['fabric/data', 'neoforge/data', 'forge/data', 'data']

def write_json_file(path: Path, data, indent=2, log_enabled=False) -> bool:
    """Write a JSON file and optionally log the action."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        if log_enabled:
            print(f"Wrote {path}")
        return True
    except Exception as e:
        print(f"Error writing {path}: {e}")
        return False
    
def copy_tree(src_dir: Path, dest_dir: Path):
    """
    Recursively copy all files from src_dir to dest_dir, preserving directory structure.
    """
    if not src_dir.exists():
        return
    for item in src_dir.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(src_dir)
            dest = dest_dir / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)

def cleanup_old_files(mod: str, enable_logging: bool = False):
    """
    Clean up old generated files and directories for a single mod.
    
    :param mod: Mod namespace
    :param enable_logging: Whether to log file operations
    """
    if enable_logging:
        print(f"Cleaning up old files for {mod}...")
        
    for directory in CLEANUP_DIRS:
        path = Path(mod) / Path(directory)
        if path.exists():
            try:
                shutil.rmtree(path)
                if enable_logging:
                    print(f"Removed {path}/")
            except Exception as e:
                # Always print errors regardless of logging setting
                print(f"Error removing {path}/: {e}")