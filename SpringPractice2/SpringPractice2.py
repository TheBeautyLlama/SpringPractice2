import os
from urllib import response
import requests
import json
import csv
import re
from tkinter import * 
from tkinter import ttk

def api_key_check():
    """������� �������� API �����
    """

    # ���������� ���������� ��� �������� �����
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
    # ����� ��������� �� �������� ���������� �����
    print('\nSaved API key!')

def load_to_objects():
    """������� �������������, ������������ �������� ������ � data.mos.ru, � �����
       ��������� �� ��� �������� ��������� �����
    """

    # ���������� ���������� � ������� �������� ����� �� apidata.mos.ru
    global resp
    # ���������� ���������� ��� �������� �����
    global api_key
    # ���������� ���������� �������� � ���� .json ��������������� ����� apidata.mos.ru
    global templates
    # ��������� ID, ��������� �������������
    dataset_id = dataset_id_entry.get()
 
    print (f"https://apidata.mos.ru/v1/datasets/{dataset_id}?api_key={api_key}")

    # ������ �������� ������ � ����� ������
    resp = requests.get(f"https://apidata.mos.ru/v1/datasets/{dataset_id}?api_key={api_key}")

    # ����� ������������������ ������ � .json
    filename = "result.json"
    with open(filename, 'w') as f:
        json.dump(resp.text, f)
    print(resp.text)
    
    # ����� ���������������� ������ � .json � FullDescription � .html, ��������� � .txt
        # ���������� ���������� �������� � ���� .json ��������������� ����� apidata.mos.ru
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

    # ����� ��������� �� �������� ��������
    print("\nLoaded description!")

def load_to_objects_rows():
    """������� �������������, ������������ ������ � data.mos.ru, � �����
       ��������� �� ��� �������� ��������� �����
    """
    # ���������� ���������� � ������� �������� ����� �� apidata.mos.ru
    global resp
    # ���������� ���������� ��� �������� �����
    global api_key
    # ���������� ���������� �������� � ���� .json ��������������� ����� apidata.mos.ru
    global templates
    # ��������� ID, ��������� �������������
    dataset_id = dataset_id_entry.get()
    print (f"https://apidata.mos.ru/v1/datasets/{dataset_id}/rows?api_key={api_key}")
    # ������ ������ � ����� ������
    resp = requests.get(f"https://apidata.mos.ru/v1/datasets/{dataset_id}/rows?api_key={api_key}")
    
    # ����� ���������������� ������ � .json, "���������" � .txt
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

    # ����� ��������� �� �������� ��������
    print("\nLoaded rows!")

def create_csv_from_rows():
    """ �������, ������������ .csv ����� �� ������ apidata.mos.ru
    """
    # ���������� ���������� �������� � ���� .json ��������������� ����� apidata.mos.ru
    global templates
    # ��������������� ����������
    headers = templates[0].keys()

    # ��������� .csv �����
    with open('file.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(templates)
    print("\nCreated CSV!")

def everything_at_once():
    """�������, ����������� ��� �������, ����� ���� �����
    """

    # ������� �������� API �����
    api_key_check()

    # ������� �������������, ������������ �������� ������ � data.mos.ru, � ����� ��������� �� ��� �������� ��������� �����
    load_to_objects()

    #������� �������������, ������������ ������ � data.mos.ru, � ����� ��������� �� ��� �������� ��������� �����
    load_to_objects_rows()

    # �������, ������������ .csv ����� �� ������ apidata.mos.ru
    create_csv_from_rows()
    print("\nDone!")

#
# ���������� ���������� ��� ID ��������� �������������, �����, ������ apidata.mos.ru
global dataset_id
global api_key
global resp

# ���������������� ���������
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