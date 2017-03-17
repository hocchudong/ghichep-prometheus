# Set the python path
import MySQLdb as mdb
import inspect
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

import threading
from http.server import HTTPServer
import socket
import time

from prometheus.collectors import Gauge
from prometheus.registry import Registry
from prometheus.exporter import PrometheusMetricHandler
import psutil

PORT_NUMBER = 4444
host="127.0.0.1"
port=3305
user="root"
password="Welcome123"

def gather_data(registry):
    """Gathers the metrics"""

    # Get the host name of the machine
    host = socket.gethostname()

    # Create our collectors
    mysql_seconds_behind_master = Gauge("mysql_slave_seconds_behind_master", "MySQL slave secons behind master",
                                        {'host': host})
    mysql_io_running = Gauge("mysql_slave_io_running", "MySQL slave IO Running",
                                        {'host': host})
    mysql_sql_running = Gauge("mysql_slave_sql_running", "MySQL slave SQL Running",
                                        {'host': host})

    # register the metric collectors
    registry.register(mysql_seconds_behind_master)
    registry.register(mysql_io_running)
    registry.register(mysql_sql_running)

    # Connect to mysql
    con = mdb.connect(host=host, port=port, user=user, passwd=password);
    cur = con.cursor(mdb.cursors.DictCursor)

    # Start gathering metrics every second
    while True:
        time.sleep(1)

        # Get replication infomation
        cur.execute('show slave status')
        slave_status = cur.fetchone()
        slave_file = slave_status["Seconds_Behind_Master"]
        slave_sql_running = 1 if slave_status["Slave_SQL_Running"] == "Yes" else 0
        slave_io_running = 1 if slave_status["Slave_IO_Running"] == "Yes" else 0
        #con.close()

        #Add metrics
        mysql_seconds_behind_master.set({},slave_file)
        mysql_io_running.set({},slave_io_running)
        mysql_sql_running.set({},slave_sql_running)

if __name__ == "__main__":

    # Create the registry
    registry = Registry()

    # Create the thread that gathers the data while we serve it
    thread = threading.Thread(target=gather_data, args=(registry, ))
    thread.start()

    # Set a server to export (expose to prometheus) the data (in a thread)
    try:
        # We make this to set the registry in the handler
        def handler(*args, **kwargs):
            PrometheusMetricHandler(registry, *args, **kwargs)

        server = HTTPServer(('', PORT_NUMBER), handler)
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
        thread.join()