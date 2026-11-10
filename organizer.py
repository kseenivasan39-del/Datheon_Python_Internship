"""
Automated File Organizer & Cleanup Utility
Internship Project: Datheon Python Internship

Features:
- Inspects target directories (e.g. Downloads, Desktop, or custom folder).
- Extension-to-category mapping for automatic sorting (Documents, Images, Videos, Audio, Archives, Code, etc.).
- Safe file relocations using os.scandir() and shutil.move().
- Naming collision resolution (appends (1), (2), etc. rather than overwriting).
- Exception handling for PermissionError, FileExistsError, and OS errors.
- Dry-run mode to preview organization without moving actual files.
- Formatted execution summary report showing total relocated files per category.
"""

import os
import shutil
import sys
from datetime import datetime

# Category to extensions mapping dictionary
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents",
    ".docx": "Documents",
    ".doc": "Documents",
    ".txt": "Documents",
    ".pptx": "Documents",
    ".ppt": "Documents",
    ".xlsx": "Documents",
    ".xls": "Documents",
    ".csv": "Documents",
    ".epub": "Documents",
    ".rtf": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",
    ".webp": "Images",
    ".bmp": "Images",
    ".ico": "Images",
    ".tiff": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".wmv": "Videos",
    ".flv": "Videos",

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",
    ".ogg": "Audio",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",

    # Code & Developer Files
    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".json": "Code",
    ".xml": "Code",
    ".sql": "Code",
    ".sh": "Code",
    ".bat": "Code",

    # Executables & Installers
    ".exe": "Installers",
    ".msi": "Installers",
    ".dmg": "Installers",
    ".iso": "Installers"
}

# Special system files or scripts to never move
IGNORED_FILES = {
    "organizer.py",
    "hangman.py",
    "portfolio_tracker.py",
    "README.md",
    ".gitignore",
    "portfolio_data.json",
    "portfolio_performance_log.csv",
    "portfolio_summary_snapshots.csv"
}

DEFAULT_FALLBACK_FOLDER = "Others"


def resolve_naming_collision(destination_dir, filename):
    """
    Prevents file overwrites by generating a unique filename
    with an incremented suffix: e.g. report.pdf -> report (1).pdf
    """
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    destination_path = os.path.join(destination_dir, new_filename)

    while os.path.exists(destination_path):
        new_filename = f"{name} ({counter}){ext}"
        destination_path = os.path.join(destination_dir, new_filename)
        counter += 1

    return destination_path, new_filename


def organize_directory(target_path, dry_run=False):
    """
    Scans target_path and categorizes all root files into subfolders.
    Handles permissions, collisions, and errors gracefully.
    """
    if not os.path.exists(target_path):
        print(f"Error: Target path '{target_path}' does not exist.")
        return None

    if not os.path.isdir(target_path):
        print(f"Error: Path '{target_path}' is not a directory.")
        return None

    print(f"\nTarget Directory: {os.path.abspath(target_path)}")
    print(f"Mode: {'[DRY RUN - Preview Only]' if dry_run else '[LIVE EXECUTION - Moving Files]'}")
    print("-" * 65)

    stats = {
        "total_scanned": 0,
        "relocated": 0,
        "skipped": 0,
        "errors": 0,
        "by_category": {}
    }

    category_folders = set(EXTENSION_MAP.values()) | {DEFAULT_FALLBACK_FOLDER}

    try:
        with os.scandir(target_path) as entries:
            for entry in entries:
                # Skip subdirectories (especially the category folders themselves)
                if entry.is_dir():
                    continue

                stats["total_scanned"] += 1
                filename = entry.name

                # Ignore specific system/repo script files
                if filename in IGNORED_FILES or filename.startswith("."):
                    stats["skipped"] += 1
                    continue

                # Determine file extension and destination category
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                category = EXTENSION_MAP.get(ext, DEFAULT_FALLBACK_FOLDER)
                category_dir = os.path.join(target_path, category)

                # Destination path with collision safety
                target_dest_path, final_name = resolve_naming_collision(category_dir, filename)

                if dry_run:
                    print(f"[PREVIEW] {filename} --> /{category}/{final_name}")
                    stats["relocated"] += 1
                    stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
                    continue

                # Live execution: create directory and move file safely
                try:
                    os.makedirs(category_dir, exist_ok=True)
                    shutil.move(entry.path, target_dest_path)
                    print(f"[MOVED] {filename} --> /{category}/{final_name}")
                    stats["relocated"] += 1
                    stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

                except PermissionError as pe:
                    print(f"[PERMISSION DENIED] Could not move '{filename}': {pe}")
                    stats["errors"] += 1
                except FileExistsError as fe:
                    print(f"[FILE EXISTS] Collision error for '{filename}': {fe}")
                    stats["errors"] += 1
                except OSError as oe:
                    print(f"[OS ERROR] Failed moving '{filename}': {oe}")
                    stats["errors"] += 1

    except PermissionError as pe:
        print(f"Permission denied accessing folder '{target_path}': {pe}")
        return None

    return stats


