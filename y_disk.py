import os
import posixpath
import sys
import time
import yadisk
from config import *

y = yadisk.YaDisk(token="y0_AgAAAABRtM0fAAlHGQAAAADejyJ6XYGbFWKKQLauAt4KNqRGPyyY_Co")


def get_yandex_disk_token(y):
    # y = yadisk.YaDisk(client_id, client_secret)
    url = y.get_code_url()

    print("Перейдите по следующему URL-адресу: %s" % url)

    code = input("Введите код подтверждения:")

    try:
        response = y.get_token(code)
    except yadisk.exceptions.BadRequestError:
        print("Неправильный код")
        sys.exit(1)

    y.token = response.access_token

    if y.check_token():
        print("Успешно полученный токен!")
    else:
        print("Что-то пошло не так.")
    print(y.token)
    return y.token


def parsing_disk_dir(dir_name):
    print(f'Содержимое папки "/{dir_name}/":\n')
    for item in y.listdir(f'/{dir_name}/'):
        print(item)
        print(f"Название: {item['name']}")
        print(f'Размер: {item["size"]} байт')
        print(f"Тип файла: {item['type']}")
        print(f"Тип документа: {item['media_type']}")
        print(f"Дата создания: {item['created']}\n")


def recursive_upload(y, from_dir, to_dir):
    for root, dirs, files in os.walk(from_dir):
        p = root.split(from_dir)[1].strip(os.path.sep)
        dir_path = posixpath.join(to_dir, p)

        try:
            y.mkdir(dir_path)
        except yadisk.exceptions.PathExistsError:
            pass

        for file in files:
            file_path = posixpath.join(dir_path, file)
            p_sys = p.replace("/", os.path.sep)
            in_path = os.path.join(from_dir, p_sys, file)
            try:
                y.upload(in_path, file_path)
            except yadisk.exceptions.PathExistsError:
                pass


def cleaning_trash(y):
    print("Опустошаю мусорное ведро...")
    operation = y.remove_trash("/")
    print("Это может занять некоторое время...")

    if operation is None:
        print("Не берите в голову. Дело сделано.")
        sys.exit(0)

    while True:
        status = y.get_operation_status(operation.href)

        if status == "in-progress":
            time.sleep(5)
            print("Все еще жду...")
        elif status == "success":
            print("Успех!")
            break
        else:
            print("Получил какой-то странный статус: %r" % (status,))
            print("Это ненормально")
            break


def mass_unloading(from_dir, to_directory):
    directory = os.fsencode(f'{from_dir}')
    for pict in os.listdir(directory):
        y.upload(f"{from_dir}/{pict.decode('utf-8')}", f"/{to_directory}/{pict.decode('utf-8')}")


# y.upload("название_файла.формат", "куда_загружать/название_файла.формат")
# y.download("откуда_выгружть/название_файла.формат", "куда_выгружать/название_файла.формат"))
# y.mkdir("/название_директории")
# y.remove("/откуда_удалять/название_файла.формат", permanently=True)

# y.upload("pictures/горшок.jpg", "/test-dir/горшок.jpg")
# y.remove("/test-dir/горшок.jpg", permanently=True)
# cleaning_trash(y)

