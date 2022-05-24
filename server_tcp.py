from controller import Controller
import json
import socket
import asyncio

HOST, PORT = "localhost", 8888
 
config_path = "settings.json"
controller = Controller(config_path)

async def get(reader, writer):
    request = await reader.read(100)
    vacancy_name = request.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (vacancy_name, addr))
    
    
    controller.update(vacancy_name)
    vacancies_info = controller.create_response(refresh=False)
    vacancies_info = json.dumps(vacancies_info)
    response = vacancies_info.encode()
    writer.write(response)
    print("Send: %r/n" % vacancies_info)
    print()
    await writer.drain()
    
    #print("Close the client socket")
    writer.close()

async def main():
    server = await asyncio.start_server(
        get, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
