# -*- coding: utf-8 -*-
import os
import zipfile
from datetime import datetime
import shutil
# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени последней модификации файла
# Файлы для работы взять из архива icons.zip - раззиповать проводником ОС в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year
#
# Усложненное задание
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится только к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html


class Streamlining:
    """без предварительного извлечения"""
    def __init__(self):
        self.name_of_zip = 'icons.zip'
        self.name_of_unzipped_folder = 'icons'

        self.info_abt_files = {}

    def printer(self):
        for i, j in self.info_abt_files.items():
            print(i, j)

    def get_info_from_zip(self):
        # получение инфы о файлах в архиве
        with zipfile.ZipFile(self.name_of_zip, 'r') as zip_loco:
            info = zip_loco.infolist()
            len_namelist = len(zip_loco.namelist())
            for i in range(len_namelist):
                filename = info[i].filename
                date_time = info[i].date_time
                file_size = info[i].file_size
                if file_size != 0:
                    self.info_abt_files.update({filename: date_time})

    @staticmethod
    def extra(this_zip):
        with zipfile.ZipFile(this_zip) as zip_local:
            for zip_info in zip_local.infolist():
                if zip_info.filename[-1] == '/':
                    continue
                info = zip_info.date_time
                year = str(info[0])
                month = str(info[1])
                path = os.path.join(os.getcwd(), 'icons_by_year')
                this_path = os.path.join(year, month)
                destination = os.path.join(path, this_path)
                zip_info.filename = os.path.basename(zip_info.filename)
                zip_local.extract(zip_info, destination)

    def go(self):
        self.get_info_from_zip()
        self.extra(this_zip=self.name_of_zip)


class EzSortZip(Streamlining):
    folder = 'icons_by_year'
    """сортировка при предварительном извлечении архива в папку"""

    def analyse_folder(self):
        for dir_path, subdir_list, name_list in os.walk(self.name_of_unzipped_folder):
            for element in name_list:
                current_dir = os.getcwd()
                str_dir_path = str(dir_path)
                str_name_element = str(element)
                path = os.path.join(current_dir, str_dir_path)
                path_2_name = os.path.join(path, str_name_element)
                info = os.path.getmtime(path_2_name)
                info = datetime.fromtimestamp(info)
                info = str(datetime.date(info))
                year = info[0:4:1]
                month = info[5:7:1]
                day = info[8::1]
                info_path = os.path.join(self.folder, year, month, day)
                destination_path = os.path.join(current_dir, info_path)
                path_4_mkdir = r'{path}'.format(path=destination_path)
                if os.path.exists(path_4_mkdir):
                    shutil.copy2(src=path_2_name, dst=destination_path, follow_symlinks=True)
                else:
                    os.makedirs(path_4_mkdir)
                    shutil.copy2(src=path_2_name, dst=destination_path, follow_symlinks=True)

    def go(self):
        self.analyse_folder()


test_hard = Streamlining()
test_hard.go()

# test_ez = EzSortZip()
# test_ez.go()
