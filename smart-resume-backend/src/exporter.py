import os
import json
import csv

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")

if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)

def get_json_path(export_id):
    return os.path.join(OUTPUTS_DIR, f"resume_{export_id}.json")

def get_csv_path(export_id):
    return os.path.join(OUTPUTS_DIR, f"resume_{export_id}.csv")

def save_json(data, export_id):
    with open(get_json_path(export_id), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_csv(data, export_id):
    with open(get_csv_path(export_id), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key, ", ".join(map(str, value))])
            elif isinstance(value, dict):
                writer.writerow([key, json.dumps(value)])
            else:
                writer.writerow([key, value])
