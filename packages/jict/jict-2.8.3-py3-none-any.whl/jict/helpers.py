from time import time
from threading import Thread
import os, json, yaml, re
from bson.objectid import ObjectId
from collections import deque


def walk( path , regx , depth = 10 ):
    myf = []
    for r , _, files in os.walk( path ):
        if r[len(path):].count(os.sep) < depth:

            if len( files ) == 0:
                continue

            for f in files:
                fl = os.path.join(r,f)
                if bool(re.search(regx , fl )):
                    myf.append( fl )

    return myf

class cycle:
    __pos__ = -1
    def __init__( self , *args, **kwargs ):
        if len(args) != 0:
            if callable(args[0]):
                self.reload = True
                self.__argsf__ = args[0]
                return
        self.__args__ = args

    def __getitem__(self, n ):
        if self.reload:
            self.__args__ = self.__argsf__()

        n += self.__pos__
        v = n % (len( self.__args__ ))
        self.__pos__ += 1
        return self.__args__[v]

def evaluate( foo, itter = 1 , threaded = False ):
    if threaded == True:
        def threadedfoo():
            Thread(target = lambda: evaluate(foo,itter) ).start()

        threadedfoo()
        return

    t0 = time()
    for _ in range( itter ):
        foo()

    print( time() - t0, "seconds wall time" )

def sqlconnect(str):
    import mysql.connector # or from mysql import connector

    user,pawd,host,database = re.findall(
        "(.*):(.*)@([0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}):(.*)"
    , str )[0]

    cnt = mysql.connector.connect(
        host     = host,
        database = database,
        user     = user,
        password = pawd
    )

    return cnt


class jsonencoder( json.JSONEncoder ):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, deque):
            return list(o)
        try:
            return json.JSONEncoder.default(self, o)
        except:
            return str(o)

def loader(nd, ext):
    text = open( nd, "r+" ).read()
    data = {}
    if text.strip() == '':
        return data
    if ext == '.yaml':
        data = yaml.safe_load( text )
    elif ext == '.json':
        data = json.loads( text )
    return data

def file( *args, **kwargs ):
    dirname = os.path.dirname(filestr)
    if os.path.isfile( filestr ):
        return open( *args, **kwargs )

    else:
        if not os.path.exists( dirname ):
            os.makedirs( dirname )

        f = open( *args, **kwargs )
        f.write("")
        f.close()

    return open( *args, **kwargs )

def threadedlist( lista , rang, slep ):
    thread_list = []

    for x in lista:
        th = Thread( target = x[0] , args=x[1] )
        thread_list.append(th)

        if len(thread_list) >= rang :
            for x in thread_list:
                x.start()
            while len([t for t in thread_list if t.is_alive()]) != 0:
                sleep( slep )
            thread_list = []

    for x in thread_list:
        x.start()
    while len([t for t in thread_list if t.is_alive()]) != 0:
        sleep( slep )
