from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path

__USAGE = """Command line script to run the solutions for the Advent of Code 2023.

Usage (pdm): pdm run solve <day> [-s <step>] [-e]
Usage: python -m advent_of_code_2023.cli <day> [-s <step>] [-e]
"""


def _read_resource(resource_file_name: str) -> str:
    with open(Path(f"resources/{resource_file_name}")) as f:
        return f.read()


def run():
    parser = ArgumentParser(description=__USAGE)
    parser.add_argument("day", type=int, help="The day of the challenge to run.")
    parser.add_argument(
        "-s",
        "--step",
        default="1",
        choices=("1", "2"),
        help="Which step of the day's challenge to run.",
    )
    parser.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="Run against the *example* input rather than the main test.",
    )
    parser.add_argument(
        "-m",
        "--method",
        help="Which method to use for the solution, if available",
    )
    args = parser.parse_args()

    module = f"day_{args.day:02}"
    mod = import_module(f"advent_of_code_2023.{module}.step_{args.step}")
    run_command = getattr(mod, "solve")
    resource_name = f"step_{args.step}_example.txt" if args.example else "input.txt"
    try:
        resource_content = _read_resource(f"{module}/{resource_name}")
    except Exception:
        resource_content = _read_resource(f"{module}/example.txt")

    if args.method is None:
        result = run_command(resource_content)
    else:
        result = run_command(resource_content, args.method)

    print(result)


# For debug
if __name__ == "__main__":
    run()
