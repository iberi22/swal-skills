import json
import argparse
import sys
import os

def validate_bundle(input_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return False

    print(f"Validating bundle: {input_file}...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            bundle = json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return False

    errors = []

    # 1. Check Metadata
    metadata = bundle.get("metadata", {})
    if not metadata.get("grade") or not metadata.get("subject"):
        errors.append("Missing metadata: grade or subject.")

    # 2. Check Questions
    questions = bundle.get("questions", [])
    if not questions:
        errors.append("No questions found in bundle.")

    for i, q in enumerate(questions):
        q_id = q.get("id", f"index_{i}")

        if not q.get("context") or len(q.get("context")) < 10:
            errors.append(f"Question {q_id}: Context too short or missing.")

        if not q.get("question"):
            errors.append(f"Question {q_id}: Missing question text.")

        options = q.get("options", [])
        if len(options) != 4:
            errors.append(f"Question {q_id}: Must have exactly 4 options.")

        answer = q.get("answer")
        if not isinstance(answer, int) or answer < 0 or answer >= len(options):
            errors.append(f"Question {q_id}: Invalid answer index ({answer}).")

        if not q.get("explanation"):
            errors.append(f"Question {q_id}: Missing explanation.")

    if errors:
        print("\nValidation FAILED:")
        for err in errors:
            print(f"- {err}")
        return False
    else:
        print("\nValidation successful: Bundle is ready for deployment.")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WorldExams Bundle Validator")
    parser.add_argument("--input", required=True, help="Path to curated bundle JSON")

    args = parser.parse_args()
    success = validate_bundle(args.input)

    if not success:
        sys.exit(1)
    sys.exit(0)
