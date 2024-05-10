import asyncio
import const

async def handle_client(reader, writer):
    data = await reader.read(const.MAX_BYTES)
    print(data)

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', const.LISTEN_PORT)
    print('Server start! Listen on port:', const.LISTEN_PORT)

    async with server:
        await server.serve_forever()

asyncio.run(main())