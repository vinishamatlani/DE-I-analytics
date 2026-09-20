import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

INPUT_FILE = DATA / "dei_events.csv"
OUTPUT_FILE = DATA / "dei_event_summary.csv"


def mean(values):

    values = list(values)

    if not values:
        return 0

    return sum(values) / len(values)


def main():

    with INPUT_FILE.open(
        encoding="utf-8",
    ) as fh:

        rows = list(
            csv.DictReader(fh)
        )

    total_invited = sum(
        int(r["invited"])
        for r in rows
    )

    total_attended = sum(
        int(r["attended"])
        for r in rows
    )

    attendance_rate = (
        total_attended
        / total_invited
    )

    average_gain = mean(
        float(r["knowledge_gain"])
        for r in rows
    )

    satisfaction = mean(
        float(r["satisfaction_1_5"])
        for r in rows
    )

    recommendation = mean(
        float(r["recommendation_1_5"])
        for r in rows
    )

    repeat = mean(
        float(r["repeat_participation_pct"])
        for r in rows
    )

    total_cost = sum(
        float(r["estimated_cost"])
        for r in rows
    )

    cost_per_attendee = (
        total_cost / total_attended
    )

    summary = [{
        "number_of_events": len(rows),

        "total_invited": total_invited,

        "total_attended": total_attended,

        "attendance_rate_pct": round(
            attendance_rate * 100,
            1,
        ),

        "average_knowledge_gain": round(
            average_gain,
            2,
        ),

        "average_satisfaction_1_5": round(
            satisfaction,
            2,
        ),

        "average_recommendation_1_5": round(
            recommendation,
            2,
        ),

        "repeat_participation_pct": round(
            repeat,
            1,
        ),

        "estimated_total_cost": round(
            total_cost,
            2,
        ),

        "cost_per_attendee": round(
            cost_per_attendee,
            2,
        ),
    }]

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=summary[0].keys(),
        )

        writer.writeheader()
        writer.writerows(summary)

    print()
    print("DE&I EVENT EFFECTIVENESS")
    print("------------------------")
    print("Participation, learning, experience, and cost measures")
    print(
        f"Attendance rate    : "
        f"{attendance_rate:.1%}"
    )
    print(
        f"Knowledge gain     : "
        f"{average_gain:.2f}"
    )
    print(
        f"Satisfaction       : "
        f"{satisfaction:.2f} / 5"
    )
    print(
        f"Repeat intention   : "
        f"{repeat:.1f}%"
    )
    print(
        f"Cost per attendee  : "
        f"{cost_per_attendee:.2f}"
    )

    print()
    print(
        f"Created {OUTPUT_FILE.name}"
    )


if __name__ == "__main__":
    main()