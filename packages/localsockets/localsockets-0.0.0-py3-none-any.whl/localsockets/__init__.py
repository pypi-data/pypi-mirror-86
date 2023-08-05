__version__ = '0.0.0'
__url__ = 'https://pypi.org/project/localsockets/'

import os
import time
import uuid
import threading

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

__path__ = os.path.dirname(os.path.abspath(__file__))

def error(name, module='builtins'):
    cls = type(name, (BaseException,), {})
    cls.__module__ = module
    return cls

ServerNotFoundError = error('ServerNotFoundError')

UPDATED = {}

SERVER_DIR = os.path.join(__path__, 'servers')

def on_created(event):
    path = os.path.basename(event.src_path)
    if path.endswith('.server'):
        id = path[:-7]
    elif path.endswith('.conn'):
        id = path[:-5]
    else:
        return
##    print(f'CREATE "{id}"')
    UPDATED[id] = False

def on_modified(event):
    path = os.path.basename(event.src_path)
    if path.endswith('.server'):
        id = path[:-7]
    elif path.endswith('.conn'):
        id = path[:-5]
    else:
        return
##    print(f'MODIFY "{id}"')
    UPDATED[id] = True

def on_deleted(event):
    path = os.path.basename(event.src_path)
    if path.endswith('.server'):
        id = path[:-7]
    elif path.endswith('.conn'):
        id = path[:-5]
    else:
        return
##    print(f'DELETE "{id}"')
    if id in UPDATED:
        del UPDATED[id]

def setup():
    #add existing servers
    for server in os.listdir(SERVER_DIR):
        id = server[:-7]
        UPDATED[id] = False
    
    patterns = '*'
    ignore_patterns = ''
    ignore_directories = True
    case_sensitive = True
    handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    handler.on_modified = on_modified
    handler.on_created = on_created
    handler.on_deleted = on_deleted
    #handler.on_moved = on_moved

    path = SERVER_DIR
    go_recursively = True
    observer = Observer()
    observer.schedule(handler, path, go_recursively)

    observer.start()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def getpath(id):
    return os.path.join(SERVER_DIR, f'{id}.server')

def getconnpath(id):
    return os.path.join(SERVER_DIR, f'{id}.conn')

def getfile(id, mode='r'):
    return open(getpath(id), mode)

def createserver(id):
    with getfile(id, 'w') as file:
        pass

def updateserver(id, data):
    with getfile(id, 'wb') as file:
        file.write(data)
        pass

def existsserver(id):
    return os.path.exists(getpath(id))

def getserver(id):
    with getfile(id, 'rb') as file:
        return file.read()

def deleteserver(id):
    os.remove(getpath(id))

class socket:
    def __init__(self, id=None):
        if not id:
            self.conn = False
            self.id = uuid.uuid4().hex
            self.open()
        else:
            self.conn = True
            if existsserver(id):
                self.id = id
                with open(getconnpath(self.id), 'w'): pass
            else:
                raise ServerNotFoundError

    def open(self):
        createserver(self.id)

    def close(self):
        if self.conn:
            os.remove(getconnpath(self.id))
        deleteserver(self.id)

    def opened(self):
        return os.path.exists(getpath(self.id))

    def connected(self):
        return os.path.exists(getconnpath(self.id))

    def send(self, data):
        updateserver(self.id, data)

    def recv(self, buf):
        if UPDATED[self.id]:
            data = getserver(self.id)
            UPDATED[self.id] = False
            stripped = data[:buf]
            return stripped
        else:
            while not UPDATED[self.id]:
                pass
            return self.recv(buf)

SETUP = threading.Thread(target=setup, daemon=True)
SETUP.start()
