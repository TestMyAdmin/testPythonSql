import asyncio
import csv
import json

import chardet
from tortoise import Tortoise

from models import Item, init_db


def detect_encoding(file_path: open) -> str:
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding


def read_file(file_path, delimiter):
    data = []
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            data.append([r.strip().strip('"') for r in row])
    return data


data1 = read_file('data/Тестовый файл1.txt', ',')
data2 = read_file('data/Тестовый файл2.txt', ';')


def merge_data(list1, list2):
    return list1 + list2


merged_data = merge_data(data1, data2)

sorted_data = sorted(merged_data, key=lambda x: x[1])


def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


save_to_json(sorted_data, "data/result.json")


async def save_to_db(data):
    items = []
    for row in data:
        items.append(Item(col1=row[0], col2=row[1], col3=row[2] if len(row) > 2 else None))

    await Item.bulk_create(items)


async def main():
    await init_db()
    await save_to_db(sorted_data)
    await Tortoise.close_connections()


asyncio.run(main())
