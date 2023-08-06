import traceback
import sys
import inspect
import collections
from generated import openfeed_api_pb2
from generated import openfeed_pb2
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time


class OpenfeedClient(object):

    def __init__(self, username, password, server="openfeed.aws.barchart.com", debug=False):
        self.server = server
        self.username = username
        self.password = password
        self.debug = debug
        self.ws = websocket.WebSocket()
        self.token = None

        self.instrument_definitions = {}
        self.instruments_by_symbol = {}
        self.snapshots = {}

        self.symbol_handlers = {}
        self.exchange_handlers = {}
        self.heartbeat_handlers = []

        self.on_connected = None
        self.on_disconnected = None
        self.on_error = None

        websocket.enableTrace(self.debug)

    def start(self, blocking=True):
        if self.token is None:
            if blocking is not True:
                thread.start_new_thread(self.__connect, ())
            else:
                self.__connect()

    def stop(self):
        if self.token is not None:
            self.__reset()

    def add_heartbeat_subscription(self, callback):
        self.heartbeat_handlers.append(callback)

    def add_symbol_subscription(self, symbol, callback, service='REAL_TIME', subscription_type=['QUOTE']):
        symbols = []

        if isinstance(symbol, list) == False:
            symbols = [symbol]
        else:
            symbols = symbol

        for sym in symbols:
            if sym not in self.symbol_handlers:
                self.symbol_handlers[sym] = []

            self.symbol_handlers[sym].append(
                Listener(sym, callback, service=service, subscription_type=subscription_type))

        if self.token is not None:
            self._send_message(
                self.__create_subscription_request([], symbols, service, subscription_type))

    def add_exchange_subscription(self, exchange, callback, service='REAL_TIME', subscription_type=['QUOTE']):
        exchanges = []

        if isinstance(exchange, list) == False:
            exchanges = [exchange]
        else:
            exchanges = exchange

        for exch in exchanges:
            if exch not in self.exchange_handlers:
                self.exchange_handlers[exch] = []

            self.exchange_handlers[exch].append(Listener(
                exch, callback, service=service, subscription_type=subscription_type, is_exchange=True))

        if self.token is not None:
            self._send_message(
                self.__create_subscription_request(exchanges, [], service, subscription_type))

    def get_instrument_definitions(self):
        return self.instrument_definitions

    def get_instrument_definition(self, id):
        return self.instrument_definitions[id]

    def get_instrument_definition_by_symbol(self, symbol):
        return self.instruments_by_symbol[symbol]

    def _send_message(self, msg):
        if self.debug:
            print("Sending:", msg)
        self.ws.send(msg.SerializeToString(), websocket.ABNF.OPCODE_BINARY)

    def __reset(self):
        self.ws.close()
        self.token = None
        self.ws = websocket.WebSocket()

    def __connect(self):

        def handleLogin(msg):

            if msg.loginResponse.status.result > 1:
                raise Exception("Login has failed: ", msg)

            self.token = msg.loginResponse.token
            self.__send_existing_interest()

            return msg

        def handleHeartbeat(msg):
            self.__notify_heartbeat_listeners(msg)
            return msg

        def handleSubscriptionResponse(msg):

            if msg.subscriptionResponse.status.result > 1:
                raise Exception("Subscription has failed: ", msg)

            if len(msg.subscriptionResponse.symbol) > 0:
                self.__notify_symbol_listeners(
                    msg.subscriptionResponse.symbol, msg)
            else:
                self.__notify_exchange_listeners(
                    msg.subscriptionResponse.exchange, msg)

            return msg

        def handleInstrumentDefinition(msg):
            self.instrument_definitions[msg.instrumentDefinition.marketId] = msg
            self.instruments_by_symbol[msg.instrumentDefinition.symbol] = msg

            return msg

        def handleMarketUpdate(msg):
            inst = self.instrument_definitions[msg.marketUpdate.marketId].instrumentDefinition

            self.__notify_exchange_listeners(inst.barchartExchangeCode, msg)
            self.__notify_symbol_listeners(inst, msg)

            return msg

        def handleMarketSnapshot(msg):
            inst = self.instrument_definitions[msg.marketSnapshot.marketId].instrumentDefinition

            self.snapshots[inst.marketId] = msg

            self.__notify_exchange_listeners(inst.barchartExchangeCode, msg)
            self.__notify_symbol_listeners(inst, msg)

            return msg

        def handleOHLC(msg):
            inst = self.instrument_definitions[msg.ohlc.marketId].instrumentDefinition

            self.__notify_exchange_listeners(inst.barchartExchangeCode, msg)
            self.__notify_symbol_listeners(inst, msg)

        handlers = {
            "loginResponse": handleLogin,
            "heartBeat": handleHeartbeat,
            "subscriptionResponse": handleSubscriptionResponse,
            "instrumentDefinition": handleInstrumentDefinition,
            "marketSnapshot": handleMarketSnapshot,
            "marketUpdate": handleMarketUpdate,
            "ohlc": handleOHLC
        }

        def on_message(ws, message):

            msg = openfeed_api_pb2.OpenfeedGatewayMessage()
            msg.ParseFromString(message)

            msg_type = msg.WhichOneof("data")

            handler = handlers.get(
                msg_type, lambda x: print("Unhandled Message: ", x))

            try:
                handler(msg)
            except Exception as e:
                if self.debug:
                    print("Failed handling incoming message:", msg_type, e)
                self.__callback(self.on_error, e)

        def on_error(ws, error):
            if self.debug:
                print("WS Error: ", error)
                traceback.print_exc()
            self.__callback(self.on_error, error)

        def on_close(ws):
            if self.debug:
                print("WS Close")

            self.__reset()
            self.__callback(self.on_disconnected, ws)

        def on_open(ws):
            if self.debug:
                print("WS Open")

            self._send_message(self.__create_login_request())
            self.__callback(self.on_connected, ws)

        self.ws = websocket.WebSocketApp("ws://" + self.server + "/ws",
                                         on_message=on_message,
                                         on_error=on_error,
                                         on_close=on_close,
                                         on_open=on_open)

        self.ws.run_forever()

    def __notify_symbol_listeners(self, instrument, msg):

        # TODO review symbology handling, subbing by one and keying off the other can create unexpected results
        # for example subscribing to "ZCYAIA40.CM" will come back with OF symbol (less the suffix) in `instrument.symbol`
        # given the below, if the instrument contains duplicate `instrument.symbols`, the listeners will get duplicate callbacks

        for s in instrument.symbols:
            if s.symbol not in self.symbol_handlers:
                return

            for cb in self.symbol_handlers[s.symbol]:
                try:
                    cb.callback(msg)
                except Exception as e:
                    if self.debug:
                        print("Failed to notify `symbol` callback", s, e)
                    self.__callback(self.on_error, e)

    def __notify_exchange_listeners(self, exchange, msg):
        if exchange not in self.exchange_handlers:
            return

        for cb in self.exchange_handlers[exchange]:
            try:
                cb.callback(msg)
            except Exception as e:
                if self.debug:
                    print("Failed to notify `exchange` callback", e)
                self.__callback(self.on_error, e)

    def __notify_heartbeat_listeners(self, msg):
        for cb in self.heartbeat_handlers:
            try:
                cb(msg)
            except Exception as e:
                if self.debug:
                    print("Failed to notify `heartbeat` callback", e)
                self.__callback(self.on_error, e)

    def __send_existing_interest(self):
        all_listeners = list(self.symbol_handlers.values()) + \
            list(self.exchange_handlers.values())

        interest = {
            'SYMBOL': {
                'REAL_TIME': {},
                'DELAYED': {}
            },
            'EXCHANGE': {
                'REAL_TIME': {},
                'DELAYED': {}
            }
        }

        # group symbols / exchanges by subscription_type
        for listeners in all_listeners:
            for l in listeners:
                syms = interest[l.key()][l.service]
                if l.symbol_or_exchange not in syms:
                    syms[l.symbol_or_exchange] = Listener(
                        l.symbol_or_exchange, None, service=l.service, subscription_type=l.subscription_type)
                else:
                    existing = syms[l.symbol_or_exchange]
                    existing.subscription_type = list(set(
                        existing.subscription_type + l.subscription_type))

        for service in ['REAL_TIME', 'DELAYED']:
            for i in interest['SYMBOL'][service].values():
                req = self.__create_subscription_request(
                    [], [i.symbol_or_exchange], service=service, subscriptionType=i.subscription_type)
                self._send_message(req)
            for i in interest['EXCHANGE'][service].values():
                self._send_message(self.__create_subscription_request(
                    [i.symbol_or_exchange], [], service=service, subscriptionType=i.subscription_type))

    def __create_subscription_request(self, exchanges, symbols, service='REAL_TIME', subscriptionType=['QUOTE']):
        requests = []

        if len(exchanges) > 0:
            for exch in exchanges:
                requests.append(openfeed_api_pb2.SubscriptionRequest.Request(
                    exchange=exch,
                    subscriptionType=[openfeed_api_pb2.SubscriptionType.Value(
                        t) for t in subscriptionType],
                    snapshotIntervalSeconds=60
                ))

        if len(symbols) > 0:
            for sym in symbols:
                requests.append(openfeed_api_pb2.SubscriptionRequest.Request(
                    symbol=sym,
                    subscriptionType=[openfeed_api_pb2.SubscriptionType.Value(
                        t) for t in subscriptionType],
                    snapshotIntervalSeconds=60
                ))

        of_req = openfeed_api_pb2.OpenfeedGatewayRequest(
            subscriptionRequest=openfeed_api_pb2.SubscriptionRequest(
                token=self.token,
                service=openfeed_pb2.Service.Value(service),
                requests=requests
            ))

        return of_req

    def __create_login_request(self):
        return openfeed_api_pb2.OpenfeedGatewayRequest(
            loginRequest=openfeed_api_pb2.LoginRequest(
                username=self.username, password=self.password))

    def __callback(self, callback, *args):
        try:
            if callback is not None:
                callback(*args)
        except Exception as e:
            print("Failed to call callback", e)


