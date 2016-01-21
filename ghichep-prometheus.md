### Các bước cài đặt

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


### Cài đặt `Node Exporter` để giám sát CPU, RAM, DISK I/O ...

- Tạo thư mục `/root/Prometheus/node_exporter`
```sh
mkdir -p ~/Prometheus/node_exporter
cd ~/Prometheus/node_exporter
```

- Tải `node_exporter-0.11.0.linux-amd64.tar.gz`
```sh
wget https://github.com/prometheus/node_exporter/releases/download/0.11.0/node_exporter-0.11.0.linux-amd64.tar.gz -O ~/Downloads/node_exporter-0.11.0.linux-amd64.tar.gz
```



















