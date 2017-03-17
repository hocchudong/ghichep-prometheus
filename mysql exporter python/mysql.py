#!/usr/bin/env python

import MySQLdb as mdb
import sys

host = sys.argv[1]
user = sys.argv[2]
password = 'some_password'

con = mdb.connect(host, user, password);
cur = con.cursor(mdb.cursors.DictCursor)
cur.execute('show slave status')
slave_status = cur.fetchone()
slave_file = slave_status["Seconds_Behind_Master"]
slave_sql_running = "1" if slave_status["Slave_SQL_Running"] == "Yes" else "0"
slave_io_running = "1" if slave_status["Slave_IO_Running"] == "Yes" else "0"
print "seconds:" + slave_file + " slave_io_running:" + slave_io_running + " slave_sql_running:" + slave_sql_running