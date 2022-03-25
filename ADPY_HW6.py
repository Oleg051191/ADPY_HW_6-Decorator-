import logging
from os import path
import os
import datetime


def my_decor(log_folder, log_size):
    def _my_decor(old_func):
        def new_func(a, b, c):
            if log_folder not in os.listdir(os.getcwd()):
                os.mkdir(log_folder)
            path = os.getcwd() + f"\\{log_folder}"
            l = os.path.join(path, f'app_{0}.log')
            if f'app_{0}_{datetime.date.today()}.log' in os.listdir(path):
                for id, log in enumerate(os.listdir(path)):
                    size = os.path.getsize(os.path.join(path, log))
                    if size > log_size:
                        continue
                    else:
                        result = old_func(a, b, c)
                        logging.basicConfig(format='%(message)s\nВремя и дата вызова - %(asctime)s',
                                            level=logging.INFO,
                                            datefmt='%A %d %B %Y, %H:%M:%S',
                                            filename=os.path.join(path, f'app_{id}_{datetime.date.today()}.log'), encoding='utf-8-sig')
                        logging.info(f'Вызвана функция "{old_func.__name__}" c аргументами {a, b, c}\n'
                                     f'Результат выполнения - {result}')
                        break
                else:
                    log_n = id+1
                    result = old_func(a, b, c)
                    logging.basicConfig(format='%(message)s\nВремя и дата вызова - %(asctime)s', level=logging.INFO,
                                        datefmt='%A %d %B %Y, %H:%M:%S',
                                        filename=os.path.join(path, f'app_{log_n}_{datetime.date.today()}.log'), encoding='utf-8-sig')
                    logging.info(f'Вызвана функция "{old_func.__name__}" c аргументами {a, b, c}\n'
                                 f'Результат выполнения - {result}')
                    with open(os.path.join(path, f"app_{id}_{datetime.date.today()}.log"), 'a', encoding='utf-8-sig') as file:
                        massage = f"""\t\t\t\t*****Размер лог-файла превышает {log_size} байт ****** 
                        Запись произведена в 'app_{log_n}_{datetime.date.today()}'"""
                        file.write(massage)
            else:
                result = old_func(a, b, c)
                logging.basicConfig(format='%(message)s\nВремя и дата вызова - %(asctime)s', level=logging.INFO,
                                    datefmt='%A %d %B %Y, %H:%M:%S',
                                    filename=os.path.join(path, f'app_{0}_{datetime.date.today()}.log'), encoding='utf-8-sig')
                logging.info(f'\t\t\t*****Первый лог-файл для вызваной функции******\n'
                             f'Вызвана функция "{old_func.__name__}" c аргументами {a, b, c}\n'
                             f'Результат выполнения - {result}')
            return result
        return new_func
    return _my_decor
"""Декоратор, принимающий на вход Имя папки для лог-файлов и размер лог-файла.
В случае превышения заданного пользователем размера лог-файла, создается новый лог-файл
с последующим порядковым номером, в предыдущем лог-файле выводится соответствующее сообщение"""
@my_decor('Log_folder', 300)
def get_summ(a, b, c):
    return a + b + c

if __name__ == '__main__':
    get_summ(1, 2, 10)

