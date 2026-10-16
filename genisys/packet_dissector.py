import struct

class PacketDissector:
    def parse(self, buf: bytes) -> dict:
        info = {}
        # minimal IPv4/UDP/TCP detection (extendable)
        if len(buf) < 1:
            return info
        ver = buf[0] >> 4
        if ver == 4:
            info['ip_version'] = 4
            # extract protocol from IPv4 header (byte 9)
            if len(buf) >= 20:
                proto = buf[9]
                info['protocol'] = proto
                # UDP = 17, TCP = 6, ICMP = 1
                if proto == 17:
                    info['is_udp'] = True
                    # rudimentary DNS detection: UDP dest port 53
                    src_port, dst_port = struct.unpack("!HH", buf[20:24])
                    if dst_port == 53 or src_port == 53:
                        info['is_dns'] = True
                elif proto == 6:
                    info['is_tcp'] = True
                    # detect TLS ClientHello SNI in payload (very simplified)
                    payload = buf[20 + 20:]  # naive: skip IP+TCP header (no options handling)
                    sni = self._extract_sni(payload)
                    if sni:
                        info['tls_sni'] = sni
        elif ver == 6:
            info['ip_version'] = 6
            # parse IPv6 / extension headers omitted for brevity
        return info

    def _extract_sni(self, payload: bytes) -> str:
        # Very simplified TLS ClientHello SNI finder: scan for bytes "server_name" in payload.
        try:
            if b"server_name" in payload:
                # naive extraction - realistic parsing requires TLS record+handshake parsing
                start = payload.find(b"server_name")
                # back-scan for nearby ASCII domain (heuristic)
                segment = payload[start-100:start+200]
                import re
                m = re.search(rb"[a-z0-9.-]+\.[a-z]{2,}", segment, re.I)
                if m:
                    return m.group(0).decode()
        except Exception:
            pass
        return ""
