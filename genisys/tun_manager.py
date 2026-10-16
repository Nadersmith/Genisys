import asyncio
import os
import fcntl
import struct

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_NO_PI = 0x1000

class TunManager:
    def __init__(self, name="genisys0", mtu=1500):
        self.name = name
        self.mtu = mtu
        self.fd = None
        self.loop = asyncio.get_event_loop()

    async def create(self):
        # requires CAP_NET_ADMIN or root
        self.fd = os.open("/dev/net/tun", os.O_RDWR)
        ifr = struct.pack('16sH', self.name.encode(), IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(self.fd, TUNSETIFF, ifr)
        # configure interface externally (ip addr add / ip link set up)
        return self.name

    async def read_packet(self):
        # read in executor to avoid blocking event loop
        return await self.loop.run_in_executor(None, os.read, self.fd, self.mtu)

    async def write_packet(self, data):
        return await self.loop.run_in_executor(None, os.write, self.fd, data)
