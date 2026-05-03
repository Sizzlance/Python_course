import os
import sys
import itertools


def project_stats(path, extensions):
    """
    Вернуть число строк в исходниках проекта.

    Файлами, входящими в проект, считаются все файлы
    в папке ``path`` (и подпапках), имеющие расширение
    из множества ``extensions``.
    """
    filenames = with_extensions(extensions, iter_filenames(path))
    return total_number_of_lines(filenames)


def total_number_of_lines(filenames):
    """
    Вернуть общее число строк в файлах ``filenames``.
    """
    return sum(map(number_of_lines, filenames))


def number_of_lines(filename):
    """
    Вернуть число строк в файле.
    """
    with open(filename, 'r', encoding='latin-1') as f:
        return sum(1 for _ in f)


def iter_filenames(path):
    """
    Итератор по именам файлов в дереве.
    """
    return (os.path.join(dirpath, file)
            for dirpath, _, files in os.walk(path)
            for file in files)


def with_extensions(extensions, filenames):
    """
    Оставить из итератора ``filenames`` только
    имена файлов, у которых расширение - одно из ``extensions``.
    """
    return filter(lambda f: get_extension(f) in extensions, filenames)


def get_extension(filename):
    """ Вернуть расширение файла """
    return os.path.splitext(filename)[1]

def print_usage():
    print("Usage: python project_sourse_stats_3.py <project_path>")


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_folder_name = "NSimulator"
    path = os.path.join(current_dir, project_folder_name)
    extensions = {".cs"}
    if os.path.exists(path):
        total_lines = project_stats(path, extensions)
        print(f"Путь: {path}")
        print(f"Общее количество строк: {total_lines}")
    else:
        print(f"Ошибка: Папка '{project_folder_name}' не найдена рядом со скриптом!")
