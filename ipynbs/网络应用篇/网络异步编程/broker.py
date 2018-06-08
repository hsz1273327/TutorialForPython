import json
import asyncio

subscribers = {}


class Exchange:

    def error_hander(self, query, msg):
        print("error")
        answer = {
            "TYPE": "E",
            "QTYPE": query.get("TYPE"),
            "CHANNEL": query.get("CHANNEL"),
            "COMMAND": query.get("COMMAND"),
            "ERROR_MESSAGE": msg
        }
        self.client_writer.write(json.dumps(answer).encode() + b'##END##')

    async def handler(self, query):
        if query["COMMAND"] == "LC":
            channel = subscribers.get(query["CHANNEL"])
            if channel and len(channel) > 0:
                chanlen = len(channel)
                channel.discard(self.client_writer)
                newchanlen = len(channel)
                if chanlen == newchanlen:
                    self.error_hander(query, "leave channel fail")
                    return False

                if newchanlen == 0:
                    del subscribers[query["CHANNEL"]]
                answer = {
                    "TYPE": "R",
                    "COMMAND": "LC",
                    "CHANNEL": query["CHANNEL"],
                    "CNUM": newchanlen
                }
                self.client_writer.write(
                    json.dumps(answer).encode() + b'##END##')
                return True
            else:
                self.error_hander(query, "channel is empty")
                return False

        elif query["COMMAND"] == "JC":
            channel = subscribers.get(query["CHANNEL"])
            if channel:
                channel.add(self.client_writer)
            else:
                subscribers[query["CHANNEL"]] = set([self.client_writer])

            answer = {
                "TYPE": "R",
                "COMMAND": "JC",
                "CHANNEL": query["CHANNEL"],
                "CNUM": len(subscribers[query["CHANNEL"]])
            }
            self.client_writer.write(json.dumps(answer).encode() + b'##END##')
            return True

        elif query["COMMAND"] == "PUB":
            channel = subscribers.get(query["CHANNEL"])
            if channel:
                answer = {"TYPE": "PUB",
                          "CHANNEL": query["CHANNEL"],
                          "MSG": query["MSG"]
                          }
                for subscriber in channel:
                    subscriber.write(json.dumps(answer).encode() + b'##END##')
            else:
                self.error_hander(query, "Unknow channel")
                return False
        else:
            self.error_hander(query, "Unknow COMMAND")
            return False

    async def client_connected_cb(self, client_reader, client_writer):
        self.client_reader = client_reader
        self.client_writer = client_writer
        while True:                
            try:
                data = await client_reader.readuntil(separator=b'##END##')
            except asyncio.streams.IncompleteReadError as re:
                print("client closed")
                self.client_writer.close()
                for _,channel in subscribers.items():
                    channel.discard(self.client_writer)
                print('client clear')
                break
            except:
                raise
            else:
                query = json.loads(data[:-7].decode())
                if query["TYPE"] == "Q":
                    await self.handler(query)
                else:
                    self.error_hander(query, "Unknow Type")
        self.client_writer.close()

    def run(self, host="127.0.0.1", port=5001, loop=None):
        coro = asyncio.start_server(
            self.client_connected_cb, host=host, port=port, loop=loop)
        server = loop.run_until_complete(coro)
        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(loop.shutdown_asyncgens())


if __name__ == "__main__":
    app = Exchange()
    loop = asyncio.get_event_loop()
    app.run(loop=loop)
