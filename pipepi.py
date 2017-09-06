#!flask/bin/python	

import asyncio
import requests
import logging
import json
import signal
import sys

class ClientProtocol(asyncio.Protocol):

    def __init__(self):
        self.logger = logging.getLogger('ClientProtocol')

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        ajsons = data.decode()
        d = self.find_jsons(ajsons)
        if d is None:
            error = 'Error : Incorrect json. Check data you are sending.'
            self.logger.error(error)
            self.jsonrpc_error(error)
            return 

        for beg, end  in d.items():
            try:
                jsonrpc = json.loads(ajsons[beg:end+1])
            except ValueError:
                print(ajsons)
                self.logger.error(data.decode())
                msg = ' Not valid data - requires JSONRPC'
                self.logger.error(msg)
                self.jsonrpc_error(msg)
                continue 
 
            # TODO validation
            #
            #
            if 'result' in jsonrpc:
                print("--- {} --- ".format(jsonrpc['result'])) 
                return
            elif 'error' in jsonrpc:
                print("--- {} --- ".format(jsonrpc['error'])) 
                return
            elif 'method' in jsonrpc:
                # to REST
                url = "http://127.0.0.1:5000" + jsonrpc['params']['url']
                if jsonrpc['method'] == "POST":
                    print("URL  - {}".format(url)) 
                    #print("Data - {}".format(data)) 
                    r = requests.post(url, json = jsonrpc['params']['data'])
                    print(r)

                response = '{"jsonrpc": "2.0", "id": "' + jsonrpc['id' ] + '", "result": true}'
                self.logger.info(' < Back to client {} -- true ') #.format(self._id))
                self.transport.write(response.encode())
            else:
                msg = "This error message should be not seen!";
                self.logger.error(msg)

        #print('Close the client socket')
        #self.transport.close()

    def jsonrpc_error(self, msg):
        """
        """
        replay = '{"jsonrpc": "2.0", "id": "9", "error": {"code" : 666, "message": "' + msg + '"} }'
        self.transport.write(replay.encode())

    def find_jsons(self, data):
        istart = []
        count = 0
        d = {}
        for i, c in enumerate(data):
            if c == '{':
                if count == 0:
                    istart.append(i)
                count += 1
            if c == '}':
                if count == 1:
                    try:
                        d[istart.pop()] = i
                    except IndexError:
                        print('Too many closing parentheses')
                        return None
                count -= 1
        if istart:
            print('Too many opening parentheses')
            return None
        return d

    #
    #
    #
    def back_to_client(self, data):
        self.transport.write(data)


class RestProtocol(asyncio.Protocol):

    def __init__(self, callback):
        self.back_to_client = callback         

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format('true'))
        self.transport.write('true'.encode())
 
        self.back_to_client(data)

        ##print('Close the client socket')
        #self.transport.close()


def start_pipepi():
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=1)
    signal.signal(signal.SIGINT, signal_handler)
    logger = logging.getLogger('pipepi')
 
    logger.info("------------------- START ---------------------")

    try:

        client = ClientProtocol()

        client_coro = loop.create_server(lambda: client, '127.0.0.1', 21004)
        print(' Client listener started on: {} and port {}'.format('127.0.0.1', 21004))
        logger.info(' Client listener started on: {} and port {}'.format('127.0.0.1', 21004))
        logger.info('')


        rest_coro = loop.create_server(lambda: RestProtocol(client.back_to_client), '127.0.0.1', 21003)
        logger.info(' Rest listener started on: {} and port {}'.format('127.0.0.1', 21003))
        print(' Rest listener started on: {} and port {}'.format('127.0.0.1', 21003))
        logger.info('')



        server = loop.run_until_complete(asyncio.gather(client_coro, rest_coro))
        loop.run_forever()

    finally:
        logger.info('---- closing event loop ----- Shutting dawn "PipePi" bye bye!')
        print('---- closing event loop ----- Shutting dawn "PipePi" bye bye!')
        loop.close()


def signal_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    start_pipepi()

