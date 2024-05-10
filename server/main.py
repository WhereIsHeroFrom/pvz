import asyncio
import const
import json
import sys
import os

current_path = os.path.abspath(__file__)
top_path = "\\".join(current_path.split('\\')[:-2])
sys.path.append(top_path)
from share.const import *
from game import *

g = Game()

async def handle_client(reader, writer):
    data = await reader.read(const.MAX_BYTES)
    msg = json.loads(data.decode())
    print(msg)

    s2cmsg = None
    if msg['type'] == C2S_ADD_FLOWER:
        s2cmsg = g.checkAddPlant(msg['pos'])

    writer.write(json.dumps(s2cmsg).encode())
    await writer.drain()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', const.LISTEN_PORT)
    print('Server start! Listen on port:', const.LISTEN_PORT)

    async with server:
        await server.serve_forever()

asyncio.run(main())