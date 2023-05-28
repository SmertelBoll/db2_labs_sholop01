from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
# from redis import Redis
import redis
import json


app = Flask(__name__)
# cache = redis.Redis()
# redis = Redis()
redis_client = redis.Redis(host='redis', port=6379)
redis_client.flushall()


# З'єднання з базою даних
# engine = create_engine('postgresql://sholop01_lab2:21132113@localhost/sholop01_lab2_DB')
engine = create_engine('postgresql://postgres:postgres@db/zno_db')

# Створення базового класу для автоматичного відображення таблиці
Base = automap_base()

# Відображення таблиць у базі даних на класи
Base.prepare(engine, reflect=True)

# Отримання класу для потрібної таблиці
MyTableClass = Base.classes.zno
ZnoTable = Base.classes.znotable
Place = Base.classes.place
Educational = Base.classes.educational
ResultZno = Base.classes.resultzno
ZnoPT = Base.classes.znopt

session = Session(engine)

pages = {
    'znotable': ZnoTable,
    'place': Place,
    'educational': Educational,
    'resultzno': ResultZno,
    'znopt': ZnoPT
}

@app.route('/')
def index():
    table = request.args.get('table', 'znotable')

    CurrentClass = pages[table]

    # Отримання всіх записів з таблиці
    if table == 'znotable':
        data = session.query(CurrentClass).order_by(CurrentClass.outid).all()
    else:
        data = session.query(CurrentClass).order_by(CurrentClass.id).all()

    data_dicts = []
    for obj in data:
        row_dict = {key: getattr(obj, key) for key in CurrentClass.__table__.columns.keys()}
        data_dicts.append(row_dict)

    data_5 = data_dicts[-5:]
    # Закриття сесії
    session.close()

    # Передача даних до шаблону HTML

    return render_template('index.html', columns=CurrentClass.__table__.columns.keys(), rows=data_5,
                           tables=pages.keys(), current_table=table)


@app.route('/add_row', methods=['POST'])
def add_row():
    # отримати значення полів
    data = request.json
    table = data['table']
    del data['table']
    CurrentClass = pages[table]

    new_row_dict = {}
    for key in data:
        if data[key] == '':
            data[key] = None
        new_row_dict[key] = data[key]
    new_row = CurrentClass(**new_row_dict)

    session.add(new_row)
    session.commit()
    return redirect(url_for('index'))


@app.route('/update_row', methods=['POST'])
def update_row():
    data = request.json
    table = data['table']
    del data['table']

    CurrentClass = pages[table]

    # Виконати запит до бази даних на оновлення рядка

    if table == 'znotable':
        row_to_update = session.query(CurrentClass).filter_by(outid=data['outid']).one()
    else:
        row_to_update = session.query(CurrentClass).filter_by(id=data['id']).one()

    for key, value in data.items():
        if value == 'None':
            value = None
        # print(value, type(value))
        setattr(row_to_update, key, value)

    session.commit()

    # Повернути оновлені дані
    return jsonify(data)


@app.route('/delete_row', methods=['POST'])
def delete_row():
    data = request.json
    table = data['table']
    del data['table']

    CurrentClass = pages[table]

    # Виконати запит до бази даних на оновлення рядка

    if table == 'znotable':
        row_to_delete = session.query(CurrentClass).filter_by(outid=data['outid']).one()
    else:
        row_to_delete = session.query(CurrentClass).filter_by(id=data['id']).one()

    session.delete(row_to_delete)

    session.commit()

    return redirect(url_for('index'))


@app.route('/data')
def data():
    year = request.args.get('year', '2020')
    subject = request.args.get('subject', 'umlball100')
    region = request.args.get('region', 'Львівська')
    region += ' область'
    status = subject.replace('ball100', 'teststatus')

    cache_key = f"data:{year}:{subject}:{region}"
    # Спробувати отримати дані з кешу Redis
    cached_data = redis_client.get(cache_key)

    # if cached_data != b'[{}]':
    if cached_data is not None:
        # Перетворити закешовані дані з рядка JSON у список
        data = json.loads(cached_data)
        print('get cache')

    else:
        column = getattr(ResultZno, subject)
        subject_status = getattr(ResultZno, status)
        data = session.query(func.min(column)) \
            .select_from(ZnoTable) \
            .join(ResultZno, ZnoTable.resznoid == ResultZno.id) \
            .join(Place, ZnoTable.placeid == Place.id) \
            .filter(subject_status == 'Зараховано') \
            .filter(Place.regname == region) \
            .filter(ZnoTable.year == year) \
            .all()

        if data[0][0] is not None:
            data = data[0][0]
        else:
            data = -1

        # Зберегти дані в кеші Redis
        redis_client.setex(cache_key, 3600, data)

    regs = session.query(Place.regname).group_by(Place.regname).all()
    regs = [item[0] for item in regs]

    columns = ['Result']
    rows = [{'Result': data}]

    return render_template('request.html', columns=columns, rows=rows, regs=regs,
                           selected_subject=subject, selected_year=year, selected_region=region)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
