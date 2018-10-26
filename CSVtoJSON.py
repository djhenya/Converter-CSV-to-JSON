# -*- coding: UTF-8 -*-
# python 2.7

import csv
import json
from collections import OrderedDict


class Converter():
    def __init__(self, csv_files, json_file):
        '''
        Конструктор класса. Вызывает метод чтения файлов csv несколько раз, в зависимости от их количества.
        Далее вызывает метод записи данных в файл json.
        '''
        self.row_dicts = []
        self.users_dict = OrderedDict({})
        self.iterator = 0
        for i in range(len(csv_files)):
            self.from_csv_reader(csv_files[i])
        self.to_json_writer(json_file)

    def from_csv_reader(self, csv_file):
        '''
        Считывает и обрабатывает для последующей записи в файл json данные из файла csv.
        :args csv_file -> string, путь к файлу csv.
        :return self.users_dict -> dict, словарь формата "пользователь": список доступных ему модулей/функций,
                self.row_dicts -> list, список всех существующих модулей/функций.
        '''
        # with open(json_file, "r") as f: # в случае необходимости анализа существующего файла json для последующего его обновления частично, а не полностью
        #     s = json.loads(f.read())
        
        username = csv_file.split('.')[0]

        try:
            with open(csv_file, 'rU') as file:
                reader = csv.DictReader(file)
                title = reader.fieldnames[0]
                keys = title.split(';')
                for row in reader:
                    values = row[title].split(';')
                    row_dict = {keys[i]:values[i] for i in range(len(keys))}
                    self.row_dicts.append(row_dict)
        except Exception, e:
            print 'Error in parsing csv-file:', e

        self.users_dict.update({username: self.row_dicts[self.iterator:]})
        self.iterator = len(self.row_dicts)
        return self.users_dict, self.row_dicts # в случае необходимости отдельного использования метода

    def to_json_writer(self, json_file):
        '''
        Записывает данные, полученные при обработке файла csv, в файл json.
        :args json_file -> string, путь к файлу json.
        :return dict_to_dump -> dict, словарь, записанный в файл json.
        '''

        def del_duplicate(list_): # функция удаления повторяющихся элементов в списке (подходит для списка словарей)
            new_list = []
            for i in list_:
                if i not in new_list:
                    new_list.append(i)
            list_ = new_list
            return list_        
        
        self.row_dicts = del_duplicate(self.row_dicts) # удаление повторяющихся элементов в списке словарей
        param_lists = []
        list_for_json = []
        for i in range(len(self.row_dicts)):
            param_lists.append([])
            for k, v in self.users_dict.iteritems():
                if self.row_dicts[i] in v:
                    param_lists[i].append({'user':k})
            dict_for_json = OrderedDict({'param':param_lists[i]})
            dict_for_json.update(self.row_dicts[i])
            list_for_json.append(dict_for_json) # список для записи в файл json по формату, заданному в ТЗ
        dict_to_dump = {'commands':list_for_json}

        with open(json_file, "w") as f:
            f.write(json.dumps(dict_to_dump, indent=4,))

        return dict_to_dump # в случае необходимости отдельного использования метода

if __name__ == "__main__":
    Converter(['user1.csv', 'user2.csv', 'user3.csv'], 'file.json')