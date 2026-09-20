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

OUTCOME_ITEMS = ["inc_out_01", "inc_out_02", "inc_out_03"]

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

MIN_GROUP = 5

EXPECTED_REGION = {
    "IN": "APAC",
    "SG": "APAC",
    "DE": "EMEA",
    "PL": "EMEA",
    "US": "North America",
    "CA": "North America",
}


def read_csv(path):
    if not path.exists():
        raise AssertionError(f"Missing file: {path}")

    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"   ✓ {message}")


def check_file_structure():
    rows = read_csv(SURVEY_FILE)
    check(rows, f"{len(rows):,} invited employees found")

    required_columns = [
        "response_id",
        "responded",
        *SEGMENT_COLUMNS,
        *INCLUSION_ITEMS,
        *OUTCOME_ITEMS,
    ]
    actual_columns = set(rows[0])
    check(
        set(required_columns).issubset(actual_columns),
        "Required response, segment, inclusion, and outcome columns present",
    )

    response_ids = [row["response_id"] for row in rows]
    check(
        len(response_ids) == len(set(response_ids)),
        f"{len(set(response_ids)):,} unique response IDs",
    )
    return rows


def check_survey_values(rows):
    respondent_rows = [row for row in rows if row["responded"] == "1"]
    check(respondent_rows, f"{len(respondent_rows):,} respondents found")

    missing_items = [
        item
        for item in INCLUSION_ITEMS + OUTCOME_ITEMS
        if any(row.get(item, "") == "" for row in respondent_rows)
    ]
    check(not missing_items, "No missing inclusion or outcome values for respondents")

    invalid_items = [
        item
        for item in INCLUSION_ITEMS + OUTCOME_ITEMS
        if any(
            not 1 <= float(row[item]) <= 5
            for row in respondent_rows
        )
    ]
    check(not invalid_items, "All 15 inclusion and 3 outcome items contain valid 1-5 responses")


def check_geography(rows):
    valid_mappings = all(
        row["country"] in EXPECTED_REGION
        and row["region"] == EXPECTED_REGION[row["country"]]
        for row in rows
    )
    check(valid_mappings, "All country-region combinations are valid")


def check_scored_data():
    rows = read_csv(SCORED_FILE)
    check(rows, f"{len(rows):,} scored respondent records found")

    required_columns = {
        "response_id",
        "inclusion_index_1_5",
        "inclusion_index_0_100",
        "inclusion_outcome",
    }
    check(required_columns.issubset(rows[0]), "Scored output contains required fields")

    valid_indexes = all(0 <= float(row["inclusion_index_0_100"]) <= 100 for row in rows)
    check(valid_indexes, "Inclusion Index values fall within 0-100")


def check_dimension_summary():
    rows = read_csv(DIMENSION_FILE)
    actual_dimensions = {row["dimension"] for row in rows}
    check(len(rows) == 5 and actual_dimensions == set(DIMENSIONS), "Exactly five expected dimensions generated")

    valid_values = all(
        0 <= float(row["score_0_100"]) <= 100
        and 0 <= float(row["favourable_pct"]) <= 100
        for row in rows
    )
    check(valid_values, "Dimension scores and favourable percentages are valid")


def check_segments():
    rows = read_csv(SEGMENT_FILE)
    check(rows, f"{len(rows):,} segment records found")

    suppression_valid = all(
        (int(row["n"]) < MIN_GROUP and row["inclusion_index"] == "SUPPRESSED")
        or (int(row["n"]) >= MIN_GROUP and row["inclusion_index"] != "SUPPRESSED")
        for row in rows
    )
    check(suppression_valid, "Groups below confidentiality threshold are suppressed")


def check_associations():
    rows = read_csv(DRIVER_FILE)
    correlations = [float(row["correlation_with_inclusion_outcome"]) for row in rows]
    check(len(rows) == 5, "Association output contains five dimensions")
    check(all(-1 <= value <= 1 for value in correlations), "Pearson correlation values fall within -1 to +1")


def check_events():
    rows = read_csv(EVENT_FILE)
    check(len(rows) == 8, "Eight DE&I events found")

    valid_events = all(
        int(row["attended"]) <= int(row["invited"])
        and 0 <= float(row["attendance_rate"]) <= 1
        and 1 <= float(row["satisfaction_1_5"]) <= 5
        for row in rows
    )
    check(valid_events, "Attendance, attendance rates, and satisfaction values are valid")

    summary = read_csv(EVENT_SUMMARY_FILE)
    check(len(summary) == 1, "One aggregate event summary record found")


def main():
    print()
    print("=" * 70)
    print("GLOBAL INCLUSION & BELONGING ANALYTICS")
    print("DATA QUALITY VALIDATION")
    print("=" * 70)

    print("\n1. SURVEY STRUCTURE")
    survey_rows = check_file_structure()

    print("\n2. SURVEY ITEMS")
    check_survey_values(survey_rows)
    check_geography(survey_rows)

    print("\n3. INCLUSION SCORING")
    check_scored_data()
    check_dimension_summary()

    print("\n4. SEGMENT REPORTING")
    check_segments()

    print("\n5. ASSOCIATION ANALYSIS")
    check_associations()

    print("\n6. EVENT ANALYTICS")
    check_events()

    print("\n" + "=" * 70)
    print("RESULT: ALL VALIDATION CHECKS PASSED")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
