from mysql.connector import connect

# connection

conn= connect(
    host='localhost',
    port='3306',
    user='root',
    passwd='',
    db='mydb'
)

c=conn.cursor()
#fetch

def view_all_data():
    c.execute('select * from insurance order by id asc')
    data=c.fetchall()
    return data