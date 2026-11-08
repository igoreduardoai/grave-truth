"""Run the offline adjudication scenarios. Does not call a model."""

from validation.adjudication.loop import run_all_scenarios
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    result = run_all_scenarios(ROOT)
    print(f"adjudication scenarios {sum(item['matched'] for item in result['scenarios'])}/{len(result['scenarios'])}")
    print("live evaluator/critic: not validated")
    for item in result["scenarios"]:
        print(f"{item['scenario']}: {item['stop']} expected {item['expected_stop']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
