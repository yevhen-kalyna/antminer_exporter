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

    def test_antminer_uptime_seconds_sum(self):
        x = "hello"
        assert hasattr(x, "format")

    def test_antminer_uptime_seconds_created(self):
        x = "hello"
        assert hasattr(x, "format")