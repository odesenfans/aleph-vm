# Avoid failures linked to nftables when initializing the global VmPool object
import os
os.environ["ALEPH_VM_ALLOW_VM_NETWORKING"] = "False"

from vm_supervisor.conf import resolvectl_dns_servers


def test_resolvectl_ipv6(mocker):
    with mocker.patch(
        "vm_supervisor.conf._call_resolvectl_dns",
        return_value=b"Link 2 (eth0): 109.88.203.3 62.197.111.140 2a02:2788:fff0:7::3\n        2a02:2788:fff0:5::140\n",
    ):
        dns_servers = set(resolvectl_dns_servers("eth0"))
        assert dns_servers == {"109.88.203.3", "62.197.111.140"}
