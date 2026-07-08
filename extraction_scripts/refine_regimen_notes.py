import os
import re
from striprtf.striprtf import rtf_to_text

def refine_and_standardize_rtf_notes(output_dir="."):
    """
    Dynamically loads the RTF notes file from the active project root directory,
    strips hidden rich text syntax, and formats a clean Markdown master document.
    Incorporates strict surrogate unicode error handling bypass protocols.
    """
    input_file = "narcolepsy_notes_daily_regime.rtf"
    
    if not os.path.exists(input_file):
        print(f"Error: Target RTF notes file missing at current directory path: {os.path.abspath(input_file)}")
        return

    print(f"Opening and decoding RTF structure from local root: {input_file}...")
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            raw_rtf_content = f.read()
            
        # Programmatically strip out the hidden RTF layout styling syntax
        raw_text = rtf_to_text(raw_rtf_content)
    except Exception as e:
        print(f"Failed to cleanly decode RTF envelope tags: {e}")
        return

    print("Sanitizing text fragments and normalizing chemical variations...")
    # Processing Logic: Perform structural text cleansing operations
    refined_text = raw_text.replace("\t", "    ")
    refined_text = re.sub(r'(?i)vit\s*c', 'Vitamin C', refined_text)
    refined_text = re.sub(r'(?i)vit\s*d', 'Vitamin D', refined_text)
    refined_text = re.sub(r'(?i)vit\s*e', 'Vitamin E', refined_text)
    refined_text = re.sub(r'(?i)cl\s*o2', 'Chlorine Dioxide (ClO2)', refined_text)
    refined_text = re.sub(r'\b(dmso|edta|maoi|atp|mods)\b', lambda m: m.group(1).upper(), refined_text)
    
    # Ensure vertical header spaces are clean and properly padded
    refined_text = re.sub(r'\n{3,}', '\n\n', refined_text)

    # Append standard semantic master structural outline tracking headers
    master_header = """# Master Document: Optimized Neuro-Immunological Protocol for Severe Narcolepsy Type 1
    
> *Heuristic Self-Experimentation Registry and Optimization Logs*
> **Current Baseline Configuration Status**: Modafinil requirement successfully reduced from 400mg to 100mg/day.

---

## Core Operational Logs & Collected Text Assets
"""
    
    final_output_content = master_header + "\n" + refined_text

    # Write out the completed master documentation tracking sheet to your active repo
    output_file_name = "NARCOLEPSY_DAILY_REGIMEN_MASTER.md"
    output_path = os.path.join(output_dir, output_file_name)
    
    # CRITICAL ENHANCEMENT: Added errors="replace" to bypass surrogate character halts safely
    with open(output_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(final_output_content)
        
    print(f"\nRefinement processing loop complete!")
    print(f"Master markdown document cleanly generated at: {output_path}")

if __name__ == "__main__":
    refine_and_standardize_rtf_notes()
