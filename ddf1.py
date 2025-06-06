import os
import shutil
import time

def find_target_folders(root_path, target_folder_name):
    target_folders = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        if target_folder_name in dirnames:
            folder_path = os.path.join(dirpath, target_folder_name)
            target_folders.append(folder_path)

    return target_folders

def delete_folder_with_progress(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete file {file_path}: {e}")

        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
                print(f"Deleted folder: {dir_path}")
            except Exception as e:
                print(f"Failed to delete folder {dir_path}: {e}")

    try:
        os.rmdir(folder_path)
        print(f"Deleted main folder: {folder_path}")
        return True
    except Exception as e:
        print(f"Failed to delete main folder {folder_path}: {e}")
        return False

def delete_target_folders_with_progress(root_path, target_folder_name):
    print("Searching for target folders...")
    target_folders = find_target_folders(root_path, target_folder_name)

    total = len(target_folders)
    if total == 0:
        print("No folders found to delete.")
        return

    print(f"Found {total} folder(s) named '{target_folder_name}'.")

    deleted_count = 0
    for idx, folder in enumerate(target_folders, 1):
        print(f"\n[{idx}/{total}] Deleting: {folder}")
        success = delete_folder_with_progress(folder)
        if success:
            deleted_count += 1
        progress = (idx / total) * 100
        print(f"Progress: {progress:.2f}%")

    print(f"\nDone. Successfully deleted {deleted_count} out of {total} folders.")

if __name__ == "__main__":
    root_path = input("Enter the root folder path: ").strip()
    target_folder_name = input("Enter the name of the folder to delete: ").strip()

    if os.path.isdir(root_path):
        delete_target_folders_with_progress(root_path, target_folder_name)
    else:
        print("The path is not valid or not a directory.")
