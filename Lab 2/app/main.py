import psycopg2
import time
import shutil
import os
import sys

import requests
from py7zr import unpack_7zarchive


def connect_bd():
    print('Try connect with DB')
    for _ in range(20):
        try:
            # connect = psycopg2.connect(user='sholop01_lab2', password='21132113', dbname='sholop01_lab2_DB')
            connect = psycopg2.connect(dbname='zno_db', user='postgres', password='postgres', host='db')
            print('Connect successful\n')
            return connect
        except:
            print('DB is unavailable, please wait a moment')
            time.sleep(5)

    print('The database is currently unavailable, please try again later')
    sys.exit()  # якщо база даних дуже довго не відповідає


def download_files(years):
    url = 'https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO__YEAR__.7z'
    shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)

    for year in years:
        print(f"Downloading the file for {year}")

        if os.path.isfile(f"Odata{year}File.csv"):
            print('The file already exists\n')
            continue

        local_url = url.replace('__YEAR__', str(year))
        filename = local_url.split('/')[-1]

        response = requests.get(local_url, stream=True)

        if response.status_code == 200:
            with open(filename, 'wb') as out:
                out.write(response.content)
            shutil.unpack_archive(filename, './')
        else:
            print(f"Error: {response.status_code}")
            continue

        print(f"Download complete\n")


def get_column_names_and_indexes(file_1, file_2):
    # назви колонок кінцевої таблиці
    first_line_1 = file_1.readline().lower()
    first_line_2 = file_2.readline().lower()

    column_names_1 = first_line_1.split(';')
    column_names_2 = first_line_2.split(';')

    for i in range(len(column_names_1)):
        column_names_1[i] = column_names_1[i].split('"')[1]
    for i in range(len(column_names_2)):
        column_names_2[i] = column_names_2[i].split('"')[1]

    in_1 = set(column_names_1)
    in_2 = set(column_names_2)

    in_2_but_not_in_1 = in_2 - in_1
    column_names = column_names_1 + list(in_2_but_not_in_1)

    # позиції елементів з різних таблиць в кінцевій таблиці
    index_1 = []
    index_2 = []

    for el in column_names_1:
        index_1.append(column_names.index(el))
    for el in column_names_2:
        index_2.append(column_names.index(el))

    return column_names, index_1, index_2


def create_table(col_names):
    print('Creating table')
    cursor.execute("select * from information_schema.tables where table_name=%s", ('zno',))
    if bool(cursor.rowcount):  # Якщо таблиця вже існує, то нічого робити не треба
        return

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS zno(
            %s text PRIMARY KEY
        );
        """ % col_names[0]
    )

    cursor.execute('ALTER TABLE zno ADD COLUMN IF NOT EXISTS year int')

    for col in col_names:
        if 'ball100' in col:
            cursor.execute('ALTER TABLE zno ADD COLUMN IF NOT EXISTS %s float' % col)
        elif 'ball' in col or 'scale' in col or 'birth' in col:
            cursor.execute('ALTER TABLE zno ADD COLUMN IF NOT EXISTS %s int' % col)
        else:
            cursor.execute('ALTER TABLE zno ADD COLUMN IF NOT EXISTS %s text' % col)
    print('Created table\n')


def insert(result_insert, values, year, cash):
    global conn
    global cursor

    try:
        cursor.execute(result_insert, (*values, year))
        return
    except:
        print('DB is unavailable, please wait a moment')
        time.sleep(5)

        conn = connect_bd()
        cursor = conn.cursor()

    try:
        for i in range(len(cash['sql'])):
            cursor.execute(cash['sql'][i], (*cash['values'][i], cash['year'][i]))
        return
    except:
        print('The database is currently unavailable, please try again later')
        sys.exit()  # якщо база даних дуже довго не відповідає


def fill_table(year, file, col_names, index_year):
    # Заповнення
    cursor.execute(f"""SELECT count(*) FROM zno WHERE year={year};""")
    rows = cursor.fetchall()
    ind = rows[0][0]

    transaction_cash = {'sql': [], 'values': [], 'year': []}  # щоб не втратити дані у випадку зупинки DB

    print(f"start loading {year}")
    for count, line in enumerate(file):
        if count < ind:
            continue

        if ind % 1000 == 0 and ind != 0 and count >= ind:
            print(f"{ind} rows loaded")
            conn.commit()

            # затираємо збережені дані
            transaction_cash['sql'] = []
            transaction_cash['values'] = []
            transaction_cash['year'] = []
        ind += 1

        line_arr = line.split(";")
        line_arr[-1] = line_arr[-1][:-1]  # після split появляється \n. Його потрібно видалити

        not_null_col_names = []
        not_null_col_values = []

        for el_id, el in enumerate(line_arr):
            el = el.replace('"', '')  # удаляємо зайві лапки
            # якщо елемент не null
            if el != 'null':
                # це число
                if 'ball' in col_names[index_year[el_id]] or \
                        'scale' in col_names[index_year[el_id]] or \
                        'birth' in col_names[index_year[el_id]]:

                    if ',' in el:  # число типу float
                        el = float(el.replace(',', '.'))
                    else:           # число типу int
                        el = int(el)

                not_null_col_names.append(col_names[index_year[el_id]])
                not_null_col_values.append(el)

        result_insert = f"""INSERT INTO zno ({','.join(not_null_col_names)}, year) 
                            VALUES ({'%s,' * (len(not_null_col_names))} %s)"""

        # кешуємо дані
        transaction_cash['sql'].append(result_insert)
        transaction_cash['values'].append(not_null_col_values)
        transaction_cash['year'].append(year)

        insert(result_insert, not_null_col_values, year, transaction_cash)
    conn.commit()
    print(f"finish loading {year}\n")


def result_table():
    print('Creating ResultFile')
    sql = """COPY (SELECT regname, year, MIN(physball100)
                   FROM zno
                   WHERE physteststatus = 'Зараховано'
                   GROUP BY regname, year
                   ORDER BY regname) TO STDOUT WITH CSV DELIMITER ';'"""

    result = open("Result.csv", "w", encoding="utf-8")
    result.write("regName;year;physMinBall100\n")
    cursor.copy_expert(sql, result)
    result.close()
    print("Created\n")

def main():
    # Підключаємо базу даних
    global conn
    conn = connect_bd()

    global cursor
    cursor = conn.cursor()

    # Загружаємо файли
    download_files([2020, 2021])

    # Відкриваємо файли
    f_20 = open(r'Odata2020File.csv', 'r', encoding='Windows-1251')
    f_21 = open(r'Odata2021File.csv', 'r', encoding='utf8')

    # Знайдемо назви колонок та позицію колонок старих таблиць в новій таблиці
    column_names, index_20, index_21 = get_column_names_and_indexes(f_20, f_21)

    # Створюємо таблицю
    create_table(column_names)

    # Заповнення значеннями 2020
    fill_table(2020, f_20, column_names, index_20)

    # Заповнення значеннями 2021
    fill_table(2021, f_21, column_names, index_21)

    f_20.close()
    f_21.close()

    conn.close()


if __name__ == "__main__":
    main()

