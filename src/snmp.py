from typing import Dict, List, Tuple
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

def collect_status(host: str, community: str, oids: List[str], timeout: int = 2, retries: int = 1) -> Dict[str, str]:
    results: Dict[str, str] = {}
    if not oids:
        return results
    for oid in oids:
        error_indication, error_status, error_index, var_binds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(community, mpModel=1),  # SNMPv2c
                UdpTransportTarget((host, 161), timeout=timeout, retries=retries),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
            )
        )
        if error_indication or error_status:
            results[oid] = f"ERROR:{error_indication or error_status.prettyPrint()}"
        else:
            for varBind in var_binds:
                oid_str, val = [x.prettyPrint() for x in varBind]
                results[oid_str] = val
    return results
