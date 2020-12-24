# -*- coding: utf-8 -*-

from termcolor import cprint

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.


class NotEnoughValuesToUnpack(Exception):
    def __str__(self):
        return 'Недостаточно значений для распаковки'


class NotNameError(Exception):
    def __str__(self):
        return 'Ошибка в имени'


class NotEmailError(Exception):
    def __str__(self):
        return 'Ошибка потчы'

#
# class AgeError(Exception):
#     def __str__(self):
#         return 'Ошибка возраста'


class Checker:

    analyse_tuple = [False, False, False, False]

    step_bool = None

    def __init__(self):
        self.filename_origin = 'registrations.txt'
        self.filename_nice_log = 'registrations_good.txt'
        self.filename_bad_log = 'registrations_bad.txt'

    @staticmethod
    def exist_check(one, two, three):
        if one is not None and two is not None and three is not None:
            return True
        else:
            return False

    @staticmethod
    def letter_check(name):
        for letter in name:
            if letter.isalpha() is False:
                return False
            return True

    @staticmethod
    def mail_check(mail):
        mail = str(mail)
        one = '.'
        two = '@'
        if one in mail:
            if two in mail:
                return True
        return False

    @staticmethod
    def age_check(age):
        if 10 < int(age) < 99:
            return True
        else:
            return False

    @staticmethod
    def add_in_log(err, string_number, line, log):
        mess = err.__str__()
        cprint(err, color='blue')
        cprint(string_number, color='magenta')
        except_message = str(string_number) + ' ' + line[0:-1:1] + ' ' + str(err.__class__) + ' ' + str(mess) + '\n'
        log.write(except_message)

    def validation(self, name, age, mail, one, two, three):
        """метод проверяет элементы строки"""
        self.analyse_tuple[0] = self.exist_check(one=one, two=two, three=three)
        self.analyse_tuple[1] = self.letter_check(name=name)
        self.analyse_tuple[2] = self.mail_check(mail=mail)
        self.analyse_tuple[3] = self.age_check(age=age)
        if self.analyse_tuple[0] is not True:
            raise ValueError("недостаточно переменных для распаковки")
        if self.analyse_tuple[1] is False:
            raise NotNameError
        if self.analyse_tuple[2] is False:
            raise NotEmailError
        if self.analyse_tuple[3] is False:
            raise ValueError("Ошибка, возраста")

    def action(self):
        """чтение и запись в логи"""
        good_log = open(file=self.filename_nice_log, encoding='utf-8', mode='w')
        bad_log = open(file=self.filename_bad_log, encoding='utf-8', mode='w')

        with open(file='registrations.txt', encoding='utf-8', mode='r') as file:
            # стринг намбер хранит номер строки, в конце тела цикла изменяется +1
            string_number = 1
            for line in file:
                name = None
                mail = None
                age = None
                # степ бул индикатор состояния ошибки, если вылетает ошибка, состояние меняется на Тру,
                # добавил, чтобы логи ровнее писались
                self.step_bool = 0
                try:
                    name, mail, age = line.split(' ')
                    age = age[0:-1:1]
                    self.validation(name=name, mail=mail, age=age, one=name, two=mail, three=age)
                except NotEmailError as ner:
                    self.step_bool = 1
                    self.add_in_log(err=ner, string_number=string_number,
                                    line=line, log=bad_log,)
                except NotNameError as nnr:
                    self.step_bool = 1
                    self.add_in_log(err=nnr, string_number=string_number,
                                    line=line, log=bad_log,)
                except ValueError as value_err:
                    self.step_bool = 1
                    self.add_in_log(err=value_err, string_number=string_number,
                                    line=line, log=bad_log)
                else:
                    output_string = str(string_number) + ' ' + '"' + line
                    if self.analyse_tuple == [True, True, True, True]:
                        good_log.write(output_string)
                finally:
                    # Объект типа None не поддерживается методом .format
                    if name is None:
                        name = 'None'
                    if mail is None:
                        mail = 'None'
                    if age is None:
                        age = "None"
                    print('|{t1:_^5}|{t2:_^20}|{t3:_^20}|{t4:_^5}|{t6:_^10}|{t7:_^10}|{t8:_^10}|{t9:_^10}|'.format
                          (t1=string_number, t2=name, t3=mail, t4=age, t6=str(self.analyse_tuple[0]),
                           t7=str(self.analyse_tuple[1]), t8=str(self.analyse_tuple[2]), t9=str(self.analyse_tuple[3])))
                    string_number += 1
        good_log.close()
        bad_log.close()

    def go(self):
        self.action()


test = Checker()
test.go()
