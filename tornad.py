import tornado.ioloop
import tornado.web
import numpy as np
import numpy.random as random
import json
import time
import os.path
from tornado import ioloop, web, websocket
from tornado.websocket import WebSocketClosedError

x = np.arange(0,10,0.1).tolist()
y = []
data_size = len(x)
counter = 0
graph_size = 2000

samples = 0
tic = time.time()

def get_graph_data():

    global counter,data_size,graph_size,x,y
    global samples,tic

    #Calculate FPS
    samples += 1
    if (time.time() - tic) > 2:
        print ("FPS is : ",samples /(time.time() - tic))
        samples = 0
        tic = time.time()
    
    counter += 1
    if counter > (data_size - graph_size):
        counter = 0

    graph_to_send = json.dumps({
        'x':x[counter:counter+graph_size],
        'y':y[counter:counter+graph_size]
    })
    if len(y)>=len(x):
        y = (2 * random.random_sample(6) - 1).tolist()
    return graph_to_send


class TestHandler(web.RequestHandler):
    def get(self):
        server = ioloop.IOLoop.current()
        data = get_graph_data()

        server.add_callback(DefaultWebSocket.send_message, data)
        self.set_status(200)
        self.finish()


class DefaultWebSocket(websocket.WebSocketHandler):
    live_web_sockets = set()

    def check_origin(self, origin):
        return True
    
    def open(self):
        try:
            self.set_nodelay(True)
            self.live_web_sockets.add(self)
            self.write_message("you've been connected. Congratz.")

        except WebSocketClosedError: 
            self.live_web_sockets.remove(self)

    def isfloat(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def on_message(self, message):
        try:
            if message!='get-data':
                list = message.split(',')
                for l in list:
                    if self.isfloat(l): y.append(float(l))
            print(message)
            [client.write_message(get_graph_data()) for client in self.live_web_sockets]
                #self.send_message(get_graph_data())

        except WebSocketClosedError:
            self.live_web_sockets.remove(self)

    def on_close(self):
        self.live_web_sockets.remove(self)
        return

    

def serve_forever(port=9998, address=''):
    application = web.Application([
            (r"/send_graph", DefaultWebSocket),
            (r"/websocket/", DefaultWebSocket),
        ],
        #static_path=os.path.join(SERVER_FOLDER, ...),
        #debug=True,
    )
    application.listen(9998)#, '127.0.0.1')
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    serve_forever()
