from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from redis import Redis


app = Flask(__name__)
# redis = Redis()

# З'єднання з базою даних
engine = create_engine('postgresql://sholop01_lab2:21132113@localhost/sholop01_lab2_DB')

# Створення базового класу для автоматичного відображення таблиці
Base = automap_base()

# Відображення таблиць у базі даних на класи
Base.prepare(engine, reflect=True)

# Отримання класу для потрібної таблиці
MyTableClass = Base.classes.zno
session = Session(engine)

@app.route('/')
def index():
    # Отримання всіх записів з таблиці
    data = session.query(MyTableClass).all()

    data_dicts = []
    for obj in data:
        row_dict = {key: getattr(obj, key) for key in MyTableClass.__table__.columns.keys()}
        data_dicts.append(row_dict)

    data_5 = data_dicts[-5:]
    # Закриття сесії
    session.close()

    # Передача даних до шаблону HTML
    print(MyTableClass.__table__.columns.keys())
    print(data_5)
    return render_template('index.html', columns=MyTableClass.__table__.columns.keys(), rows=data_5)


@app.route('/add_row', methods=['POST'])
def add_row():
    # отримати значення полів
    data = request.json

    new_row_dict = {}
    for key in data:
        if data[key] == '':
            data[key] = None
        new_row_dict[key] = data[key]
    new_row = MyTableClass(**new_row_dict)

    session.add(new_row)
    session.commit()
    return redirect(url_for('index'))


@app.route('/update_row', methods=['POST'])
def update_row():
    data = request.json

    # Виконати запит до бази даних на оновлення рядка

    row_to_update = session.query(MyTableClass).filter_by(outid=data['outid']).one()

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

    # Виконати запит до бази даних на оновлення рядка

    row_to_delete = session.query(MyTableClass).filter_by(outid=data['outid']).one()

    session.delete(row_to_delete)

    session.commit()

    return redirect(url_for('index'))


@app.route('/data')
def data():
    year = request.args.get('year', '2020')
    subject = request.args.get('subject', 'umlball100')
    region = request.args.get('region', 'Львівська')
    region += ' область'

    column = getattr(MyTableClass, subject)
    print(year, region, subject, region == 'Херсонська область')
    # Запит до таблиці, наприклад, з БД PostgreSQL
    data = session.query(func.min(column))\
                .filter(MyTableClass.physteststatus == 'Зараховано') \
                .filter(MyTableClass.regname == region) \
                .filter(MyTableClass.year == year) \
                .all()
    regs = session.query(MyTableClass.regname).group_by(MyTableClass.regname).all()
    regs = [item[0] for item in regs]
    print(regs)
    print(data)

    # Зберегти дані у Redis з таймаутом 1 години
    # redis.setex('data', 60, data)

    # columns = ['Area', 'Year', 'Result']
    columns = ['Result']
    rows = []
    # for el in data:
    #     rows.append({columns[0]: el[0], columns[1]: el[1], columns[2]: el[2]})
    for el in data:
        rows.append({columns[0]: el[0]})
    return render_template('request.html', columns=columns, rows=rows, regs=regs,
                           selected_subject=subject, selected_year=year, selected_region=region)



#
# @app.route('/request')
# def request():
#     # Отримати дані з Redis
#     data = redis.get('data')
#
#     # Якщо дані є в Redis, то повернути їх
#     if data:
#         return render_template('data.html', data=data)
#
#     # Інакше зробити запит до таблиці і зберегти його в Redis
#     else:
#         data()


if __name__ == '__main__':
    app.run(debug=True)
