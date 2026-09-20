import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

OUTPUT_FILE = DATA / "dei_events.csv"

rng = random.Random(17)


EVENTS = [
    ("E001", "Inclusive Leadership Workshop", "Workshop"),
    ("E002", "Women in Leadership Forum", "Forum"),
    ("E003", "Psychological Safety Lab", "Workshop"),
    ("E004", "Global Cultural Awareness Week", "Awareness"),
    ("E005", "Employee Voice Roundtable", "Roundtable"),
    ("E006", "Inclusive Hiring Seminar", "Seminar"),
    ("E007", "Belonging at Work Panel", "Panel"),
    ("E008", "Fair Opportunity Career Session", "Career"),
]


REGIONS = [
    "APAC",
    "EMEA",
    "North America",
]


def clamp(value, low, high):

    return max(
        low,
        min(high, value),
    )


def main():

    DATA.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    for event_id, event_name, event_type in EVENTS:

        invited = rng.randint(120, 450)

        attendance_rate = clamp(
            rng.gauss(0.67, 0.10),
            0.40,
            0.90,
        )

        attended = int(
            invited * attendance_rate
        )

        no_show_rate = round(
            1 - attendance_rate,
            3,
        )

        knowledge_before = clamp(
            rng.gauss(3.0, 0.25),
            2.3,
            3.6,
        )

        knowledge_gain = clamp(
            rng.gauss(0.72, 0.18),
            0.30,
            1.20,
        )

        knowledge_after = clamp(
            knowledge_before + knowledge_gain,
            1,
            5,
        )

        satisfaction = clamp(
            rng.gauss(4.15, 0.30),
            3.2,
            4.9,
        )

        recommendation = clamp(
            rng.gauss(4.20, 0.30),
            3.2,
            4.9,
        )

        repeat_intent = clamp(
            rng.gauss(0.76, 0.08),
            0.50,
            0.95,
        )

        rows.append({
            "event_id": event_id,
            "event_name": event_name,
            "event_type": event_type,
            "region": rng.choice(REGIONS),

            "invited": invited,
            "attended": attended,

            "attendance_rate": round(
                attendance_rate,
                3,
            ),

            "no_show_rate": no_show_rate,

            "knowledge_before": round(
                knowledge_before,
                2,
            ),

            "knowledge_after": round(
                knowledge_after,
                2,
            ),

            "knowledge_gain": round(
                knowledge_after - knowledge_before,
                2,
            ),

            "satisfaction_1_5": round(
                satisfaction,
                2,
            ),

            "recommendation_1_5": round(
                recommendation,
                2,
            ),

            "repeat_participation_pct": round(
                repeat_intent * 100,
                1,
            ),

            "estimated_cost": rng.randint(
                2500,
                12000,
            ),
        })

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(rows)

    print()
    print("DE&I EVENT DATA")
    print("---------------")
    print(f"Events created : {len(rows)}")
    print(f"Created {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()