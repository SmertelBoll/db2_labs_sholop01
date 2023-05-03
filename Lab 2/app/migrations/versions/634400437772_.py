"""empty message

Revision ID: 634400437772
Revises: 
Create Date: 2023-05-02 22:56:35.163598

"""
from app import app, db
from sqlalchemy import text



# revision identifiers, used by Alembic.
revision = '634400437772'
down_revision = None
branch_labels = None
depends_on = None




class Place(db.Model):
    __tablename__ = 'place'

    id = db.Column(db.Integer, primary_key=True)
    regname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    areaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    tername = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    tertypename = db.Column(db.TEXT(), autoincrement=False, nullable=True)


class Educational(db.Model):
    __tablename__ = 'educational'

    id = db.Column(db.Integer, primary_key=True)
    eoname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    eotypename = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    eoregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    eoareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    eotername = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    eoparent = db.Column(db.TEXT(), autoincrement=False, nullable=True)


class ResultZno(db.Model):
    __tablename__ = 'resultzno'

    id = db.Column(db.Integer, primary_key=True)

    ukrtest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    ukrteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    ukrball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    ukrball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    ukrball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    ukradaptscale = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    histtest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    histlang = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    histteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    histball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    histball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    histball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    mathtest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathlang = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    mathball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    mathball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    phystest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    physlang = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    physteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    physball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    physball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    physball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    chemtest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    chemlang = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    chemteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    chemball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    chemball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    chemball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    biotest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    biolang = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    bioteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    bioball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    bioball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    bioball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    geotest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    geolang = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    geoteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    geoball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    geoball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    geoball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    engtest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    engteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    engball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    engball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    engdpalevel = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    engball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    fratest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    frateststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    fraball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    fraball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    fradpalevel = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    fraball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    deutest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    deuteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    deuball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    deuball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    deudpalevel = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    deuball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    spatest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    spateststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    spaball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    spaball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    spadpalevel = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    spaball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    mathsttest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathstteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathstlang = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathstball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    mathdpalevel = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathstball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)

    umltest = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    umlteststatus = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    umlball100 = db.Column(db.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    umlball12 = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    umlball = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    umladaptscale = db.Column(db.INTEGER(), autoincrement=False, nullable=True)


class ZnoPT(db.Model):
    __tablename__ = 'znopt'

    id = db.Column(db.Integer, primary_key=True)

    ukrptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    ukrptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    ukrptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    ukrpttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    histptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    histptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    histptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    histpttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    mathptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathpttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    physptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    physptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    physptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    physpttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    chemptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    chemptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    chemptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    chempttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    bioptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    bioptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    bioptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    biopttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    geoptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    geoptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    geoptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    geopttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    engptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    engptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    engptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    engpttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    fraptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    fraptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    fraptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    frapttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    deuptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    deuptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    deuptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    deupttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    spaptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    spaptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    spaptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    spapttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    mathstptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathstpttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathstptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    mathstptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    umlptname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    umlptareaname = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    umlpttername = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    umlptregname = db.Column(db.TEXT(), autoincrement=False, nullable=True)


class ZnoTable(db.Model):
    __tablename__ = 'znotable'

    outid = db.Column(db.TEXT(), primary_key=True)
    year = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    birth = db.Column(db.INTEGER(), autoincrement=False, nullable=True)
    sextypename = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    regtypename = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    classprofilename = db.Column(db.TEXT(), autoincrement=False, nullable=True)
    classlangname = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    ukrsubtest = db.Column(db.TEXT(), autoincrement=False, nullable=True)

    placeid = db.Column(db.INTEGER(), db.ForeignKey('place.id'), autoincrement=False, nullable=True)
    edid = db.Column(db.INTEGER(), db.ForeignKey('educational.id'), autoincrement=False, nullable=True)
    resznoid = db.Column(db.INTEGER(), db.ForeignKey('resultzno.id'), autoincrement=False, nullable=True)
    znoptid = db.Column(db.INTEGER(), db.ForeignKey('znopt.id'), autoincrement=False, nullable=True)


with app.app_context():
    db.create_all()


def insert_tables(insert_query, data, col_names, tablename, len_table):
    print(f"\n -- Заповнення таблиці {tablename} --")

    step = 1000
    skip = False
    for main_index in range(0, len(data), step):

        local_data = data[main_index: min(main_index + step, len(data))]
        if len(local_data) == 0:  # ми перебрали всі рядки
            break

        for count, d in enumerate(local_data):
            if main_index+count < len_table:
                if main_index+count == 0:
                    print('Пропускаємо завантажені дані...')
                    skip = True
                continue
            else:
                skip = False
            res = {}
            for id, el in enumerate(d):
                res[str(col_names[id])] = el
            db.session.execute(insert_query, res)

        if not skip:
            db.session.commit()
            print(f"{main_index + step}")


def fill_place_educational(table_model):
    col_names = [column.name for column in table_model.__table__.columns][1:] # всі колонки таблиці без id
    col_names_with_points = [f":{col}" for col in col_names]
    data = db.session.execute(text(f"""
            SELECT {', '.join(col_names)}
            FROM zno 
            GROUP BY {', '.join(col_names)} 
        """))
    data = data.fetchall()  # отримуємо всі унікальні дані місця реєстрації

    insert_query = text(f"""
        INSERT INTO {table_model.__tablename__} ({', '.join(col_names)})
        VALUES ({', '.join(col_names_with_points)})
        """)

    len_table = db.session.execute(text(f"""SELECT count(*) FROM {table_model.__tablename__}"""))
    len_table = len_table.fetchall()[0][0]  # кількість записів предмета у нашій таблиці

    insert_tables(insert_query, data, col_names, table_model.__tablename__, len_table)


def fill_reszno_znopt(table_model):
    col_names = [column.name for column in table_model.__table__.columns][1:]  # без id
    col_names_with_points = [f":{col}" for col in col_names]

    data = db.session.execute(text(f"""SELECT {', '.join(col_names)} FROM zno"""))
    data = data.fetchall()  # отримуємо всі дані

    insert_query = text(f"""
                        INSERT INTO {table_model.__tablename__} ({', '.join(col_names)})
                        VALUES ({', '.join(col_names_with_points)})
                    """)

    len_table = db.session.execute(text(f"""SELECT count(*) FROM {table_model.__tablename__}"""))
    len_table = len_table.fetchall()[0][0]  # кількість записів предмета у нашій таблиці

    insert_tables(insert_query, data, col_names, table_model.__tablename__, len_table)


def get_id_from_PE(all_col_names, table_model, data):  # from Place or Educational
    ids = []  # id з таблиці
    col_names = [column.name for column in table_model.__table__.columns][1:]  # всі колонки таблиці без id
    index_col_name = [all_col_names.index(col) for col in col_names]  # індекс колонок, в яких потрібні дані

    for data_el in data:
        str_where = ""
        for i in index_col_name:

            data_el_i = data_el[i].replace("'", "''") if data_el[i] is not None else data_el[i]  # якщо апостроф є
            res = f"= '{data_el_i}'" if data_el_i is not None else f"IS NULL"
            str_where = str_where + f"{all_col_names[i]} {res} AND "
        str_where = str_where[:-4]  # видаляємо останнє AND

        id = db.session.execute(text(f"""
                                SELECT id
                                FROM {table_model.__tablename__} 
                                WHERE {str_where}
                            """))

        id = id.fetchall()  # отримуємо наше id
        ids.append(id)
    return ids


def fill_zno_table():
    all_col_names = db.session.execute(text(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'zno'
            ORDER BY ordinal_position;
        """))  # дістаємо назви колонок
    all_col_names = all_col_names.fetchall()  # повертає таке: [('spaptareaname',), ('spaptname',), ('spaptregname',), ('spapttername',)]
    all_col_names = [item[0] for item in all_col_names]  # перетворюэмо на ['spaptareaname', 'spaptname', 'spaptregname', 'spapttername']

    main_col_names = [column.name for column in ZnoTable.__table__.columns][:-4]  # без 4 ключів з інших таблиць
    key_names = [column.name for column in ZnoTable.__table__.columns][-4:]  # 4 ключі інших таблиць
    col_names_with_points = [f":{col}" for col in main_col_names]
    key_names_with_points = [f":{col}" for col in key_names]

    col_names = main_col_names + key_names

    data = db.session.execute(text(f"""SELECT {', '.join(main_col_names)} FROM zno"""))
    data = data.fetchall()  # отримуємо дані для основних стовпців

    all_data = db.session.execute(text(f"""SELECT * FROM zno"""))
    all_data = all_data.fetchall()  # отримуємо дані

    data_res = db.session.execute(text(f"""SELECT id FROM resultzno"""))
    data_res = data_res.fetchall()  # отримуємо id resultzno

    data_pt = db.session.execute(text(f"""SELECT id FROM znopt"""))
    data_pt = data_pt.fetchall()  # отримуємо id znopt

    insert_query = text(f"""
                        INSERT INTO {ZnoTable.__tablename__} ({', '.join(col_names)})
                        VALUES ({', '.join(col_names_with_points + key_names_with_points)})
                    """)

    len_table = db.session.execute(text(f"""SELECT count(*) FROM {ZnoTable.__tablename__}"""))
    len_table = len_table.fetchall()[0][0]  # кількість записів предмета у нашій таблиці

    if len(data) != len_table and len(data) != 0:  # кількість отриманих записів не рівна кількісті записів у нашій таблиці
        ZnoTable.query.delete()  # видаляємо записи
        db.session.commit()

    print(f"\n -- Заповнення таблиці {ZnoTable.__tablename__} --")

    step = 1000
    for main_index in range(0, len(data), step):

        local_data = data[main_index: min(main_index + step, len(data))]
        if len(local_data) == 0:  # ми перебрали всі рядки
            break

        local_all_data = all_data[main_index: min(main_index + step, len(all_data))]
        local_data_res = data_res[main_index: min(main_index + step, len(data_res))]
        local_data_pt = data_pt[main_index: min(main_index + step, len(data_pt))]

        place_ids = get_id_from_PE(all_col_names, Place, local_all_data)  # id місця реєстрації з таблиці Place
        educational_ids = get_id_from_PE(all_col_names, Educational, local_all_data)  # id місця навчання з таблиці Educational

        result = [(*loc, place[0][0], ed[0][0], res[0], pt[0]) for loc, place, ed, res, pt in zip(local_data, place_ids, educational_ids, local_data_res, local_data_pt)]
        # отримали наступний кортеж: [('outid', year, birth, 'sextypename', 'regtypename', 'classprofilename',
        # 'classlangname', 'ukrsubtest', 'placeid', 'edid', 'resznoid', 'znoptid'),

        for r in result:
            res = {}
            for id, el in enumerate(r):
                res[str(col_names[id])] = el
            db.session.execute(insert_query, res)
        db.session.commit()
        print(f"{main_index+step}")
    print()


def upgrade():
    print('upgrade')
    fill_place_educational(Place)

    fill_place_educational(Educational)

    fill_reszno_znopt(ResultZno)

    fill_reszno_znopt(ZnoPT)

    fill_zno_table()



def downgrade():
    print('downgrade')
    db.session.execute(text("DROP TABLE place CASCADE"))
    db.session.execute(text("DROP TABLE educational CASCADE"))
    db.session.execute(text("DROP TABLE resultzno CASCADE"))
    db.session.execute(text("DROP TABLE znopt CASCADE"))
    db.session.execute(text("DROP TABLE znotable CASCADE"))
    db.session.commit()

