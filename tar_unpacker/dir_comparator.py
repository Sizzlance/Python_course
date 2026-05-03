import os
import filecmp
import hashlib


def hash_file(filepath):
    """Возвращает хэш файла для проверки содержимого."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def compare_folders(folder1, folder2):
    """Сравнивает две папки на одинаковость файлов."""
    # Получаем списки всех файлов и подкаталогов в обеих папках
    files1 = set(os.path.relpath(os.path.join(dp, f), folder1)
                 for dp, dn, filenames in os.walk(folder1) for f in filenames)
    files2 = set(os.path.relpath(os.path.join(dp, f), folder2)
                 for dp, dn, filenames in os.walk(folder2) for f in filenames)

    # Получаем файлы, которые присутствуют только в одной из папок
    only_in_folder1 = files1 - files2
    only_in_folder2 = files2 - files1

    # Печатаем отсутствующие файлы
    if only_in_folder1:
        print(f"Файлы только в {folder1}:")
        print("\n".join(only_in_folder1))
    if only_in_folder2:
        print(f"Файлы только в {folder2}:")
        print("\n".join(only_in_folder2))

    # Проверяем содержимое общих файлов
    common_files = files1 & files2
    for file in common_files:
        path1 = os.path.join(folder1, file)
        path2 = os.path.join(folder2, file)
        if hash_file(path1) != hash_file(path2):
            print(f"Файл {file} отличается содержимым!")

    # Итоговая проверка
    if not only_in_folder1 and not only_in_folder2 and all(
            hash_file(os.path.join(folder1, f)) == hash_file(os.path.join(folder2, f)) for f in common_files):
        print("Папки идентичны!")
    else:
        print("Папки различаются.")


# Пример использования
folder1 = "qwer"
folder2 = "NSimulator"
compare_folders(folder1, folder2)
