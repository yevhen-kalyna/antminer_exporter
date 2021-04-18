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

### Run emulation of AntMiner

* Docker required
* Fill up `config.yaml` with your machine IP address

Build and run image

```bash
docker build -f tests/antminer_emulator/Dockerfile -t antminer_exporter/antminer_emulator tests/antminer_emulator

docker run -d -p 80:80 antminer_exporter/antminer_emulator
```

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

### Tests

All functions and metrics should have tests for them.

#### Tests example

`tests/test_metrics.py`

```python3
import requests

def get_metrics() -> requests.Response:
    return requests.request('GET', 'http://localhost:8000')
    
def test_get_metrics():
    assert get_metrics().status_code == 200

class TestAntminerUptimeSeconds:
    def test_antminer_uptime_seconds_count(self):
        r = get_metrics().text.split('\n')
        subs = 'antminer_uptime_seconds_count'
        res = [i for i in r if subs in i]
        assert subs in res[0]
```
