#!/usr/bin/python3
# =====================
# EEL5713 Final Project
#   Testing Framework
# =====================
# Author: Yuxuan Zhang
from mininet.net import Host

active_qperf_server: Host = None


def qperf_server(host: Host):
    """Start a qperf server on the host"""
    global active_qperf_server
    if active_qperf_server == host:
        return
    if active_qperf_server is not None:
        jobs = active_qperf_server.cmd("jobs", "-p")
        active_qperf_server.cmd("kill", jobs)
    host.cmd("qperf &")
    active_qperf_server = host


def parse_qperf(output: str):
    result = {}
    for line in output.split("\n"):
        seg_v = line.split("=")
        if len(seg_v) != 2:
            continue
        key, val = [seg.strip() for seg in seg_v]
        if len(val.split(" ")) >= 2:
            val, unit = val.split(" ")[:2]
            result[key] = (float(val.replace(",", "")), unit)
        else:
            result[key] = (float(val.replace(",", "")), None)
    return result


def test_icmp(server: Host, client: Host, count=10, interval=0.02):
    """ICMP Ping latency test"""
    output = client.cmd("ping", server.IP(), "-c", count, "-i", interval)
    # Find rtt min/avg/max/mdev from string output
    PREAMBLE = "rtt min/avg/max/mdev ="
    for line in output.split("\n"):
        if line.strip().startswith(PREAMBLE):
            val, unit = line.split("=")[1].strip().split(" ")[:2]
            val = float(val.split("/")[1])
            assert unit == "ms", unit
            assert val >= 0, val
            return val
    # No match found, raise error
    raise ValueError("Unexpected ping result:", output, sep="\n")


def test_tcp_udp(server: Host, client: Host):
    """Test TCP and UDP latency and bandwidth"""
    qperf_server(server)

    output = client.cmd("qperf", "-vvs", server.IP(), "tcp_lat")
    result = parse_qperf(output)
    tcp_lat, unit = result["latency"]
    assert unit == "us", unit

    output = client.cmd("qperf", "-vvs", server.IP(), "tcp_bw")
    result = parse_qperf(output)
    tcp_bw, unit = result["bw"]
    assert str(unit).startswith("GB/s"), unit

    output = client.cmd("qperf", "-vvs", server.IP(), "udp_lat")
    result = parse_qperf(output)
    udp_lat, unit = result["latency"]
    assert unit == "us", unit

    output = client.cmd("qperf", "-vvs", server.IP(), "udp_bw")
    result = parse_qperf(output)

    udp_send_bw, unit = result["send_bw"]
    assert str(unit).startswith("GB/s"), unit
    udp_recv_bw, unit = result["recv_bw"]
    assert str(unit).startswith("GB/s"), unit
    udp_bw = (udp_send_bw + udp_recv_bw) / 2

    return tcp_lat, tcp_bw, udp_lat, udp_bw
