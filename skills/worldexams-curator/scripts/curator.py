import json
import argparse
import sys
import os

def curate_bundle(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        sys.exit(1)

    print(f"Curating bundle: {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)

    # Simulate curation logic:
    # 1. Clean whitespace
    # 2. Ensure all fields exist
    # 3. Mark as curated

    bundle["metadata"]["curator"] = "worldexams-curator-v1"
    bundle["metadata"]["status"] = "curated"

    for q in bundle.get("questions", []):
        q["context"] = q["context"].strip()
        q["question"] = q["question"].strip()
        if "curated" not in q:
            q["curated"] = True

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    print(f"Curated bundle saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WorldExams Content Curator")
    parser.add_argument("--input", required=True, help="Path to raw bundle JSON")
    parser.add_argument("--output", default="curated_bundle.json", help="Path to save curated bundle")

    args = parser.parse_args()
    curate_bundle(args.input, args.output)
