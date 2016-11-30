#Alerting 

Alerting hoạt động trên Prometheus với 2 thành phần:
- Alerting rules
- Alertmanager

###1. Alerting rules

**Mô tả Alerting rules**

Alerting rules cho phép xác định các điều kiện đưa ra cảnh báo, dựa trên language expressions và gửi thông báo đi. 

```sh
ALERT <alert name>
  IF <expression>
  [ FOR <duration> ]
  [ LABELS <label set> ]
  [ ANNOTATIONS <label set> ]
```

- FOR: Chờ đợi trong 1 khoảng thời gian để đưa ra cảnh báo
- LABELS: Đặt nhãn cho cảnh báo
- ANNOTATIONS: Chứa thêm các thông tin cho cảnh báo

Ví dụ:
```sh
# Alert for any instance that is unreachable for >5 minutes.
ALERT InstanceDown
  IF up == 0
  FOR 5m
  LABELS { severity = "page" }
  ANNOTATIONS {
    summary = "Instance {{ $labels.instance }} down",
    description = "{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes.",
  }

# Alert for any instance that have a median request latency >1s.
ALERT APIHighRequestLatency
  IF api_http_request_latencies_second{quantile="0.5"} > 1
  FOR 1m
  ANNOTATIONS {
    summary = "High request latency on {{ $labels.instance }}",
    description = "{{ $labels.instance }} has a median request latency above 1s (current value: {{ $value }}s)",
  }
```

**Kiểm tra các cảnh báo đang hoạt động**

- Webside của Prometheus có tab "Alerts" show lên thông tin các alert đang hoạt động.

Alert có 2 chế độ (Pending và firing), chúng cũng đc lưu dưới dạng time series với dạng

```sh
ALERTS{alertname="<alert name>", alertstate="pending|firing", <additional alert labels>}
```

Nếu alert hoạt động sẽ có value là 1, ko hoạt động sẽ có value là 0

**Gửi thông báo**

Để gửi các thông báo đi ta cần tới thành phần **Alertmanager**

###2. Alertmanager

- AlertManager đưa ra các thông báo với chế độ như im lặng (Silencing), ức chế (Inhibition), tập hợp (Grouping) và gửi thông báo qua email...
	- Grouping: Tập hợp các thông báo giống nhau vào một cảnh báo.
	- Inhibition: Giữ lại các cảnh báo nếu một số cảnh báo khác đã được đưa ra.
	- Silencing: Tắt cảnh báo trong khoảng thời gian nhất định.


###3. Demo Alert

- Device "/" còn trống 44GB

![plugincpu](/Images/Alert-1.png)

- Tạo ra cảnh báo khi dung lượng device "/" trống ít hơn 40GB

- Tạo file alert.rules cùng thư mục chứa file prometheus.yml với nội dung bên dưới
```sh
# Alert when Disk_Free of device"/" <40 GB
ALERT Disk_Free
  IF (node_filesystem_avail{mountpoint="/"}/1024/1024/1024) < 40
  FOR 1m
  LABELS { severity = "page" }
  ANNOTATIONS {
        description = "{{ $labels.instance }} of job {{ $labels.job }} Disk space > 40GB",
  }
```

- Khai báo alert.rules trong file prometheus.yml
```sh
rule_files:
    - 'alert.rules'
```

- Khởi động lại Prometheus

- Truy cập tab "Alert" trên Webside

![plugincpu](/Images/Alert-2.png)


- Tạo file hoặc copy sao cho dung lượng device "/" trống ít hơn 40GB

Ví dụ ở đây dùng command 
```sh
fallocate -l 15G /tmp/test.img
```

- Cảnh báo

![plugincpu](/Images/Alert-3.png)
























