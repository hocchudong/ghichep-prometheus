#Install Prometheus

Mục lục:
==========

[1. Cài đặt Prometheus](#1)

[2. Cài đặt Node_Exporter để giám sát CPU, RAM, DISK I/O ...](#2)

[3. Cài đặt PromDash](#3)

[4. Cài đặt Node_Exporter trên client](#4)

[Chú ý](#c)

Mô hình cài đặt:

<img src=http://i.imgur.com/kueaHCm.png>

Môi trường cài đặt:

- 1 máy server ubuntu-14.04 cài đặt dịch vụ Prometheus server, Node_exporter, PromDash
- Card mạng ra ngoài Internet để tải các gói cài đặt
- 1 máy client cài đặt Node_exporter để gửi thông tin về server

Có thể truy cập https://prometheus.io/download/ để tải các gói cài đặt hoặc dùng lệnh wget

<a name="1"></a>
###1. Cài đặt Prometheus

- Tạo thư mục cài đặt
```sh
mkdir -p Prometheus
```

- Tạo thư mục để download bộ cài 
```sh
mkdir ~/Downloads
cd ~/Downloads
```

- Tải file cài đặt Version 1.2.3
```sh
wget https://github.com/prometheus/prometheus/releases/download/v1.2.3/prometheus-1.2.3.linux-amd64.tar.gz
```

- Giải nén bộ cài Prometheus
```sh
tar -xvzf ~/Downloads/prometheus-1.2.3.linux-amd64.tar.gz  -C ~/Prometheus
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

- Sửa file cấu hình `prometheus.yml`
```sh
cd ~/Prometheus/server/
vim prometheus.yml
```

- Sửa file theo ví dụ bên dưới:
```sh
scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['10.10.10.21:9100']
```

- Khởi động `prometheus`
```sh
cd ~/Prometheus/server/
nohup ./prometheus > prometheus.log 2>&1 &
```

- Kết quả
```sh
[1] 1410 

- Lưu ý, số trên sẽ thay đổi tùy lần chạy.
```

- Kiểm tra file log của prometheus
```sh
tail ~/Prometheus/server/prometheus.log
```

- Kết quả của file log
```sh
root@prometheus:~/Prometheus/server# tailf prometheus.log
time="2016-11-10T15:13:58+07:00" level=info msg="Cleaning up archive indexes." file=crashrecovery.go line=359
time="2016-11-10T15:13:58+07:00" level=info msg="Clean-up of archive indexes complete." file=crashrecovery.go line=447
time="2016-11-10T15:13:58+07:00" level=info msg="Rebuilding label indexes." file=crashrecovery.go line=455
time="2016-11-10T15:13:58+07:00" level=info msg="Indexing metrics in memory." file=crashrecovery.go line=456
time="2016-11-10T15:13:58+07:00" level=info msg="Indexing archived metrics." file=crashrecovery.go line=464
time="2016-11-10T15:13:58+07:00" level=info msg="All requests for rebuilding the label indexes queued. (Actual processing may lag behind.)" file=crashrecovery.go line=483
time="2016-11-10T15:13:58+07:00" level=warning msg="Crash recovery complete." file=crashrecovery.go line=141
time="2016-11-10T15:13:58+07:00" level=info msg="495 series loaded." file=storage.go line=268
time="2016-11-10T15:13:58+07:00" level=info msg="Starting target manager..." file=targetmanager.go line=75
time="2016-11-10T15:13:58+07:00" level=info msg="Listening on :9090" file=web.go line=186

```

- Truy cập vào web của prometheus với URL: http://your_server_ip:9090 or http://your_server_ip:9090/consoles/node.html

<img src=http://i.imgur.com/wdBl8Qp.png>

<img src=http://i.imgur.com/Y6l8ru1.png>

<a name="3"></a>
###3. Cài đặt PromDash

- Di chuyển vào `/root/Prometheus`
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

<a name="4"></a>
###4. Cài đặt Node_Exporter trên client

- Tạo thư mục cài đặt
```sh
mkdir -p Prometheus
```

- Tạo thư mục để download bộ cài 
```sh
mkdir ~/Downloads
cd ~/Downloads
```
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

- Chỉnh sửa file prometheus.yml trên server

Thêm các thông số cho client:

```sh
scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['prometheus:9090']
      - targets: ['prometheus:9100']
      - targets: ['prometheus-client:9100']
```

- Khởi động lại dịch vụ prometheus trên server

- Truy cập http://your_server_ip:9090

<img src=http://i.imgur.com/4wB0ygk.png>

<a name="c"></a>
###Chú ý: 

Khi reboot server

- Ko vào được web http://your_server_ip:9090/

```sh
cd ~/Prometheus/server
./prometheus
```

- Ko vào được PromDash

```sh
Chạy command `bundle exec rails s` trong thư mục ~/Prometheus/promdash
```


**Tham khảo:**

[1]- https://www.digitalocean.com/community/tutorials/how-to-use-prometheus-to-monitor-your-ubuntu-14-04-server

[2]- https://github.com/prometheus/promdash











