from flask import Blueprint
import redis
import gevent

ws = Blueprint('ws',__name__,url_prefix='/ws')

# connect to the redis
redis = redis.from_url('redis://127.0.0.1:6379')

class Chatroom(object):
    def __init__(self):
        self.clients = []
        # initiate pubsub system
        self.pubsub = redis.pubsub()
        # subscribe chat channel
        self.pubsub.subscribe('chat')

    def register(self,client):
        self.clients.append(client)

    def send(self,client,data):
        # send message to every clients
        try:
            client.send(data.decode('utf-8'))
        except:
            # colud be the client no longer exists,delete from list
            self.clients.remove(client)

    def run(self):
        # send received message to every clients by order
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message.get('data')
                for client in self.clients:
                    # using gevent asynchronous send message
                    gevent.spawn(self.send,client,data)

    def start(self):
        # asynchronous run the self.run()
        gevent.spawn(self.run)

# initiate the chat room
chat = Chatroom()
# asynchronous run the room
chat.start()

@ws.route('/send')
def inbox(ws):# using flask-sockets, what ws linked objects will be automatically inject into route functions
    while not ws.closed:
        message = ws.receive()

        if message:
            # send the message to the chat channel
            redis.publish('chat',message)

@ws.route('/recv')
def outbox(ws):
    chat.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)
