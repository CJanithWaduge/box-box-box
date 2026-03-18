import json
import subprocess
import sys
from pathlib import Path
from typing import List

# Configuration
SOLUTION_CMD_FILE = Path("solution/run_command.txt")
INPUT_DIR  = Path("data/test_cases/inputs")
EXPECTED_DIR = Path("data/test_cases/expected_outputs")

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"


def get_solution_command() -> str:
    if not SOLUTION_CMD_FILE.exists():
        print(f"{RED}Error: {SOLUTION_CMD_FILE} not found.{RESET}")
        sys.exit(1)
    with open(SOLUTION_CMD_FILE, "r", encoding="utf-8") as f:
        cmd = f.read().strip()
    return cmd


def run_your_solution(input_path: Path, cmd: str) -> str:
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            input_json = f.read()

        result = subprocess.run(
            cmd,
            input=input_json,
            text=True,
            capture_output=True,
            shell=True,
            timeout=20
        )

        if result.returncode != 0:
            print(f"{RED}Execution failed for {input_path.name}{RESET}")
            print(result.stderr.strip())
            return ""

        return result.stdout.strip()

    except Exception as e:
        print(f"{RED}Exception running solution: {e}{RESET}")
        return ""


def load_positions(json_str: str) -> List[str]:
    try:
        data = json.loads(json_str)
        return data.get("finishing_positions", [])
    except:
        return []


def compare_lists(pred: List[str], exp: List[str]) -> tuple[int, float]:
    if len(pred) != 20 or len(exp) != 20:
        return 0, 0.0

    correct = sum(1 for a, b in zip(pred, exp) if a == b)
    percent = (correct / 20) * 100
    return correct, percent


def main():
    cmd = get_solution_command()
    print(f"Using command: {cmd}\n")

    input_files = sorted(INPUT_DIR.glob("test_*.json"))
    if not input_files:
        print(f"{RED}No input files found in {INPUT_DIR}{RESET}")
        return

    total_correct_races = 0
    total_tests = 0

    print("═" * 70)

    for idx, inp_file in enumerate(input_files, 1):
        test_id = inp_file.stem.upper()  # TEST_001 etc.

        exp_file = EXPECTED_DIR / f"{inp_file.stem}.json"
        if not exp_file.exists():
            print(f"{RED}Missing expected file: {exp_file}{RESET}")
            continue

        print(f"{test_id}")

        # Run your solution
        your_output = run_your_solution(inp_file, cmd)
        if not your_output:
            print(f"  {RED}Your solution produced no output or crashed{RESET}\n")
            continue

        your_positions = load_positions(your_output)
        if not your_positions:
            print(f"  {RED}Invalid JSON or missing finishing_positions{RESET}\n")
            continue

        # Load expected
        with open(exp_file, "r", encoding="utf-8") as f:
            exp_data = json.load(f)
        expected_positions = exp_data.get("finishing_positions", [])

        correct_count, percent = compare_lists(your_positions, expected_positions)

        print(f"  Predicted positions (your script):")
        print(f"    {', '.join(your_positions)}")
        print(f"  Expected positions:")
        print(f"    {', '.join(expected_positions)}")
        print(f"  Correct positions: {correct_count}/20 → {percent:.1f}%")

        if correct_count == 20:
            total_correct_races += 1
            print(f"  {GREEN}FULL MATCH{RESET}")
        else:
            print(f"  {RED}Not fully correct{RESET}")

        print("─" * 70)
        total_tests += 1

    # Final score (as per challenge: % of fully correct races)
    if total_tests > 0:
        score = (total_correct_races / total_tests) * 100
        print(f"\nFinal Score: {total_correct_races}/{total_tests} → {score:.1f}%")
        print("(Challenge score = percentage of races where entire finishing order is exactly correct)")
    else:
        print("\nNo valid tests compared.")


if __name__ == "__main__":
    main()