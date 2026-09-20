import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


STEPS = [
    (
        "1/7 Generate synthetic inclusion survey",
        "generate_survey.py",
    ),
    (
        "2/7 Calculate Inclusion Index and segment gaps",
        "inclusion_metrics.py",
    ),
    (
        "3/7 Run inclusion association analysis",
        "inclusion_drivers.py",
    ),
    (
        "4/7 Generate DE&I event data",
        "generate_events.py",
    ),
    (
        "5/7 Analyse DE&I event effectiveness",
        "event_analysis.py",
    ),
    (
        "6/7 Build inclusion dashboard",
        "build_inclusion_dashboard.py",
    ),
    (
        "7/7 Build executive inclusion report",
        "build_inclusion_report.py",
    ),
]


def run_script(label, filename):
    print()
    print("=" * 70)
    print(label)
    print("=" * 70)

    script = ROOT / "src" / filename

    subprocess.run(
        [sys.executable, str(script)],
        check=True,
        cwd=ROOT,
    )


def main():
    print()
    print("GLOBAL INCLUSION & BELONGING ANALYTICS")
    print("======================================")

    for label, filename in STEPS:
        run_script(label, filename)

    print()
    print("=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)

    print()
    print("Key outputs:")
    print()
    print("  Dashboard:")
    print("    index.html")
    print()
    print("  Survey analytics:")
    print("    data/inclusion_dimension_summary.csv")
    print("    data/inclusion_segment_summary.csv")
    print("    data/inclusion_driver_summary.csv")
    print()
    print("  DE&I events:")
    print("    data/dei_events.csv")
    print("    data/dei_event_summary.csv")
    print()
    print("  Executive reporting:")
    print("    reports/inclusion_executive_report.md")
    print("    reports/intervention_framework.md")
    print()


if __name__ == "__main__":
    main()