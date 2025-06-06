import os
import shutil
import threading
import itertools
import sys
import time

stop_spinner = False

def spinner(text):
    for c in itertools.cycle(['.', '..', '...']):
        if stop_spinner:
            break
        sys.stdout.write(f'\r{text}{c}   ')
        sys.stdout.flush()
        time.sleep(0.4)

def find_target_folders(root_path, target_folder_name):
    global stop_spinner
    stop_spinner = False
    spinner_thread = threading.Thread(target=spinner, args=("Searching",))
    spinner_thread.start()

    target_folders = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        if target_folder_name in dirnames:
            folder_path = os.path.join(dirpath, target_folder_name)
            target_folders.append(folder_path)

    stop_spinner = True
    spinner_thread.join()
    print(f"\rFound {len(target_folders)} folder(s) named '{target_folder_name}'.{' ' * 20}")
    return target_folders

def delete_folder_with_progress(folder_path):
    global stop_spinner
    stop_spinner = False
    spinner_thread = threading.Thread(target=spinner, args=(f"Deleting {folder_path}",))
    spinner_thread.start()

    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)
                except Exception:
                    pass
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                except Exception:
                    pass
        os.rmdir(folder_path)
        success = True
    except Exception:
        success = False

    stop_spinner = True
    spinner_thread.join()
    status = "✔️" if success else "❌"
    print(f"\r{status} Deleted: {folder_path}{' ' * 20}")
    return success

def delete_target_folders_with_progress(root_path, target_folder_name):
    target_folders = find_target_folders(root_path, target_folder_name)

    total = len(target_folders)
    if total == 0:
        print("No folders found to delete.")
        return

    deleted_count = 0
    for idx, folder in enumerate(target_folders, 1):
        print(f"[{idx}/{total}] Processing...")
        success = delete_folder_with_progress(folder)
        if success:
            deleted_count += 1
        progress = (idx / total) * 100
        print(f"Progress: {progress:.2f}%\n")

    print(f"✅ Done. Successfully deleted {deleted_count} out of {total} folders.")

if __name__ == "__main__":
    root_path = input("Enter the root folder path: ").strip()
    target_folder_name = input("Enter the name of the folder to delete: ").strip()

    if os.path.isdir(root_path):
        delete_target_folders_with_progress(root_path, target_folder_name)
    else:
        print("❌ The path is not valid or not a directory.")
