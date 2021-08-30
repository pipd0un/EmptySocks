import threading
import logging
class Helper:
    def __init__(self,format) -> None:
        self.__FORMAT = format

    def utf8len(self,msg):
        return str(len(msg.encode(self.__FORMAT))).encode(self.__FORMAT)
        # formatted length(string) of formatted msg(string)

class MyThread(threading.Thread):

    def run(self):
        logging.debug('running')
        return