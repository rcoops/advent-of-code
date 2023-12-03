from pathlib import Path


def read_resource(resource_file_name: str) -> str:
    with open(Path(f"resources/{resource_file_name}")) as f:
        return f.read()