def print_summary(stats, dry_run=False):
    """Prints a formatted execution summary."""
    if not stats:
        return

    print("\n" + "=" * 65)
    print("           AUTOMATED FILE ORGANIZER - EXECUTION SUMMARY")
    print("=" * 65)
    print(f"Total Files Scanned      : {stats['total_scanned']}")
    print(f"Total Files Relocated    : {stats['relocated']}")
    print(f"Total Files Skipped      : {stats['skipped']}")
    print(f"Errors Encountered       : {stats['errors']}")
    print("-" * 65)
    print("Breakdown by Category:")
    if stats["by_category"]:
        for cat, count in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
            print(f"  • /{cat:<15} : {count} file(s)")
    else:
        print("  (No files required relocation)")
    print("=" * 65)
    if dry_run:
        print("💡 This was a DRY RUN. No files were physically moved.")
    else:
        print("✓ Directory cleanup completed successfully.")


def create_demo_cluttered_folder(base_path):
    """Creates a sample cluttered folder for safe demonstration and testing."""
    demo_dir = os.path.join(base_path, "Demo_Cluttered_Folder")
    os.makedirs(demo_dir, exist_ok=True)

    sample_files = [
        "Project_Proposal.docx",
        "Quarterly_Report.pdf",
        "dataset_2026.csv",
        "vacation_photo.jpg",
        "screenshot_app.png",
        "presentation_intro.pptx",
        "demo_recording.mp4",
        "background_music.mp3",
        "project_backup.zip",
        "web_app_script.js",
        "main_algorithm.py",
        "setup_installer.exe",
        "readme_notes.txt"
    ]

    for fname in sample_files:
        sample_file_path = os.path.join(demo_dir, fname)
        if not os.path.exists(sample_file_path):
            with open(sample_file_path, "w", encoding="utf-8") as f:
                f.write(f"Sample test content for {fname}\nCreated for Datheon Python Internship demo.")

    return demo_dir


def main():
    """Main CLI interface for file organizer."""
    print("*" * 65)
    print("        AUTOMATED FILE ORGANIZER & CLEANUP UTILITY")
    print("               Datheon Python Internship")
    print("*" * 65)

    default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    print("\nSelect an option:")
    print(f"1. Organize your standard Downloads folder ({default_downloads})")
    print("2. Organize a custom directory")
    print("3. Generate and organize a sample 'Demo_Cluttered_Folder' (Recommended for test run)")
    print("4. Exit")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        target = default_downloads
    elif choice == "2":
        target = input("Enter the absolute or relative folder path: ").strip().strip('"')
    elif choice == "3":
        target = create_demo_cluttered_folder(os.getcwd())
        print(f"\n✓ Generated demo test directory at: {target}")
    elif choice == "4":
        print("Exiting utility.")
        sys.exit(0)
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Ask for dry-run
    mode = input("\nEnable Dry-Run preview first? (y/n, default 'y'): ").strip().lower()
    is_dry_run = mode not in ['n', 'no']

    stats = organize_directory(target, dry_run=is_dry_run)
    print_summary(stats, dry_run=is_dry_run)

    # If dry-run was performed, offer to execute live immediately
    if is_dry_run and stats and stats["relocated"] > 0:
        proceed = input("\nWould you like to execute the actual organization now? (y/n): ").strip().lower()
        if proceed in ['y', 'yes']:
            live_stats = organize_directory(target, dry_run=False)
            print_summary(live_stats, dry_run=False)


if __name__ == "__main__":
    main()
