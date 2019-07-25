import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="H0rr0rland$",
  auth_plugin="mysql_native_password",
  database="saturnine"
)

cursor = mydb.cursor()


def driver(id, today_date, year, month_number, month_name, day, day_name, mood):
  small_id = id.lower()
  create_table(small_id)
  if(mood != 4):
    insert_row(small_id, today_date, year, month_number, month_name, day, day_name, mood)

def create_table(id):
  cursor.execute("CREATE TABLE IF NOT EXISTS " + str(id) + " (date DATE PRIMARY KEY, year YEAR, month_number INTEGER(2), month_name VARCHAR(10), day INTEGER(2), day_name VARCHAR(10), mood INTEGER(1))")

def insert_row(id, today_date, year, month_number, month_name, day, day_name, mood):
  print(mood)
  print(str(mood))
  cursor.execute("INSERT INTO " + str(id) + " (date, year, month_number, month_name, day, day_name, mood) VALUES('" + today_date + "', '" + year + "', " + str(month_number) + ", '" + month_name + "', " + str(day) + ", '" + day_name + "', " + str(mood) + ") ON DUPLICATE KEY UPDATE mood=" + str(mood))
  mydb.commit()