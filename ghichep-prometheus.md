### Các bước cài đặt

#### Cài đặt Prometheus
- Tạo thư mục để download bộ cài 

```sh
mkdir ~/Downloads
cd ~/Downloads
```

- Tải file cài đặt mới nhất (21/01/2016) Version Prometheus 0.16.2

```sh
wget "https://github.com/prometheus/prometheus/releases/download/0.16.2/prometheus-0.16.2.linux-amd64.tar.gz"
```

- Tạo thư mục `/Prometheus/server` trong thư mục `/root`

```sh
mkdir -p ~/Prometheus/server
```

- Di chuyển vào thư mục vừa tạo ở trên 
```sh
cd ~/Prometheus/server
```

- Giải nén bộ cài Prometheus
```sh
tar -xvzf ~/Downloads/prometheus-0.16.2.linux-amd64.tar.gz
```

- Di chuyển vào thư mục vừa giải nén
```sh
cd ~/Prometheus/server/prometheus-0.16.2.linux-amd64
```

- Thực hiện lệnh cài đặt 
```sh
./prometheus -version
```

- Kết quả lệnh trên sẽ như sau
```sh
prometheus, version 0.16.2 (branch: release-0.16, revision: 287d9b2)
  build user:       fabianreinartz@macpro
  build date:       20160118-13:10:31
  go version:       1.5.3
```


#### Cài đặt `Node Exporter` để giám sát CPU, RAM, DISK I/O ...

- Tạo thư mục `/root/Prometheus/node_exporter`
```sh
mkdir -p ~/Prometheus/node_exporter
cd ~/Prometheus/node_exporter
```

- Tải `node_exporter-0.11.0.linux-amd64.tar.gz` về thư mục  `/root/Prometheus`
```sh
wget https://github.com/prometheus/node_exporter/releases/download/0.11.0/node_exporter-0.11.0.linux-amd64.tar.gz -O ~/Downloads/node_exporter-0.11.0.linux-amd64.tar.gz
```

- Giải nén `node_exporter-0.11.0.linux-amd64.tar.gz` vào thư mục hiện tại là `/root/Prometheus/node_exporter`
```sh
tar -xvzf ~/Downloads/node_exporter-0.11.0.linux-amd64.tar.gz
```

- Tạo soft link cho node_exporter 
```sh
sudo ln -s ~/Prometheus/node_exporter/node_exporter /usr/bin
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
sudo service node_exporter start
```

- Mở web với địa chỉ của máy chủ cài Prometheus `http://your_server_ip:9100/metrics` sẽ thấy kết quả dưới
```sh
# HELP go_gc_duration_seconds A summary of the GC invocation durations.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 0.00029520400000000003
go_gc_duration_seconds{quantile="0.25"} 0.000324071
go_gc_duration_seconds{quantile="0.5"} 0.0006052060000000001
go_gc_duration_seconds{quantile="0.75"} 0.0013162150000000001
go_gc_duration_seconds{quantile="1"} 0.0018389020000000001
go_gc_duration_seconds_sum 0.005879231
go_gc_duration_seconds_count 7
# HELP go_goroutines Number of goroutines that currently exist.
# TYPE go_goroutines gauge
go_goroutines 13

......
```

- Tạo file `/root/Prometheus/server/prometheus-0.16.2.linux-amd64/prometheus.yml` với nội dung dưới
```sh
scrape_configs:
  - job_name: "node"
    scrape_interval: "15s"
    target_groups:
    - targets: ['localhost:9100']
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
tail ~/Prometheus/server/prometheus-0.16.2.linux-amd64/prometheus.log
```

- Kết quả của file log
```sh
prometheus, version 0.16.2 (branch: release-0.16, revision: 287d9b2)
  build user:       fabianreinartz@macpro
  build date:       20160118-13:10:31
  go version:       1.5.3
time="2016-01-21T21:54:46+07:00" level=info msg="Loading configuration file prometheus.yml" source="main.go:196" 
time="2016-01-21T21:54:46+07:00" level=info msg="Loading series map and head chunks..." source="storage.go:268" 
time="2016-01-21T21:54:46+07:00" level=info msg="0 series loaded." source="storage.go:273" 
time="2016-01-21T21:54:46+07:00" level=info msg="Starting target manager..." source="targetmanager.go:114" 
time="2016-01-21T21:54:46+07:00" level=info msg="Listening on :9090" source="web.go:220" 
```

- Truy cập vào web của prometheus với URL: http://your_server_ip:9090


- Truy cập vào http://IP_SRV_PROMETHEUS:9090/consoles/node.html để xem các thông số về RAM/CPU


#### Cài đặt `PromDash`

- Di chuyển vào /root/Prometheus`
```sh
cd ~/Prometheus
```

- `PromDash` viết bằng Ruby & Rails do vậy cần cài đặt các gói bổ trợ 
```sh
sudo apt-get update && sudo apt-get install git ruby bundler libsqlite3-dev sqlite3 zlib1g-dev
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

- Kết quả sẽ như sau
```sh
Your bundle is complete!
Gems in the groups mysql and postgresql were not installed.
Use `bundle show [gemname]` to see where a bundled gem is installed.
Post-install message from rdoc:
```

- Tạo thư mục để lưu trữ `SQLite3`

```sh
mkdir ~/Prometheus/databases
```

- Thiết lập biến môi trường  `RAILS_ENV`
```sh
echo "export RAILS_ENV=production" >> ~/.bashrc
```

- Thực thi các biến môi trường vừa khai báo
```sh
. ~/.bashrc
```

- Tạo db
```sh
rake db:migrate

rake assets:precompile
```

- Chạy `promdash`
```sh
bundle exec thin start -d
```

- Truy cập vào web với địa chỉ `http://your_server_ip:3000/`

#### Tham khảo:

1. https://www.digitalocean.com/community/tutorials/how-to-use-prometheus-to-monitor-your-ubuntu-14-04-server











