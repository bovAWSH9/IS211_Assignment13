#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211_Assignment13 - Web Development with Flask (2/2)"""

import os
import re

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
is_logged = False

students = []
quizzes = []


@app.route('/', methods=["POST", "GET"])
def index():
    if not is_logged:
        return redirect('/login')
    else:
        return redirect('/dashboard')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form['user_name']
        password = request.form['password']
        if user_name == "admin" and password == "password":
            return redirect("/dashboard")
        else:
            error = "The Username or Password is not correct"
            return render_template("Login.html", error=error)
    else:
        return render_template("Login.html", error="")


@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    global students
    global quizzes
    try:
        sqliteConnection = sqlite3.connect('hw13.db')
        cursor = sqliteConnection.cursor()
        students_select_query = """SELECT * from students"""

        cursor.execute(students_select_query)
        students = cursor.fetchall()
        quizzes_select_query = """SELECT * from quizzes"""
        cursor.execute(quizzes_select_query)
        quizzes = cursor.fetchall()
        return render_template("dashboard.html", students=students, quizzes=quizzes)
    except:
        print("error with db connection")


@app.route("/student/add", methods=["POST", "GET"])
def add_student():
    global sqliteConnection
    if request.method == "POST" and 'first_name' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        try:
            sqliteConnection = sqlite3.connect('hw13.db')
            cursor = sqliteConnection.cursor()

            sqlite_insert_query = """INSERT INTO `students`
                                  ('first_name', 'last_name') 
                                   VALUES 
                                  (?,?)"""

            count = cursor.execute(sqlite_insert_query, (first_name, last_name,))
            sqliteConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            return render_template('add_student.html', error="Failed to insert data into sqlite table")
        finally:
            if sqliteConnection:
                sqliteConnection.close()

        return redirect('/dashboard')
    else:
        return render_template('add_student.html', error="")


@app.route("/quiz/add", methods=["POST", "GET"])
def add_quiz():
    global sqliteConnection
    if request.method == "POST" and 'subject' in request.form:
        subject = request.form['subject']
        number_of_questions = request.form['number_of_questions']
        date = request.form['date']
        try:
            sqliteConnection = sqlite3.connect('hw13.db')
            cursor = sqliteConnection.cursor()

            sqlite_insert_query = """INSERT INTO `quizzes`
                                     ('subject', 'number_of_questions','date') 
                                      VALUES 
                                     (?,?,?)"""

            count = cursor.execute(sqlite_insert_query, (subject, number_of_questions, date,))
            sqliteConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            return render_template('add_quiz.html', error="Failed to insert data into sqlite table")
        finally:
            if sqliteConnection:
                sqliteConnection.close()

        return redirect('/dashboard')
    else:
        return render_template('add_quiz.html', error="")


@app.route("/student/<int:id>", methods=["POST", "GET"])
def view_student_result(id):
    global sqliteConnection
    try:
        sqliteConnection = sqlite3.connect('hw13.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = """SELECT * from `quizzes_result`
                                where student_id=? """

        cursor.execute(sqlite_insert_query, (id,))
        results = cursor.fetchall()
        if results == []:
            error = "No Results "
        else:
            error = ''
        return render_template('view_result.html', results=results, error=error)
    except sqlite3.Error as error:
        pass
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    return render_template('view_result.html', error='Something Wrong Happened')


@app.route("/results/add", methods=["POST", "GET"])
def add_result():
    global sqliteConnection

    if request.method == "POST" and 'student_id' in request.form:
        print("hello")
        try:
            quiz_id = request.form['quiz_id']
            student_id = request.form['student_id']
            score = request.form['score']
            sqliteConnection = sqlite3.connect('hw13.db')
            cursor = sqliteConnection.cursor()
            query = """INSERT INTO `quizzes_result`
                                     ('quiz_id', 'student_id','score') 
                                      VALUES 
                                     (?,?,?)"""

            count = cursor.execute(query, (quiz_id, student_id, score,))
            sqliteConnection.commit()
            cursor.close()
            return redirect('/dashboard')
        except sqlite3.Error as error:
            pass
        finally:
            if sqliteConnection:
                sqliteConnection.close()
    else:
        try:
            sqliteConnection = sqlite3.connect('hw13.db')
            cursor = sqliteConnection.cursor()
            students_select_query = """SELECT id from students"""

            cursor.execute(students_select_query)
            students = cursor.fetchall()
            students = [element[0] for element in students]
            quizzes_select_query = """SELECT id from quizzes"""
            cursor.execute(quizzes_select_query)
            quizzes = cursor.fetchall()
            quizzes = [element[0] for element in quizzes]
            return render_template('add_quiz_result.html', error='', students=students, quizzes=quizzes)
        except sqlite3.Error as error:
            pass
        finally:
            if sqliteConnection:
                sqliteConnection.close()


if __name__ == '__main__':
    app.run()
