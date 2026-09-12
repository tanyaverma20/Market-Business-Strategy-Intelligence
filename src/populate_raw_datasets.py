"""Deprecated legacy generator retained only for traceability.

It previously manufactured proxy registration and state data while calling it
official. It is intentionally disabled. Save documented source exports in
data/raw/, update DATASET_MANIFEST.csv, then run data_processing.py instead.
"""
if __name__ == "__main__":
    raise SystemExit("Disabled: this legacy generator would create non-observed proxy data.")
