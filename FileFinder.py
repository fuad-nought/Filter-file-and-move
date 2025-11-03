import os
import shutil
from pathlib import Path

def extract_files_by_extension(parent_folder, extension, output_folder=None):
    """
    Extract all files with a specific extension from parent folder and its subfolders.
    
    Args:
        parent_folder: Path to the parent folder containing subfolders
        extension: File extension to search for (e.g., '.ipt' or 'ipt')
        output_folder: Optional destination folder. If None, files are moved to parent folder
    """
    # Ensure extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Convert to Path object
    parent_path = Path(parent_folder)
    
    # Validate parent folder exists
    if not parent_path.exists():
        print(f"Error: Parent folder '{parent_folder}' does not exist!")
        return
    
    # Set output folder (default to parent folder if not specified)
    if output_folder is None:
        output_path = parent_path
    else:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all files with the specified extension
    found_files = list(parent_path.rglob(f"*{extension}"))
    
    if not found_files:
        print(f"No files with extension '{extension}' found in '{parent_folder}'")
        return
    
    print(f"Found {len(found_files)} file(s) with extension '{extension}'")
    print("\nMoving files...")
    
    moved_count = 0
    for file_path in found_files:
        # Skip if file is already in the output folder
        if file_path.parent == output_path:
            print(f"  Skipped (already in destination): {file_path.name}")
            continue
        
        # Handle duplicate filenames
        destination = output_path / file_path.name
        if destination.exists():
            # Add number suffix if file already exists
            base_name = file_path.stem
            counter = 1
            while destination.exists():
                new_name = f"{base_name}_{counter}{extension}"
                destination = output_path / new_name
                counter += 1
        
        # Move the file
        try:
            shutil.move(str(file_path), str(destination))
            print(f"  Moved: {file_path.name} -> {destination}")
            moved_count += 1
        except Exception as e:
            print(f"  Error moving {file_path.name}: {e}")
    
    print(f"\nCompleted! Moved {moved_count} file(s) to '{output_path}'")

if __name__ == "__main__":
    # Get user input
    parent_folder = input("Enter the parent folder path: ").strip()
    extension = input("Enter the file extension (e.g., .ipt or ipt): ").strip()
    
    # Optional: ask if user wants a different output location
    use_custom_output = input("Move files to a different folder? (y/n): ").strip().lower()
    
    if use_custom_output == 'y':
        output_folder = input("Enter output folder path: ").strip()
    else:
        output_folder = None
        print(f"Files will be moved to the parent folder: {parent_folder}")
    
    # Execute the extraction
    print("\n" + "="*50)
    extract_files_by_extension(parent_folder, extension, output_folder)
    print("="*50)