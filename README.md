# antminer_exporter

Prometheus exporter for AntMiner

## Metrics

### Check endpoint

1. Run app
2. Go to `http://localhost:8000/`

### Metics example

#### Uptime

```text
# HELP antminer_uptime_seconds General uptime of miner in seconds
# TYPE antminer_uptime_seconds summary
antminer_uptime_seconds_count 1.0
antminer_uptime_seconds_sum 9000.0
# HELP antminer_uptime_seconds_created General uptime of miner in seconds
# TYPE antminer_uptime_seconds_created gauge
antminer_uptime_seconds_created 1.6174733872678773e+09
```