class Listener(object):
    def __init__(self, symbol_or_exchange, callback, service='REAL_TIME', subscription_type=['QUOTE'], is_exchange=False):
        self.symbol_or_exchange = symbol_or_exchange
        self.callback = callback
        self.service = service
        self.subscription_type = subscription_type
        self.is_exchange = is_exchange

    def key(self):
        if self.is_exchange:
            return 'EXCHANGE'
        return 'SYMBOL'

    def has_same_interest(self, other_listener):
        return collections.Counter(self.subscription_type) == collections.Counter(other_listener.subscription_type)


if __name__ == "__main__":

    def handle_message(msg):
        print("of-client: Market Data: ", msg.WhichOneof("data"))

    def handle_heartbeat(msg):
        print("of-client: Heartbeat: ", msg)

    of_client = OpenfeedClient("username", "password", debug=False)

    of_client.add_exchange_subscription(
        exchange="FOREX", callback=handle_message)
    of_client.add_heartbeat_subscription(callback=handle_heartbeat)

    of_client.on_error = lambda x: print("of-client: something went wrong:", x)
    of_client.on_disconnected = lambda x: print("of-client: disconnected")
    of_client.on_connected = lambda x: print("of-client: connected")

    # blocking mode
    of_client.start(blocking=False)

    while True:
        print("Number of Instruments:", len(
            of_client.get_instrument_definitions()))
        time.sleep(10)
