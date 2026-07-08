import os
import shutil

def consolidate_external_folders():
    """
    Crawls through the two desktop narcolepsy directories on this Mac, pulls all 
    collected articles, and consolidates them into the active project directory.
    """
    # Exact pre-configured macOS absolute path strings for your directories
    old_folder_1 = "/Users/croma/desktop/everything/1 non-academic/narcolepsy"
    old_folder_2 = "/Users/croma/desktop/everything/1 non-academic/covid/black cumin/narcolepsy"
    
    # Active local project destination directory paths
    destination_dir = "data_payloads/consolidated_articles"
    os.makedirs(destination_dir, exist_ok=True)
    
    sources = [old_folder_1, old_folder_2]
    file_count = 0
    clash_count = 0

    print("Initializing structural data consolidation loop across hard drive paths...\n")

    for src_dir in sources:
        if not os.path.exists(src_dir):
            print(f"Warning: Pathway does not exist or volume unmounted, skipping:\n -> {src_dir}")
            continue
            
        print(f"Scanning target path: {src_dir}")
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                # Skip hidden system metadata artifacts (like macOS .DS_Store files)
                if file.startswith("."):
                    continue
                    
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_dir, file)
                
                # Prevent accidental file overwriting if duplicate names exist across folders
                if os.path.exists(destination_file_path):
                    name, ext = os.path.splitext(file)
                    destination_file_path = os.path.join(destination_dir, f"{name}_duplicate_{file_count}{ext}")
                    clash_count += 1
                
                try:
                    shutil.copy2(source_file_path, destination_file_path)
                    file_count += 1
                except Exception as e:
                    print(f"    Failed to copy asset {file}. Error: {e}")

    print(f"\n=== CONSOLIDATION COMPLETION METRICS ===")
    print(f"* Total assets copied into active repository track: {file_count}")
    print(f"* Duplicate name clashes safely resolved: {clash_count}")
    print(f"* Destination folder local path: {destination_dir}")

if __name__ == "__main__":
    consolidate_external_folders()
