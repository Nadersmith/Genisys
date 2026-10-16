import asyncio
import binascii
from datetime import datetime

class Inspector:
    def __init__(self, core):
        self.core = core
        self.queue = asyncio.Queue()
        self.running = False

    async def start(self):
        if not self.running:
            self.running = True
            asyncio.create_task(self._printer())

    async def inspect_packet(self, pkt: bytes, info: dict):
        # enqueue summary for live monitoring
        item = {
            "time": datetime.utcnow().isoformat(),
            "len": len(pkt),
            "info": info,
            "hex": binascii.hexlify(pkt[:128]).decode()  # sample hex dump
        }
        await self.queue.put(item)

    async def _printer(self):
        while True:
            item = await self.queue.get()
            print(f"[{item['time']}] len={item['len']} info={item['info']}")
            # for production, you can forward to a websocket/web UI
