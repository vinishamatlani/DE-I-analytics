import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


SURVEY_FILE = DATA / "survey_responses.csv"
SCORED_FILE = DATA / "inclusion_scored.csv"
DIMENSION_FILE = DATA / "inclusion_dimension_summary.csv"
SEGMENT_FILE = DATA / "inclusion_segment_summary.csv"
DRIVER_FILE = DATA / "inclusion_driver_summary.csv"
EVENT_FILE = DATA / "dei_events.csv"
EVENT_SUMMARY_FILE = DATA / "dei_event_summary.csv"


INCLUSION_ITEMS = [
    "bel_01", "bel_02", "bel_03",
    "voi_01", "voi_02", "voi_03",
    "psy_01", "psy_02", "psy_03",
    "fair_01", "fair_02", "fair_03",
    "ldr_01", "ldr_02", "ldr_03",
]


DIMENSIONS = [
    "Belonging",
    "Employee Voice",
    "Psychological Safety",
    "Fairness & Opportunity",
    "Inclusive Leadership",
]


SEGMENT_COLUMNS = [
    "region",
    "gender_group",
    "age_band",
    "department",
    "job_level",
    "tenure_band",
    "work_model",
]


def read_csv(path):
    if not path.exists():
        raise AssertionError(f"Missing file: {path}")

    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check(condition, message):
    if not condition:
        raise AssertionError(message)

    print(f"✓ {message}")


def check_file_structure():
    rows = read_csv(SURVEY_FILE)

    check(
        len(rows) > 0,
        "Survey file contains data",
    )

    required_columns = [
        "response_id",
        "responded",
        "region",
        "gender_group",
        "age_band",
        "department",
        "job_level",
        "tenure_band",
        "work_model",
    ]

    for column in required_columns:
        check(
            column in rows[0],
            f"Survey contains '{column}'",
        )

    for item in INCLUSION_ITEMS:
        check(
            item in rows[0],
            f"Survey contains '{item}'",
        )

    return rows


def check_survey_values(rows):
    respondent_rows = [
        row for row in rows
        if row["responded"] == "1"
    ]

    check(
        len(respondent_rows) > 0,
        f"{len(respondent_rows):,} respondents found",
    )

    response_ids = [
        row["response_id"]
        for row in rows
    ]

    check(
        len(response_ids) == len(set(response_ids)),
        "No duplicate response IDs",
    )

    for row in respondent_rows:
        for item in INCLUSION_ITEMS:
            value = row.get(item, "")

            check(
                value != "",
                f"{item} has no missing respondent values",
            )

            numeric_value = float(value)

            check(
                1 <= numeric_value <= 5,
                f"{item} contains valid Likert values",
            )


def check_scored_data():
    rows = read_csv(SCORED_FILE)

    check(
        len(rows) > 0,
        "Scored inclusion file contains data",
    )

    required_columns = [
        "response_id",
        "inclusion_index_1_5",
        "inclusion_index_0_100",
        "inclusion_outcome",
    ]

    for column in required_columns:
        check(
            column in rows[0],
            f"Scored data contains '{column}'",
        )

    for row in rows:
        index = float(row["inclusion_index_0_100"])

        check(
            0 <= index <= 100,
            "Inclusion Index values are within 0–100",
        )


def check_dimension_summary():
    rows = read_csv(DIMENSION_FILE)

    check(
        len(rows) == 5,
        "Exactly five inclusion dimensions found",
    )

    actual_dimensions = {
        row["dimension"]
        for row in rows
    }

    check(
        actual_dimensions == set(DIMENSIONS),
        "All five expected dimensions are present",
    )

    for row in rows:
        score = float(row["score_0_100"])
        favourable = float(row["favourable_pct"])

        check(
            0 <= score <= 100,
            f"{row['dimension']} score is valid",
        )

        check(
            0 <= favourable <= 100,
            f"{row['dimension']} favourable percentage is valid",
        )


def check_segments():
    rows = read_csv(SEGMENT_FILE)

    check(
        len(rows) > 0,
        "Segment summary contains data",
    )

    for row in rows:
        n = int(row["n"])

        if n < 5:
            check(
                row["inclusion_index"] == "SUPPRESSED",
                f"{row['segment']} is suppressed below threshold",
            )

        else:
            check(
                row["inclusion_index"] != "SUPPRESSED",
                f"{row['segment']} is visible at n >= 5",
            )


def check_drivers():
    rows = read_csv(DRIVER_FILE)

    check(
        len(rows) == 5,
        "Driver analysis contains five dimensions",
    )

    for row in rows:
        correlation = float(
            row["correlation_with_inclusion_outcome"]
        )

        check(
            -1 <= correlation <= 1,
            f"{row['dimension']} correlation is valid",
        )


def check_events():
    rows = read_csv(EVENT_FILE)

    check(
        len(rows) == 8,
        "Exactly eight DE&I events found",
    )

    for row in rows:
        invited = int(row["invited"])
        attended = int(row["attended"])
        attendance_rate = float(row["attendance_rate"])
        satisfaction = float(row["satisfaction_1_5"])

        check(
            attended <= invited,
            f"{row['event_name']} attendance does not exceed invitations",
        )

        check(
            0 <= attendance_rate <= 1,
            f"{row['event_name']} attendance rate is valid",
        )

        check(
            1 <= satisfaction <= 5,
            f"{row['event_name']} satisfaction is valid",
        )

    summary = read_csv(EVENT_SUMMARY_FILE)

    check(
        len(summary) == 1,
        "Event summary contains one aggregate record",
    )


def main():
    print()
    print("=" * 70)
    print("GLOBAL INCLUSION & BELONGING ANALYTICS")
    print("DATA QUALITY VALIDATION")
    print("=" * 70)

    print()
    print("1. SURVEY STRUCTURE")
    print("--------------------")
    survey_rows = check_file_structure()

    print()
    print("2. SURVEY VALUES")
    print("-----------------")
    check_survey_values(survey_rows)

    print()
    print("3. SCORED DATA")
    print("---------------")
    check_scored_data()

    print()
    print("4. DIMENSION SUMMARY")
    print("--------------------")
    check_dimension_summary()

    print()
    print("5. SEGMENT ANALYSIS")
    print("-------------------")
    check_segments()

    print()
    print("6. DRIVER ANALYSIS")
    print("------------------")
    check_drivers()

    print()
    print("7. DE&I EVENT DATA")
    print("------------------")
    check_events()

    print()
    print("=" * 70)
    print("RESULT: ALL DATA QUALITY CHECKS PASSED")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()