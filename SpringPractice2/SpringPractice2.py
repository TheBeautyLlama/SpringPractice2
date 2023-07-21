import os
from urllib import response
import requests
import json
import csv
import re
from tkinter import * 
from tkinter import ttk

def api_key_check():
    """Функция проверки API ключа 
    """

    # Глобальная переменная для хранения ключа
    global api_key
    try:
        file = open('api_key.txt')
    except IOError as e:
        with open("api_key.txt","w") as f:
            f.write(api_key_entry.get())
    else:
        with file:
            api_key_entry.insert(0, api_key)
    with open('api_key.txt', 'r') as f:
        api_key = f.read()
    # Вывод сообщения об успешном сохранении ключа
    print('\nSaved API key!')

def load_to_objects():
    """Функция запрашивающая, записывающая описание данных с data.mos.ru, а также
       создающая из них читаемые человеком файлы
    """

    # Глобальная переменная в которой хранится ответ от apidata.mos.ru
    global resp
    # Глобальная переменная для хранения ключа
    global api_key
    # Глобальная переменная хранящая в себе .json форматированный ответ apidata.mos.ru
    global templates
    # Получение ID, введённого пользователем
    dataset_id = dataset_id_entry.get()
 
    print (f"https://apidata.mos.ru/v1/datasets/{dataset_id}?api_key={api_key}")

    # Запрос описания данных с сайта Москвы
    resp = requests.get(f"https://apidata.mos.ru/v1/datasets/{dataset_id}?api_key={api_key}")

    # Вывод неформатированного ответа в .json
    filename = "result.json"
    with open(filename, 'w') as f:
        json.dump(resp.text, f)
    print(resp.text)
    
    # Вывод форматированного ответа в .json и FullDescription в .html, читаемого в .txt
        # Глобальная переменная хранящая в себе .json форматированный ответ apidata.mos.ru
    templates = json.loads(resp.text)
    with open('readable_result.txt', 'w') as f:
        f.write("")
    for section, commands in templates.items():
        with open('readable_result.txt', 'a') as f:
            if section == "FullDescription":
                    try:
                        with open("FullDescritpion.html","w") as i:
                            i.write(commands)
                    except TypeError:
                        print("FullDiscription is Null")
            f.write(f"\n")
            f.write(f"{section}: {commands} \n")
        print(f"{section}: {commands}")

    # Вывод сообщения об успешной загрузке
    print("\nLoaded description!")

def load_to_objects_rows():
    """Функция запрашивающая, записывающая данные с data.mos.ru, а также
       создающая из них читаемые человеком файлы
    """
    # Глобальная переменная в которой хранится ответ от apidata.mos.ru
    global resp
    # Глобальная переменная для хранения ключа
    global api_key
    # Глобальная переменная хранящая в себе .json форматированный ответ apidata.mos.ru
    global templates
    # Получение ID, введённого пользователем
    dataset_id = dataset_id_entry.get()
    print (f"https://apidata.mos.ru/v1/datasets/{dataset_id}/rows?api_key={api_key}")
    # Запрос данных с сайта Москвы
    resp = requests.get(f"https://apidata.mos.ru/v1/datasets/{dataset_id}/rows?api_key={api_key}")
    
    # Вывод форматированного ответа в .json, "читаемого" в .txt
    filename = "rows.json"
    with open(filename, 'w') as f:
        json.dump(resp.text, f)
    print(resp.text)

    templates = json.loads(resp.text)
    with open('readable_rows.txt', 'w') as f:
                f.write("")
    for tuple in templates:
        for section, commands in tuple.items():
            with open('readable_rows.txt', 'a') as f:
                f.write(f"\n")
                f.write(f"{section}: {commands} \n")
            print(f"{section}: {commands}")

    # Вывод сообщения об успешной загрузке
    print("\nLoaded rows!")

def create_csv_from_rows():
    """ Функция, генерирующая .csv файлы из ответа apidata.mos.ru
    """
    # Глобальная переменная хранящая в себе .json форматированный ответ apidata.mos.ru
    global templates
    # Вспомогательная переменная
    headers = templates[0].keys()

    # Генерация .csv файла
    with open('file.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(templates)
    print("\nCreated CSV!")

def everything_at_once():
    """Функция, вызыывающая все функции, кроме себя самой
    """

    # Функция проверки API ключа
    api_key_check()

    # Функция запрашивающая, записывающая описание данных с data.mos.ru, а также создающая из них читаемые человеком файлы
    load_to_objects()

    #Функция запрашивающая, записывающая данные с data.mos.ru, а также создающая из них читаемые человеком файлы
    load_to_objects_rows()

    # Функция, генерирующая .csv файлы из ответа apidata.mos.ru
    create_csv_from_rows()
    print("\nDone!")

#
# Глобальные переменные для ID введённого пользователем, ключа, ответа apidata.mos.ru
global dataset_id
global api_key
global resp

# Пользовательский интерфейс
root = Tk()
root.title("User Interface")
root.geometry("300x250")

greeting = ttk.Label(text="Enter article ID")
greeting.pack(anchor=N)

dataset_id_entry = ttk.Entry()
dataset_id_entry.pack(anchor=N)

api_key_request = ttk.Label(text="Enter your API key")
api_key_request.pack(anchor=N)

api_key = str("")
api_key_entry = ttk.Entry()
api_key_entry.pack(anchor=N)
try:
    file = open('api_key.txt')
except IOError as e:
    print("")
else:
    with open('api_key.txt', 'r') as f:
        api_key = f.read()
        api_key_entry.insert(0, api_key)

load_button = ttk.Button(text="Load description", command = load_to_objects)
load_button.pack(anchor=N)

load_rows_button = ttk.Button(text="Load rows", command = load_to_objects_rows)
load_rows_button.pack(anchor=N)

create_csv_button = ttk.Button(text="Create CSV from rows", command = create_csv_from_rows)
create_csv_button.pack(anchor=N)

save_key_button = ttk.Button(text="Save API Key", command = api_key_check)
save_key_button.pack(anchor=N)

everything_at_once_button = ttk.Button(text="Everything at once", command = everything_at_once)
everything_at_once_button.pack(anchor=N)

root.mainloop()