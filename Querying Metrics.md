#Querying Metrics

=================

* Prometheus cung cấp ngôn ngữ thể hiện (Expression language) để lựu chọn và tổng hợp time series data với thời gian thực. 

* Kết quả trả về có thể view như một biểu đồ, bảng hoặc sử dụng bởi các hệ thống khác thông qua HTTP API.

* Có 4 loại metrics:

	- Instant vector: `http_requests_total{job="prometheus",group="canary"}`
	- Range vector: `http_requests_total{job="prometheus"}[5m]`
	- Scalar: Một simple numeric
	- String: 

https://prometheus.io/docs/querying/basics/

### Các toán tử

<ul>
<li>+ (addition)
<li>- (subtraction)
<li>* (multiplication)
<li>/ (division)
<li>% (modulo)
<li>^ (power/exponentiation)
<li>== (equal)
<li>!= (not-equal)
<li>> (greater-than)
<li>< (less-than)
<li>>= (greater-or-equal)
<li><= (less-or-equal)
<li>and (intersection)
<li>or (union)
<li>unless (complement)
<li>sum (calculate sum over dimensions)
<li>min (select minimum over dimensions)
<li>max (select maximum over dimensions)
<li>avg (calculate the average over dimensions)
<li>stddev (calculate population standard deviation over dimensions)
<li>stdvar (calculate population standard variance over dimensions)
<li>count (count number of elements in the vector)
<li>count_values (count number of elements with the same value)
<li>bottomk (smallest k elements by sample value)
<li>topk (largest k elements by sample value)
<li>quantile (calculate φ-quantile (0 ≤ φ ≤ 1) over dimensions)
<ul>

**Ví dụ:**

- Trả về time series của http_requests_total với 2 nhãn bên trong
```sh
http_requests_total{job="apiserver", handler="/api/comments"}
```

- Giới hạn trong 5'
```sh
http_requests_total{job="apiserver", handler="/api/comments"}[5m]
```

- Kết thúc của job là server
```sh
http_requests_total{job=~"server$"}
```

- Loại bỏ status 4xx
```sh
http_requests_total{status!~"^4..$"}
```

- Nhóm các thông số xác định bởi `by`
```sh
sum(node_cpu)  by (cpu)
```

- Mức độ cached
```sh
(node_memory_Cached /1024)/1024
```
- Trừ 2 giá trị metrics
```sh
(instance_memory_limit_bytes - instance_memory_usage_bytes) / 1024 / 1024
```

- %CPU user
```sh
sum(rate(node_cpu{job='node',instance='localhost:9100',mode='user'}[5m])) * 100 / count(count by (cpu)(node_cpu{job='node',instance='localhost:9100'}))
```

- &CPU system
```sh
sum(rate(node_cpu{job='node',instance='localhost:9100',mode='system'}[5m])) * 100 / count(count by (cpu)(node_cpu{job='node',instance='localhost:9100'}))
```

- %CPU
```sh
100 * (1 - avg by(instance)(rate(node_cpu{job='node',mode='idle',instance='localhost:9100'}[5m])))
```

- Memory total
```sh
node_memory_MemTotal{job='node',instance='localhost:9100'}
```

- Memory free
```sh
node_memory_MemFree{job='node',instance='localhost:9100'}
```

- Network receive
```sh
rate(node_network_receive_bytes{job='node',instance='localhost:9100',device='eth0'}[5m])
```

- % disk / use 
```sh
100 - node_filesystem_free{job='node',instance='localhost:9100',mountpoint='/'} / node_filesystem_size{job='node'} * 100
```

### Function

https://prometheus.io/docs/querying/functions/

### Các metrics của node_exporter

- node_cpu: Seconds the cpus spent in each mode.
- node_disk_io:_now The number of I/Os currently in progress.
- node_disk_io_time_ms: Milliseconds spent doing I/Os.
- node_disk_io_time_weighted: The weighted # of milliseconds spent doing I/Os.
- node_disk_read_time_ms: The total number of milliseconds spent by all reads.
- node_disk_reads_completed: The total number of reads completed successfully.
- node_disk_reads_merged: The number of reads merged.
- node_disk_sectors_read: The total number of sectors read successfully.
- node_disk_sectors_written: The total number of sectors written successfully.
- node_disk_writes_completed: The total number of writes completed successfully.

===========================================

- node_filesystem_avail: Filesystem space available to non-root users in bytes.
- node_filesystem_files: Filesystem total file nodes.
- node_filesystem_files:_free Filesystem total free file nodes.
- node_filesystem_free: Filesystem free space in bytes.
- node_filesystem_size: Filesystem size in bytes.

============================================

- node_memory_Active: Active from /proc/meminfo.
- node_load1: 1m load average.
- node_memory_Buffers: Buffers from /proc/meminfo.
- node_memory_Cached: Cached from /proc/meminfo.
- node_memory_MemFree: MemFree from /proc/meminfo.
- node_memory_MemAvailable: MemAvailable from /proc/meminfo.
- node_memory_SwapCached: SwapCached from /proc/meminfo.
- node_memory_SwapFree: SwapFree from /proc/meminfo.
- node_memory_SwapTotal: SwapTotal from /proc/meminfo.

============================================

- node_network_receive_bytes: bytes receive from /proc/net/dev.
- node_network_receive_compressed: compressed receive from /proc/net/dev.
- node_network_receive_drop: drop receive from /proc/net/dev.
- node_network_receive_errs: errs receive from /proc/net/dev.
- node_network_transmit_bytes: bytes transmit from /proc/net/dev.

============================================

- node_time: System time in seconds since epoch (1970).
- process_cpu_seconds_total: Total user and system CPU time spent in seconds.



































































