import mysql.connector

try:
    my_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='@Vahid123'
    )

    db_obj = my_connection.cursor()

    with open('ConfigDatabase.sql','r') as sql_file:
        sql_queries = sql_file.read()

    for sql in sql_queries.split(';'):
        if sql:
            db_obj.execute(sql)

    print('Database and tables created Successful')
except Exception as e:
    print(e)