import sys
import logging
import xmlrpc.client

from os import environ
from functools import partial

from gevent import spawn
from gevent.lock import RLock
from gevent.queue import Queue
from zerorpc import stream, Server, LostRemote
from supervisor.childutils import getRPCInterface


READY = 'READY\n'
ACKNOWLEDGED = 'RESULT 2\nOK'

DEFAULT_BIND = 'tcp://*:9002'


def signal(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def wait_for_event():
    header_line = sys.stdin.readline()
    event = dict((x.split(':') for x in header_line.split()))
    payload_str = sys.stdin.read(int(event['len']))
    event['payload'] = dict((x.split(':') for x in payload_str.split()))
    return event


def event_dispatcher_loop(handler):
    while True:
        signal(READY)
        event = wait_for_event()
        handler(event)
        signal(ACKNOWLEDGED)


get_rpc = partial(getRPCInterface, environ)


def build_method(name):
    subsystem_name, func_name = name.split('.', 1)
    fname = '{}_{}'.format(subsystem_name, func_name)
    def method(*args):
        subsystem = getattr(get_rpc(), subsystem_name)
        return getattr(subsystem, func_name)(*args)
    method.__name__ = fname
    return fname, method


class Supervisor(object):

    def __init__(self, channel):
        self.channel = channel
        self.event_channels = set()
        self.rpc = get_rpc()
        for name in self.rpc.system.listMethods():
            setattr(self, *build_method(name))

    @stream
    def event_stream(self):
        logging.info('client connected to stream')
        channel = Queue()
        self.event_channels.add(channel)
        try:
            yield 'First event to trigger connection. Please ignore me!'
            for event in channel:
                yield event
        except LostRemote as e:
            logging.info('remote end of stream disconnected')
        finally:
            self.event_channels.remove(channel)

    def publish_event(self, event):
        name = event['eventname']
        if name.startswith('TICK'):
            return
        event = dict(event)
        if name.startswith('PROCESS_STATE'):
            payload = event['payload']
            pname = "{}:{}".format(payload['groupname'], payload['processname'])
            logging.info('handling %s of %s', name, pname)
            try:
                payload['process'] = self.rpc.supervisor.getProcessInfo(pname)
            except xmlrpc.client.Fault:
                # probably supervisor is shutting down
                logging.warn('probably shutting down...')
                return
        for channel in self.event_channels:
            channel.put(event)


def run(bind=DEFAULT_BIND):
    def event_consumer_loop():
        # xmlrpclib is not reentrant. We might have several greenlets accessing
        # supervisor at the same time so we serialize event treatment here
        lock = RLock()
        for event in channel:
            try:
                with lock:
                    supervisor.publish_event(event)
            except:
                logging.exception('Error processing %s', event)
    channel = Queue()
    supervisor = Supervisor(channel)
    spawn(event_consumer_loop)
    spawn(event_dispatcher_loop, channel.put)
    server = Server(supervisor)
    server.bind(bind)
    server.run()


def main(args=None):
    import gevent.monkey
    gevent.monkey.patch_all(thread=False, sys=True)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', help='bind address',
                        default=DEFAULT_BIND)
    parser.add_argument('--log-level', help='log level', type=str,
                        default='INFO',
                        choices=['DEBUG', 'INFO', 'WARN', 'ERROR'])
    options = parser.parse_args(args)

    log_level = getattr(logging, options.log_level.upper())
    log_fmt = '%(levelname)s %(asctime)-15s %(name)s: %(message)s'
    logging.basicConfig(level=log_level, format=log_fmt)

    bind = options.bind
    if '://' not in bind:
        bind = 'tcp://' + bind
    logging.info('Supervisor: %s', environ['SUPERVISOR_SERVER_URL'])
    run(bind)
