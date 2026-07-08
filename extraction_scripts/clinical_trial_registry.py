import os
import csv
from datetime import datetime

def run_clinical_trial_registry(output_dir="data_payloads"):
    """
    Automates data collection for an N-of-1 self-experimentation case study,
    formatting entries cleanly to prepare for medical journal submission.
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "clinical_trial_registry.csv")
    
    # Establish standard clinical columns
    headers = [
        "Date", "Study_Phase", "Modafinil_Dose_mg", "Stanford_Sleepiness_Scale_Avg",
        "Sleep_Attacks_Count", "Nocturnal_Sleep_Quality_1to10", "Adverse_Events_Logged", "Notes"
    ]
    
    file_exists = os.path.exists(csv_path)
    
    print("=== CLINICAL TRIAL REGISTRY: N-OF-1 NARCOLEPSY PROJECT ===")
    print("Record your daily empirical metrics below:\n")
    
    # Gather your clinical parameters via terminal prompts
    phase = input("Current Study Phase (e.g., Baseline, EDTA-Washout, Maintenance): ") or "Baseline"
    modafinil = input("Modafinil Dose (mg) [e.g., 100]: ") or "100"
    sss_score = input("Stanford Sleepiness Scale Daily Average (1=Fully Active, 7=Severe Sleepiness): ") or "1"
    attacks = input("Daytime REM Intrusions / Sleep Attacks [Count]: ") or "0"
    sleep_quality = input("Nocturnal Sleep Consolidation Score [1-10]: ") or "10"
    adverse = input("Adverse Events Logged (e.g., skin rash, heart palpitations, None): ") or "None"
    notes = input("Daily observations: ") or "Protocol parameters stable."
    
    row_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Study_Phase": phase,
        "Modafinil_Dose_mg": modafinil,
        "Stanford_Sleepiness_Scale_Avg": sss_score,
        "Sleep_Attacks_Count": attacks,
        "Nocturnal_Sleep_Quality_1to10": sleep_quality,
        "Adverse_Events_Logged": adverse,
        "Notes": notes
    }
    
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)
        
    print(f"\nSuccess! Entry appended cleanly to your clinical database.")
    print(f"File Location: {csv_path}")

if __name__ == "__main__":
    run_clinical_trial_registry()
