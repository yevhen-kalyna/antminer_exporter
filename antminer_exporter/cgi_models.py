# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = system_info_from_dict(json.loads(json_string))

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, TypeVar, Callable, Type, cast
import dateutil.parser
from prometheus_client import CollectorRegistry
from prometheus_client.metrics import Info
import requests
from requests.auth import HTTPDigestAuth
from exceptions import KernelLogError
import re
from loguru import logger

class Miner:
    def __init__(self, ip: str, cgi_user: str = 'root', cgi_password: str = 'root'):
        self.ip = ip
        self.cgi_user = cgi_user
        self.cgi_password = cgi_password
        self.miner_conf = miner_conf_from_dict(self.get_request('cgi-bin/get_miner_conf.cgi').json())
        self.miner_status = miner_status_from_dict(self.get_request('cgi-bin/get_miner_status.cgi').json())
        self.network_info = network_info_from_dict(self.get_request('cgi-bin/get_network_info.cgi').json())
        self.system_info = system_info_from_dict(self.get_request('cgi-bin/get_system_info.cgi').json())

    def get_request(self, route: str) -> requests.Response:
        url = f'http://{self.ip}/{route}'
        response = requests.request('GET', url, auth=HTTPDigestAuth(self.cgi_user, self.cgi_password))
        return response
    
    def is_alive(self) -> bool:
        for i in range(2):
            try:
                if self.miner_status.pools[i].status == 'Alive':
                    self._is_alive = True
            except:
                self._is_alive = False
                continue
        # self.create_metrics()
        return self._is_alive
    
    #TODO: prometheus metrics inside miner instance (self monitoring)
    def create_metrics(self):
        pass

    def get_kernel_log(self) -> list:
        return self.get_request('cgi-bin/get_kernel_log.cgi').text.split('\n')

    def verify_kernel_log(self):
        for l in self.get_kernel_log():  
            if re.findall(r'(?<![\w\d])(error|err|ERR|ERROR)(?![\w\d])', l):
                logger.error(l)
            elif re.findall(r'(?<![\w\d])(warn|warning|WARN|WARNING)(?![\w\d])', l):
                logger.warning(l)

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x

