# -*- coding: utf-8 -*-

import zipfile
import collections
import operator

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# | буква | частота |
# +---------+----------+
# | А | 77777 |
# | Б | 55555 |
# | ... | ..... |
# | a | 33333 |
# | б | 11111 |
# | ... | ..... |
# +---------+----------+
# | итого | 9999999 |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
# см https://refactoring.guru/ru/design-patterns/template-..
# и https://gitlab.skillbox.ru/vadim_shandrinov/python_ba..


# родительский класс - по частоте - по убыванию
class AbcParsePapa:
    # настройка сортировки
    sort_blank_tuning_bull = True
    sort_blank_tuning_int_index = 1
    printer_logo = 'по частоте - по убыванию'

    def __init__(self):
        # имя архива и целевой папки
        self.zip_dir_name = 'python_snippets/voyna-i-mir.txt.zip'
        self.txt_name = 'voyna-i-mir.txt'

        # подсчет символов
        self.total_quantity_letters = 0
        self.collector = collections.defaultdict(int)

        # результаты чтения и сортировки
        self.raw_data = []
        self.sorted_jigging_result = []

    def printer(self):
        print('+{txt:-^51}+'.format(txt='+'))
        print('|{txt:^51}|'.format(txt=self.printer_logo))
        print('+{txt:-^51}+'.format(txt='+'))
        print('+{txt: ^51}+'.format(txt='всего ' + str(self.total_quantity_letters) + ' символов'))
        print('+{txt:-^51}+'.format(txt='+'))
        print('|{txt:^25}|{txt_1:^25}|'.format(txt='Символ', txt_1='Кол-во'))
        print('+{txt:-^51}+'.format(txt='+'))
        for key, value in self.sorted_jigging_result:
            print('|{txt:^25}|{txt_1:^25}|'.format(txt=key, txt_1=value))
            print('+{txt:-^51}+'.format(txt='+'))

    def smart_open(self):
        with zipfile.ZipFile(self.zip_dir_name, 'r') as loco_zip:
            with loco_zip.open(self.txt_name, 'r') as file:
                for line in file:
                    result = line.decode('cp1251')
                    for symbol in result:
                        if symbol.isalpha():
                            self.total_quantity_letters += 1
                            self.collector[symbol] += 1
                        else:
                            pass

        return list(self.collector.items())

    def sort_blank(self, object_loco):
        sorted_jigging_result = sorted(object_loco,
                                       key=operator.itemgetter(self.sort_blank_tuning_int_index),
                                       reverse=self.sort_blank_tuning_bull)
        return sorted_jigging_result

    def go(self):
        self.raw_data = self.smart_open()
        self.sorted_jigging_result = self.sort_blank(object_loco=self.raw_data)
        self.printer()


# - по частоте по возрастанию
class SortFrequencyIncrease(AbcParsePapa):
    sort_blank_tuning_bull = False
    printer_logo = 'По частоте, по возрастанию'


# - по алфавиту по возрастанию
class SortAbcIncrease(AbcParsePapa):
    sort_blank_tuning_bull = False
    sort_blank_tuning_int_index = 1
    printer_logo = 'По алфавиту, по возрастанию'


# - по алфавиту по убыванию
class SortAbcDecrease(AbcParsePapa):
    sort_blank_tuning_int_index = 1
    printer_logo = 'По алфавиту, по убыванию'


sort_1 = SortFrequencyIncrease()
sort_1.go()

sort_2 = SortAbcIncrease()
sort_2.go()

sort_3 = SortAbcDecrease()
sort_3.go()

sort_4 = AbcParsePapa()
sort_4.go()
