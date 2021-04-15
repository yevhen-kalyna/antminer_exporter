# antminer_exporter

Prometheus exporter for AntMiner

## Development

### Install dependencies

System dependencies

```bash
sudo apt install python3.9 python3.9-dev -y
```

Virtual Environment

```bash
pip3 install pipenv
```

Install python dependencies

```bash
pipenv install --dev
```

Activate virtual environment

```bash
pipenv shell
```

Reload VS Code and set Python Interpretor for it

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
