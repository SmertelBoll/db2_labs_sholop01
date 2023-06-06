from flask import Flask, render_template, url_for, redirect, request
from pymongo import MongoClient

import psql_functions, mongo_functions
from mongo_functions import *
import psycopg2
app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://postgres:root1@localhost/student01_DB")
#engine = create_engine("postgresql+psycopg2://postgres:root1@db/student01_DB")

mongo_client = MongoClient('mongodb://localhost:27017/')
#mongo_client = MongoClient('mongodb://mongodb:27017/')

db = mongo_client.student01_DB


#docker-compose build --no-cache && docker-compose up -d --force-recreate
Session = sessionmaker(bind=engine)
session = Session()

Config = psql_functions.Config


@app.route("/", methods=['POST', 'GET'])
def showTables():
    global Config
    config = Config()
    if request.method == 'POST':
        if request.form["submit_button"] == "Use PostgreSQL":
            Config = psql_functions.Config
        if request.form["submit_button"] == "Use MongoDB":
            Config = mongo_functions.Config

        print(Config)
        if request.form["submit_button"] == "Show locations":
            headers = tuple(config.fetchLocationsColumnNames())
            data = tuple(config.fetchRowsFromLocations())
            return render_template("table.html", headers=headers, data=data, url="/locations")

        elif request.form['submit_button'] == "Show students":
            headers = tuple(config.fetchStudentsColumnNames())
            data = tuple(config.fetchRowsFromStudents())
            return render_template("table.html", headers=headers, data=data, url="/students")

        elif request.form['submit_button'] == "Show EO":
            headers = tuple(config.fetchEOColumnNames())
            data = tuple(config.fetchRowsFromEO())
            return render_template("table.html", headers=headers, data=data, url="/eo")

        elif request.form['submit_button'] == "Show Tests":
            headers = config.fetchTestsColumnNames()
            data = tuple(config.fetchRowsFromTests())
            return render_template("table.html", headers=headers, data=data, url="/tests")

        elif request.form['submit_button'] == "Filters":
            years = ("2019", "2021")
            regnames = config.fetchRegnames()
            subjects_dict = config.subjectDict()
            subjects = list(subjects_dict.keys())
            index = 0
            for subject in subjects:
                if subjects[index] == 'Українська мова':
                    subjects[index] = 'Українська_мова'

                if subjects[index] == 'Українська мова та література':
                    subjects[index] = 'Українська_мова_та_література'
                index += 1

            subjects = tuple(subjects)
            functions = ('max', 'min', 'avg')

            return render_template("filters.html", years=years, regnames=regnames, subjects=subjects, functions=functions, url="/filters")

    return render_template("main.html")


@app.route("/locations", methods=['POST', 'GET'])
def locationsTable():
    global Config
    config = Config()
    url="/locations"
    headers = tuple(config.fetchLocationsColumnNames())
    data = tuple(config.fetchRowsFromLocations())
    if request.method == 'POST':
        location_data = {column_name: request.form.get(column_name) if request.form.get(column_name) != '' else None for
                   column_name in headers}
        location = Locations(**location_data)
        if 'update_delete' in request.form:
            if request.form['update_delete'] == "Update":
                config.updateLocation(location.location_id, location_data)
                print(request.form)
            if request.form['update_delete'] == "Delete":
                config.deleteLocation(location.location_id)

        else:
            config.createLocation(location_data)

        session.commit()
        return redirect(url)

    return render_template("table.html", headers=headers, data=data, url=url)


@app.route("/eo", methods=['POST', 'GET'])
def eoTable():
    global Config
    config = Config()

    url="/eo"
    headers = tuple(config.fetchEOColumnNames())
    data = tuple(config.fetchRowsFromEO())
    if request.method == 'POST':
        eo_data = {column_name: request.form.get(column_name) if request.form.get(column_name) != '' else None for
                        column_name in headers}
        eo = EO(**eo_data)
        if 'update_delete' in request.form:
            if request.form['update_delete'] == "Update":
                config.updateEO(eo.eo_id, eo_data)

            if request.form['update_delete'] == "Delete":
                config.deleteEO(eo.eo_name, eo.eo_type, eo.location_id)

        else:
            config.createEO(eo_data)

        session.commit()
        return redirect(url)

    return render_template("table.html", headers=headers, data=data, url=url)


@app.route("/students", methods=['POST', 'GET'])
def studentsTable():
    global Config
    config = Config()

    url = "/students"
    headers = tuple(config.fetchStudentsColumnNames())
    data = tuple(config.fetchRowsFromStudents())
    if request.method == 'POST':
        student_data = {column_name: request.form.get(column_name) if request.form.get(column_name) != '' else None for
                      column_name in headers}
        student = Students(**student_data)
        if 'update_delete' in request.form:
            if request.form['update_delete'] == "Update":
                config.updateStudent(student.outid, student_data)

            if request.form['update_delete'] == "Delete":
                config.deleteStudent(student.outid)
                session.commit()

        else:
            config.createStudent(student_data)

        session.commit()
        return redirect(url)

    return render_template("table.html", headers=headers, data=data, url=url)


@app.route("/tests", methods=['POST', 'GET'])
def testsTable():
    global Config
    config = Config()

    url="/tests"
    headers = tuple(config.fetchTestsColumnNames())
    data = tuple(config.fetchRowsFromTests())
    if request.method == 'POST':
        tests_data = {column_name: request.form.get(column_name) if request.form.get(column_name) != '' else None for column_name in headers}
        test = Tests(**tests_data)
        if 'update_delete' in request.form:
            if request.form['update_delete'] == "Update":
                config.updateTest(test.tests_id, tests_data)

            if request.form['update_delete'] == "Delete":
                config.deleteTest(test.tests_id)

        else:
            config.createTest(tests_data)
        session.commit()
        return redirect(url)

    return render_template("table.html", headers=headers, data=data, url=url)


@app.route("/filters", methods=["POST", "GET"])
def filters():
    global Config
    config = Config()

    years = ("2019", "2021")
    regnames = config.fetchRegnames()
    subjects_dict = config.subjectDict()
    subjects = list(subjects_dict.keys())
    index = 0
    for subject in subjects:
        if subjects[index] == 'Українська мова':
            subjects[index] = 'Українська_мова'

        if subjects[index] == 'Українська мова та література':
            subjects[index] = 'Українська_мова_та_література'
        index += 1

    subjects = tuple(subjects)
    functions = ('max', 'min', 'avg')
    if request.method == 'POST':
        selected_year = request.form['years']
        selected_regname = request.form['regnames']
        selected_subject = request.form['subjects']
        selected_function = request.form['funcs']

        for key in config.spaceProblemSolverDict().keys():
            if selected_subject == key:
                selected_subject = config.spaceProblemSolverDict().get(key)
        query_result = config.fetchGrade(selected_year, selected_regname, subjects_dict.get(selected_subject), selected_function)
        grade = query_result
        if grade == 0:
            grade = 'None'
        session.commit()

    return render_template("filters.html", years=years, regnames=regnames, subjects=subjects, functions=functions, grade=grade, url="/filters")


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True)
