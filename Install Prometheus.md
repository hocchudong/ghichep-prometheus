#Install Prometheus

Mục lục:
==========

[1. Cài đặt Prometheus](#1)

[2. Cài đặt `Node Exporter` để giám sát CPU, RAM, DISK I/O ...](#2)

[3. Cài đặt PromDash](#2)

[Chú ý](#c)

Mô hình cài đặt:

<img src=http://i.imgur.com/kueaHCm.png>

Môi trường cài đặt:

- 1 máy server ubuntu-14.04 cài đặt dịch vụ Prometheus server, Node_exporter, PromDash
- Card mạng ra ngoài Internet để tải các gói cài đặt
- 1 máy client cài đặt Node_exporter để gửi thông tin về server (Chưa triển khai)

Có thể truy cập https://prometheus.io/download/ để tải các gói cài đặt hoặc dùng lệnh wget

<a name="1"></a>
###1. Cài đặt Prometheus
- Tạo thư mục để download bộ cài 

```sh
mkdir ~/Downloads
cd ~/Downloads
```

- Tải file cài đặt (01/11/2016) Version 1.2.3

```sh
wget "https://github.com/prometheus/prometheus/releases/download/v1.2.3/prometheus-1.2.3.linux-amd64.tar.gz"
```

- Giải nén bộ cài Prometheus
```sh
tar -xvzf ~/Downloads/prometheus-1.2.3.linux-amd64.tar.gz -C ~/Prometheus
``` 

- Đổi tên thư mục vừa giải nén
```sh
mv ~/Prometheus/prometheus-1.2.3.linux-amd64 ~/Prometheus/server
```

- Vào thư mục và thực hiện lệnh cài đặt 
```sh
cd ~/Prometheus/server
./prometheus -version
```

- Kết quả lệnh trên sẽ như sau
```sh
prometheus, version 1.2.3 (branch: master, revision: c1eee5b0da2540b9dfd2f70752015b0fce83b616)
  build user:       root@d8eb84e17a12
  build date:       20161103-21:45:14
  go version:       go1.7.3
```

<a name="2"></a>
###2. Cài đặt `Node Exporter` để giám sát CPU, RAM, DISK I/O ...

- Tải `node_exporter-0.13.0-rc.1.linux-amd64.tar.gz` về thư mục  `/root/Downloads`
```sh
wget https://github.com/prometheus/node_exporter/releases/download/v0.13.0-rc.1/node_exporter-0.13.0-rc.1.linux-amd64.tar.gz -O ~/Downloads/node_exporter-0.13.0-rc.1.linux-amd64.tar.gz
```

- Giải nén sang thư mục `/root/Prometheus`
```sh
tar -xvzf ~/Downloads/node_exporter-0.13.0-rc.1.linux-amd64.tar.gz -C /root/Prometheus
```

- Đổi tên thư mục vừa giải nén

```sh
mv /root/Prometheus/node_exporter-0.13.0-rc.1.linux-amd64 /root/Prometheus/node_exporter
```

- Tạo soft link cho node_exporter 
```sh
ln -s ~/Prometheus/node_exporter/node_exporter /usr/bin
```

- Tạo file `/etc/init/node_exporter.conf` với nội dung dưới
```sh
# Run node_exporter

start on startup

script
   /usr/bin/node_exporter
end script
```

- Khởi động `node_exporter`
```sh
service node_exporter start
```

- Mở web với địa chỉ của máy chủ cài Prometheus `http://your_server_ip:9100/metrics` sẽ thấy kết quả dưới
```sh
# HELP go_gc_duration_seconds A summary of the GC invocation durations.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 0
go_gc_duration_seconds{quantile="0.25"} 0
go_gc_duration_seconds{quantile="0.5"} 0
go_gc_duration_seconds{quantile="0.75"} 0
go_gc_duration_seconds{quantile="1"} 0
go_gc_duration_seconds_sum 0
go_gc_duration_seconds_count 0
# HELP go_goroutines Number of goroutines that currently exist.
# TYPE go_goroutines gauge
go_goroutines 11
......
```

- Khởi động `prometheus` cùng OS 
```sh
nohup ./prometheus > prometheus.log 2>&1 &
```

- Kết quả sau khi khởi động cùng OS
```sh
[1] 1410 

- Lưu ý, số trên sẽ thay đổi tùy lần chạy.
```

- Kiểm tra file log của prometheus
```sh
tail ~/Prometheus/server/prometheus-1.2.3.linux-amd64/prometheus.log
```

- Kết quả của file log
```sh
time="2016-11-05T10:59:44+07:00" level=info msg="Starting prometheus (version=1.2.3, branch=master, revision=c1eee5b0da2540b9dfd2f70752015b0fce83b616)" source="main.go:75"
time="2016-11-05T10:59:44+07:00" level=info msg="Build context (go=go1.7.3, user=root@d8eb84e17a12, date=20161103-21:45:14)" source="main.go:76"
time="2016-11-05T10:59:44+07:00" level=info msg="Loading configuration file prometheus.yml" source="main.go:247"
time="2016-11-05T10:59:44+07:00" level=info msg="Loading series map and head chunks..." source="storage.go:354"
time="2016-11-05T10:59:44+07:00" level=info msg="0 series loaded." source="storage.go:359"
time="2016-11-05T10:59:44+07:00" level=info msg="Listening on :9090" source="web.go:240"
time="2016-11-05T10:59:44+07:00" level=warning msg="No AlertManagers configured, not dispatching any alerts" source="notifier.go:176"
time="2016-11-05T10:59:44+07:00" level=info msg="Starting target manager..." source="targetmanager.go:76"
```

- Truy cập vào web của prometheus với URL: http://your_server_ip:9090 or http://your_server_ip:9090/consoles/node.html

<img src=http://i.imgur.com/wdBl8Qp.png>

<img src=http://i.imgur.com/Y6l8ru1.png>

<a name="3"></a>
###3. Cài đặt PromDash

- Di chuyển vào /root/Prometheus`
```sh
cd ~/Prometheus
```

- `PromDash` viết bằng Ruby & Rails do vậy cần cài đặt các gói bổ trợ 
```sh
apt-get update && sudo apt-get install git ruby bundler libsqlite3-dev sqlite3 zlib1g-dev
```

- Tải `PromDash`
```sh
git clone https://github.com/prometheus/promdash.git
```

- Di chuyển vào thư mục `promdash` vừa tải về
```sh
cd ~/Prometheus/promdash
```

- Cài `promdash` và sử dụng SQLite3 và không sử dụng MySQL và PostgreSQL
```sh
bundle install --without mysql postgresql
```

<img src=http://i.imgur.com/ze1sRsV.png>

- Copy file database
```sh
cp ~/Prometheus/promdash/config/database.yml.example ~/Prometheus/promdash/config/database.yml
```

- Đặt biến môi trường và tạo database

```sh
RAILS_ENV=development bundle exec rake db:setup
```

<img src=http://i.imgur.com/C02gtR3.png>

- Start the Rails server

```sh
bundle exec rails s
```

<img src=http://i.imgur.com/Whbfjon.png>

- Truy cập vào web với địa chỉ `http://your_server_ip:3000/`

<img src=http://i.imgur.com/VqpyRC6.png>

<a name="c"></a>
###Chú ý: 

Khi reboot server

- Ko vào được web http://your_server_ip:9090/

```sh
Truy cập vào thư mục ~/Prometheus/server
Xóa file prometheus.log
Chạy command **nohup ./prometheus > prometheus.log 2>&1 &** để server tạo ra file prometheus.log mới
```

- Ko vào được PromDash

```sh
Chạy command `bundle exec rails s` trong thư mục ~/Prometheus/promdash
```


**Tham khảo:**

[1]- https://www.digitalocean.com/community/tutorials/how-to-use-prometheus-to-monitor-your-ubuntu-14-04-server

[2]- https://github.com/prometheus/promdash











