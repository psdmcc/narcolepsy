import os
import re
from striprtf.striprtf import rtf_to_text

def refine_longitudinal_outline_rtf(output_dir="."):
    """
    Dynamically loads the longitudinal study outline RTF document, 
    strips hidden layout tags, sanitizes text syntax, and outputs a 
    standardized master Markdown file for GitHub tracking.
    """
    input_file = "longitudinal_study_outline.rtf"
    
    if not os.path.exists(input_file):
        print(f"Error: Target RTF study outline file missing at: {os.path.abspath(input_file)}")
        print("Please verify the exact file placement inside your narcolepsy-pipeline workspace.")
        return

    print(f"Opening and decoding RTF structure from local repository root: {input_file}...")
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            raw_rtf_content = f.read()
            
        # Programmatically strip away the hidden rich-text formatting tags
        raw_text = rtf_to_text(raw_rtf_content)
    except Exception as e:
        print(f"Failed to cleanly decode RTF envelope tags: {e}")
        return

    print("Sanitizing text fragments and normalizing chemical variations...")
    # Core Processing Logic: Sanitize string parameters and expand abbreviated text components
    refined_text = raw_text.replace("\t", "    ")
    refined_text = re.sub(r'(?i)vit\s*c', 'Vitamin C', refined_text)
    refined_text = re.sub(r'(?i)vit\s*d', 'Vitamin D', refined_text)
    refined_text = re.sub(r'(?i)vit\s*e', 'Vitamin E', refined_text)
    refined_text = re.sub(r'(?i)cl\s*o2', 'Chlorine Dioxide (ClO2)', refined_text)
    refined_text = re.sub(r'\b(dmso|edta|maoi|atp|mods)\b', lambda m: m.group(1).upper(), refined_text)
    
    # Ensure all structural vertical header margins are padded and clean
    refined_text = re.sub(r'\n{3,}', '\n\n', refined_text)

    # Prepend formal academic master project structural headers
    master_header = """# Institutional Protocol Blueprint: Longitudinal N-of-1 Case Study Optimization Metrics
    
> *Subject Operational Blueprint for Peer-Reviewed Medical Journal Submission Tracking*
> **Principal Investigator / Patient Model**: Patrick S.D. McCartney
> **Affiliation Mapping Resource**: Graduate School of Humanities and Social Sciences, Hiroshima University

---
"""
    
    final_output_content = master_header + "\n" + refined_text

    # Write out the completed, pristine master document to your directory root
    output_file_name = "NARCOLEPSY_LONGITUDINAL_STUDY_OUTLINE.md"
    output_path = os.path.join(output_dir, output_file_name)
    
    # Enforce clear surrogate error handling protection flags to guarantee clean file compilation
    with open(output_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(final_output_content)
        
    print(f"\nRefinement processing complete!")
    print(f"Master longitudinal study markdown file cleanly generated at: {output_path}")

if __name__ == "__main__":
    refine_longitudinal_outline_rtf()
