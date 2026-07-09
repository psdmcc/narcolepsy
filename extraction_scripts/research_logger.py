import os
import csv
from datetime import datetime

def log_daily_research_metrics(output_dir="data_payloads"):
    """
    Automates local daily data entry for an empirical N-of-1 narcolepsy research project,
    exporting data directly to a structured CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "patient_metrics_log.csv")
    
    # Define the permanent structural columns for your clinical spreadsheet
    headers = [
        "Date", "Modafinil_Dose_mg", "Symptom_Vibe_1to10", 
        "Daytime_Sleep_Attacks", "Sleep_Quality_1to10", "Notes_Observations"
    ]
    
    # Initialize the spreadsheet file with headers if it doesn't exist yet
    file_exists = os.path.exists(csv_path)
    
    print("=== N-of-1 BIOMEDICAL RESEARCH LOGGER ===")
    print("Enter your daily empirical metrics below:\n")
    
    # 1. Gather your objective and subjective tracking points via terminal prompts
    modafinil = input("Current Modafinil Daily Dose (mg) [e.g., 100]: ") or "100"
    vibe_score = input("Daytime Alertness Vibe Score (1=Severe Sleepiness, 10=Perfect Awake) [1-10]: ") or "10"
    sleep_attacks = input("Number of Daytime Sleep Attacks/REM Intrusions Today [Count]: ") or "0"
    sleep_quality = input("Nocturnal Sleep Quality Score (1=Very Fragmented, 10=Deep/Consolidated) [1-10]: ") or "10"
    notes = input("Targeted observations (e.g., skipped EDTA, shifted topical window): ") or "Baseline protocol stable."
    
    row_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Modafinil_Dose_mg": modafinil,
        "Symptom_Vibe_1to10": vibe_score,
        "Daytime_Sleep_Attacks": sleep_attacks,
        "Sleep_Quality_1to10": sleep_quality,
        "Notes_Observations": notes
    }
    
    # 2. Append the data entry cleanly to your permanent hard drive file
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)
        
    print(f"\nSuccess! Metrics logged cleanly to your research database.")
    print(f"File Location: {csv_path}")

if __name__ == "__main__":
    log_daily_research_metrics()
