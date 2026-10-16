import asyncio
from .tun_manager import TunManager
from .packet_dissector import PacketDissector
from .dns_filter import DnsFilterEngine
from .inspector import Inspector

class Genisys:
    def __init__(self, tun_name="genisys0"):
        self.tun = TunManager(tun_name)
        self.dissector = PacketDissector()
        self.dns = DnsFilterEngine()
        self.inspector = Inspector(self)

    async def start(self):
        await self.tun.create()
        loop = asyncio.get_event_loop()
        loop.create_task(self._read_loop())
        await self.inspector.start()  # start local UI/CLI inspector

    async def _read_loop(self):
        while True:
            pkt = await self.tun.read_packet()
            # parse headers (non-blocking)
            info = self.dissector.parse(pkt)
            # DNS handling
            if info.get("is_dns"):
                pkt = await self.dns.handle_dns_packet(pkt, info)
            # pass to inspector for logging and possible blocking
            await self.inspector.inspect_packet(pkt, info)
            # default: write back or drop (for now we just log)
