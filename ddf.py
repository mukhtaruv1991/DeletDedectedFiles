import os
import shutil

def delete_target_folders(root_path, target_folder_name):
    deleted_folders = []

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        if target_folder_name in dirnames:
            folder_to_delete = os.path.join(dirpath, target_folder_name)
            try:
                shutil.rmtree(folder_to_delete)
                print(f"تم حذف المجلد: {folder_to_delete}")
                deleted_folders.append(folder_to_delete)
            except Exception as e:
                print(f"فشل في حذف {folder_to_delete}: {e}")

    if not deleted_folders:
        print("لم يتم العثور على أي مجلدات للحذف.")

if __name__ == "__main__":
    root_path = input("أدخل مسار المجلد الرئيسي: ").strip()
    target_folder_name = input("أدخل اسم المجلد المراد حذفه: ").strip()

    if os.path.isdir(root_path):
        delete_target_folders(root_path, target_folder_name)
    else:
        print("المسار غير صحيح أو لا يشير إلى مجلد.")
