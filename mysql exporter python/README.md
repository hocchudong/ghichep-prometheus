# MySQL exporter for prometheus
# 1. Prerequisites
- Install python3
```sh
apt-get install python3
```

- Install pip3
```sh
apt-get install python3-pip
```

- Install prometheus client:
```sh
pip3 install prometheus_client
```

- Install prometheus
```sh
pip3 install prometheus
```

- Install mysqlclient
```sh
apt-get install python3-dev libmysqlclient-dev
pip3 install mysqlclient
```
- Install psutil
```sh
pip3 install psutil
```

# 2. Run
```sh
wget https://raw.githubusercontent.com/linhlt247/networking-team/master/LinhLT/Prometheus%2Bgrafana/mysql%20exporter%20python/exporter.py
python3 exporter.py
```
Metrics will export where: **http://ipaddress_server:4444/metrics**

Demo: 

![](http://image.prntscr.com/image/c3a75c2e82444d4caa0065a5793bdab1.png)

# 3. Config prometheus

```sh
- job_name: test
    static_configs:
    - targets: ['localhost:4444']
      labels:
        instance: test
        alias: test
```

# 4. Reference
https://prometheus.io/docs/introduction/overview/

https://github.com/prometheus/client_python

https://github.com/PyMySQL/mysqlclient-python

https://mysqlclient.readthedocs.io/en/latest/index.html

https://etl.svbtle.com/mysql-replication-slave-monitoring-script-for-zenoss

https://kb.paessler.com/en/topic/39913-how-can-i-monitor-mysql-replication-on-a-linux-machine

https://github.com/slok/prometheus-python