def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class SystemInfo:
    minertype: str
    nettype: str
    netdevice: str
    macaddr: str
    hostname: str
    ipaddress: str
    netmask: str
    gateway: str
    dnsservers: str
    curtime: datetime
    uptime: str
    loadaverage: str
    mem_total: int
    mem_used: int
    mem_free: int
    mem_buffers: int
    mem_cached: int
    system_mode: str
    ant_hwv: str
    system_kernel_version: str
    system_filesystem_version: str
    cgminer_version: str

    @staticmethod
    def from_dict(obj: Any) -> 'SystemInfo':
        assert isinstance(obj, dict)
        minertype = from_str(obj.get("minertype"))
        nettype = from_str(obj.get("nettype"))
        netdevice = from_str(obj.get("netdevice"))
        macaddr = from_str(obj.get("macaddr"))
        hostname = from_str(obj.get("hostname"))
        ipaddress = from_str(obj.get("ipaddress"))
        netmask = from_str(obj.get("netmask"))
        gateway = from_str(obj.get("gateway"))
        dnsservers = from_str(obj.get("dnsservers"))
        curtime = from_datetime(obj.get("curtime"))
        uptime = from_str(obj.get("uptime"))
        loadaverage = from_str(obj.get("loadaverage"))
        mem_total = int(from_str(obj.get("mem_total")))
        mem_used = int(from_str(obj.get("mem_used")))
        mem_free = int(from_str(obj.get("mem_free")))
        mem_buffers = int(from_str(obj.get("mem_buffers")))
        mem_cached = int(from_str(obj.get("mem_cached")))
        system_mode = from_str(obj.get("system_mode"))
        ant_hwv = from_str(obj.get("ant_hwv"))
        system_kernel_version = from_str(obj.get("system_kernel_version"))
        system_filesystem_version = from_str(obj.get("system_filesystem_version"))
        cgminer_version = from_str(obj.get("cgminer_version"))
        return SystemInfo(minertype, nettype, netdevice, macaddr, hostname, ipaddress, netmask, gateway, dnsservers, curtime, uptime, loadaverage, mem_total, mem_used, mem_free, mem_buffers, mem_cached, system_mode, ant_hwv, system_kernel_version, system_filesystem_version, cgminer_version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["minertype"] = from_str(self.minertype)
        result["nettype"] = from_str(self.nettype)
        result["netdevice"] = from_str(self.netdevice)
        result["macaddr"] = from_str(self.macaddr)
        result["hostname"] = from_str(self.hostname)
        result["ipaddress"] = from_str(self.ipaddress)
        result["netmask"] = from_str(self.netmask)
        result["gateway"] = from_str(self.gateway)
        result["dnsservers"] = from_str(self.dnsservers)
        result["curtime"] = self.curtime.isoformat()
        result["uptime"] = from_str(self.uptime)
        result["loadaverage"] = from_str(self.loadaverage)
        result["mem_total"] = from_str(str(self.mem_total))
        result["mem_used"] = from_str(str(self.mem_used))
        result["mem_free"] = from_str(str(self.mem_free))
        result["mem_buffers"] = from_str(str(self.mem_buffers))
        result["mem_cached"] = from_str(str(self.mem_cached))
        result["system_mode"] = from_str(self.system_mode)
        result["ant_hwv"] = from_str(self.ant_hwv)
        result["system_kernel_version"] = from_str(self.system_kernel_version)
        result["system_filesystem_version"] = from_str(self.system_filesystem_version)
        result["cgminer_version"] = from_str(self.cgminer_version)
        return result

@dataclass
class MinerConfPool:
    url: str
    user: str
    pool_pass: int

    @staticmethod
    def from_dict(obj: Any) -> 'MinerConfPool':
        assert isinstance(obj, dict)
        url = from_str(obj.get("url"))
        user = from_str(obj.get("user"))
        pool_pass = int(from_str(obj.get("pass")))
        return MinerConfPool(url, user, pool_pass)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_str(self.url)
        result["user"] = from_str(self.user)
        result["pass"] = from_str(str(self.pool_pass))
        return result


@dataclass
class MinerConf:
    pools: List[MinerConfPool]
    api_listen: bool
    api_network: bool
    api_groups: str
    api_allow: str
    bitmain_use_vil: bool
    bitmain_freq: str
    bitmain_voltage: int

    @staticmethod
    def from_dict(obj: Any) -> 'MinerConf':
        assert isinstance(obj, dict)
        pools = from_list(MinerConfPool.from_dict, obj.get("pools"))
        api_listen = from_bool(obj.get("api-listen"))
        api_network = from_bool(obj.get("api-network"))
        api_groups = from_str(obj.get("api-groups"))
        api_allow = from_str(obj.get("api-allow"))
        bitmain_use_vil = from_bool(obj.get("bitmain-use-vil"))
        bitmain_freq = from_str(obj.get("bitmain-freq"))
        bitmain_voltage = int(from_str(obj.get("bitmain-voltage")))
        return MinerConf(pools, api_listen, api_network, api_groups, api_allow, bitmain_use_vil, bitmain_freq, bitmain_voltage)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pools"] = from_list(lambda x: to_class(MinerConfPool, x), self.pools)
        result["api-listen"] = from_bool(self.api_listen)
        result["api-network"] = from_bool(self.api_network)
        result["api-groups"] = from_str(self.api_groups)
        result["api-allow"] = from_str(self.api_allow)
        result["bitmain-use-vil"] = from_bool(self.bitmain_use_vil)
        result["bitmain-freq"] = from_str(self.bitmain_freq)
        result["bitmain-voltage"] = from_str(str(self.bitmain_voltage))
        return result


@dataclass
class Dev:
    index: int
    chain_acn: int
    freq: str
    fan: int
    temp: int
    chain_acs: str

    @staticmethod
    def from_dict(obj: Any) -> 'Dev':
        assert isinstance(obj, dict)
        index = int(from_str(obj.get("index")))
        chain_acn = int(from_str(obj.get("chain_acn")))
        freq = from_str(obj.get("freq"))
        fan = int(from_str(obj.get("fan")))
        temp = int(from_str(obj.get("temp")))
        chain_acs = from_str(obj.get("chain_acs"))
        return Dev(index, chain_acn, freq, fan, temp, chain_acs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["index"] = from_str(str(self.index))
        result["chain_acn"] = from_str(str(self.chain_acn))
        result["freq"] = from_str(self.freq)
        result["fan"] = from_str(str(self.fan))
        result["temp"] = from_str(str(self.temp))
        result["chain_acs"] = from_str(self.chain_acs)
        return result


@dataclass
class Pool:
    index: int
    url: str
    user: str
    status: str
    priority: int
    getworks: int
    accepted: int
    rejected: int
    discarded: int
    stale: int
    diff: str
    diff1: int
    diffa: str
    diffr: str
    diffs: str
    lsdiff: str
    lstime: str

    @staticmethod
    def from_dict(obj: Any) -> 'Pool':
        assert isinstance(obj, dict)
        index = int(from_str(obj.get("index")))
        url = from_str(obj.get("url"))
        user = from_str(obj.get("user"))
        status = from_str(obj.get("status"))
        priority = int(from_str(obj.get("priority")))
        getworks = int(from_str(obj.get("getworks")))
        accepted = int(from_str(obj.get("accepted")))
        rejected = int(from_str(obj.get("rejected")))
        discarded = int(from_str(obj.get("discarded")))
        stale = int(from_str(obj.get("stale")))
        diff = from_str(obj.get("diff"))
        diff1 = int(from_str(obj.get("diff1")))
        diffa = from_str(obj.get("diffa"))
        diffr = from_str(obj.get("diffr"))
        diffs = from_str(obj.get("diffs"))
        lsdiff = from_str(obj.get("lsdiff"))
        lstime = from_str(obj.get("lstime"))
        return Pool(index, url, user, status, priority, getworks, accepted, rejected, discarded, stale, diff, diff1, diffa, diffr, diffs, lsdiff, lstime)

    def to_dict(self) -> dict:
        result: dict = {}
        result["index"] = from_str(str(self.index))
        result["url"] = from_str(self.url)
        result["user"] = from_str(self.user)
        result["status"] = from_str(self.status)
        result["priority"] = from_str(str(self.priority))
        result["getworks"] = from_str(str(self.getworks))
        result["accepted"] = from_str(str(self.accepted))
        result["rejected"] = from_str(str(self.rejected))
        result["discarded"] = from_str(str(self.discarded))
        result["stale"] = from_str(str(self.stale))
        result["diff"] = from_str(self.diff)
        result["diff1"] = from_str(str(self.diff1))
        result["diffa"] = from_str(self.diffa)
        result["diffr"] = from_str(self.diffr)
        result["diffs"] = from_str(self.diffs)
        result["lsdiff"] = from_str(self.lsdiff)
        result["lstime"] = from_str(self.lstime)
        return result


@dataclass
class Summary:
    elapsed: int
    ghs5_s: str
    ghsav: str
    foundblocks: int
    getworks: int
    accepted: int
    rejected: int
    hw: int
    utility: str
    discarded: int
    stale: int
    localwork: int
    wu: str
    diffa: str
    diffr: str
    diffs: str
    bestshare: int

    @staticmethod
    def from_dict(obj: Any) -> 'Summary':
        assert isinstance(obj, dict)
        elapsed = int(from_str(obj.get("elapsed")))
        ghs5_s = from_str(obj.get("ghs5s"))
        ghsav = from_str(obj.get("ghsav"))
        foundblocks = int(from_str(obj.get("foundblocks")))
        getworks = int(from_str(obj.get("getworks")))
        accepted = int(from_str(obj.get("accepted")))
        rejected = int(from_str(obj.get("rejected")))
        hw = int(from_str(obj.get("hw")))
        utility = from_str(obj.get("utility"))
        discarded = int(from_str(obj.get("discarded")))
        stale = int(from_str(obj.get("stale")))
        localwork = int(from_str(obj.get("localwork")))
        wu = from_str(obj.get("wu"))
        diffa = from_str(obj.get("diffa"))
        diffr = from_str(obj.get("diffr"))
        diffs = from_str(obj.get("diffs"))
        bestshare = int(from_str(obj.get("bestshare")))
        return Summary(elapsed, ghs5_s, ghsav, foundblocks, getworks, accepted, rejected, hw, utility, discarded, stale, localwork, wu, diffa, diffr, diffs, bestshare)

    def to_dict(self) -> dict:
        result: dict = {}
        result["elapsed"] = from_str(str(self.elapsed))
        result["ghs5s"] = from_str(self.ghs5_s)
        result["ghsav"] = from_str(self.ghsav)
        result["foundblocks"] = from_str(str(self.foundblocks))
        result["getworks"] = from_str(str(self.getworks))
        result["accepted"] = from_str(str(self.accepted))
        result["rejected"] = from_str(str(self.rejected))
        result["hw"] = from_str(str(self.hw))
        result["utility"] = from_str(self.utility)
        result["discarded"] = from_str(str(self.discarded))
        result["stale"] = from_str(str(self.stale))
        result["localwork"] = from_str(str(self.localwork))
        result["wu"] = from_str(self.wu)
        result["diffa"] = from_str(self.diffa)
        result["diffr"] = from_str(self.diffr)
        result["diffs"] = from_str(self.diffs)
        result["bestshare"] = from_str(str(self.bestshare))
        return result


@dataclass
class MinerStatus:
    summary: Summary
    pools: List[Pool]
    devs: List[Dev]

    @staticmethod
    def from_dict(obj: Any) -> 'MinerStatus':
        assert isinstance(obj, dict)
        summary = Summary.from_dict(obj.get("summary"))
        pools = from_list(Pool.from_dict, obj.get("pools"))
        devs = from_list(Dev.from_dict, obj.get("devs"))
        return MinerStatus(summary, pools, devs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["summary"] = to_class(Summary, self.summary)
        result["pools"] = from_list(lambda x: to_class(Pool, x), self.pools)
        result["devs"] = from_list(lambda x: to_class(Dev, x), self.devs)
        return result


@dataclass
class NetworkInfo:
    nettype: str
    netdevice: str
    macaddr: str
    ipaddress: str
    netmask: str
    conf_nettype: str
    conf_hostname: str
    conf_ipaddress: str
    conf_netmask: str
    conf_gateway: str
    conf_dnsservers: str

    @staticmethod
    def from_dict(obj: Any) -> 'NetworkInfo':
        assert isinstance(obj, dict)
        nettype = from_str(obj.get("nettype"))
        netdevice = from_str(obj.get("netdevice"))
        macaddr = from_str(obj.get("macaddr"))
        ipaddress = from_str(obj.get("ipaddress"))
        netmask = from_str(obj.get("netmask"))
        conf_nettype = from_str(obj.get("conf_nettype"))
        conf_hostname = from_str(obj.get("conf_hostname"))
        conf_ipaddress = from_str(obj.get("conf_ipaddress"))
        conf_netmask = from_str(obj.get("conf_netmask"))
        conf_gateway = from_str(obj.get("conf_gateway"))
        conf_dnsservers = from_str(obj.get("conf_dnsservers"))
        return NetworkInfo(nettype, netdevice, macaddr, ipaddress, netmask, conf_nettype, conf_hostname, conf_ipaddress, conf_netmask, conf_gateway, conf_dnsservers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nettype"] = from_str(self.nettype)
        result["netdevice"] = from_str(self.netdevice)
        result["macaddr"] = from_str(self.macaddr)
        result["ipaddress"] = from_str(self.ipaddress)
        result["netmask"] = from_str(self.netmask)
        result["conf_nettype"] = from_str(self.conf_nettype)
        result["conf_hostname"] = from_str(self.conf_hostname)
        result["conf_ipaddress"] = from_str(self.conf_ipaddress)
        result["conf_netmask"] = from_str(self.conf_netmask)
        result["conf_gateway"] = from_str(self.conf_gateway)
        result["conf_dnsservers"] = from_str(self.conf_dnsservers)
        return result


def network_info_from_dict(s: Any) -> NetworkInfo:
    return NetworkInfo.from_dict(s)


def miner_status_from_dict(s: Any) -> MinerStatus:
    return MinerStatus.from_dict(s)


def miner_conf_from_dict(s: Any) -> MinerConf:
    return MinerConf.from_dict(s)


def system_info_from_dict(s: Any) -> SystemInfo:
    return SystemInfo.from_dict(s)


