import _sqlite3
import csv


def load_training_dataset():
    with open('comp3208-train-small.csv', 'r') as f:
        reader = csv.reader(f)
        data = next(reader)
        query = 'insert into Training_ts values ({0})'
        query = query.format(','.join('?' * len(data)))
        cursor.execute(query, data)
        for data in reader:
            cursor.execute(query, data)
        connection.commit()


def load_testing_dataset():
    with open('comp3208-test-small.csv', 'r') as f:
        reader = csv.reader(f)
        data = next(reader)
        query = 'insert into Testing_ts values ({0})'
        query = query.format(','.join('?' * len(data)))
        cursor.execute(query, data)
        for data in reader:
            cursor.execute(query, data)
        connection.commit()


connection = _sqlite3.connect("comp3208-small.db")
cursor = connection.cursor()

cursor.execute("create table Training_ts (user int, item int, rating float, timestamp int)")
load_training_dataset()

cursor.execute("create table Testing_ts (user int, item int, timestamp int)")
load_testing_dataset()

cursor.execute("create table Training (user int, item int, rating float )")
cursor.execute("insert into Training select user, item, rating from Training_ts")

cursor.execute("create table Testing (user int, item float )")
cursor.execute("insert into Testing select user, item from Testing_ts")

cursor.execute("drop table Training_ts")
cursor.execute("drop table Testing_ts")

connection.commit()

connection.close()