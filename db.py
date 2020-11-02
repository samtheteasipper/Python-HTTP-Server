#This file is only run one time
import sqlite3

conn = sqlite3.connect('speeding.db')

#Speed_limit, current_speed, is_speeding
#int, int, bool

#Create cursor object
c = conn.cursor()

#Create table:
c.execute('''CREATE TABLE speeding (id integer, speed_limit integer, current_speed integer, is_speeding integer)''')

conn.commit()

conn.close()
