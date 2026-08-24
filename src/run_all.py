"""
Chạy tất cả các bước lab theo thứ tự hoặc chỉ một bước cụ thể.

Cách dùng:
    python run_all.py            # chạy tất cả 4 bước
    python run_all.py --step 1   # chỉ chạy Bước 1
    python run_all.py --step 3   # chỉ chạy Bước 3 (RAGAS ~15-30 phút)
"""
import sys
import argparse
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def _configure_ascii_streams() -> None:
    """Prevent Windows CP1252 consoles from failing on Unicode output."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="ascii", errors="ignore")


_configure_ascii_streams()


STEPS = {
    1: ("Step 1: LangSmith RAG Pipeline",   "01_langsmith_rag_pipeline"),
    2: ("Step 2: Prompt Hub & A/B Routing", "02_prompt_hub_ab_routing"),
    3: ("Step 3: RAGAS Evaluation",         "03_ragas_evaluation"),
    4: ("Step 4: Guardrails AI Validators", "04_guardrails_validator"),
}


def run_step(step_num: int):
    """Import and execute one lab step, returning whether it succeeded."""
    title, module_name = STEPS[step_num]
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    try:
        module = importlib.import_module(module_name)
        module.main()
        print(f"\n[PASS] {title}")
        return True
    except SystemExit as e:
        if e.code != 0:
            print(f"\n[FAIL] {title} - stopped by configuration or runtime error")
        return e.code == 0
    except Exception as e:
        print(f"\n[FAIL] {title} - {e}")
        return False


def main():
    """Parse CLI arguments, run selected steps, and return a process exit code."""
    parser = argparse.ArgumentParser(
        description="Run Day22 Lab: LangSmith + Prompt Versioning + RAGAS + Guardrails"
    )
    parser.add_argument(
        "--step", type=int, choices=[1, 2, 3, 4],
        help="Run only the selected step (1-4)"
    )
    args = parser.parse_args()

    steps_to_run = [args.step] if args.step else list(STEPS.keys())

    results = {}
    for step_num in steps_to_run:
        success = run_step(step_num)
        results[step_num] = success
        if not success and not args.step:
            print(f"\n[STOP] Step {step_num} failed; remaining steps were not run.")
            break

    # Summary
    print(f"\n{'=' * 60}")
    print("  Summary")
    print(f"{'=' * 60}")
    for step_num, success in results.items():
        title = STEPS[step_num][0]
        status = "PASS" if success else "FAIL"
        print(f"  {status}  {title}")

    return 0 if results and all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
