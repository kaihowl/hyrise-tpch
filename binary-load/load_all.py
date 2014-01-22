import threading
import time
import os, subprocess, signal
import urllib, httplib
import json
import sys
import re

from glob import glob
from copy import copy

CWD = os.path.dirname(__file__)
TABLE_PATH = os.path.join(CWD, '../hyrise/')
QUERIES_DIR = os.path.join(CWD, './queries/*')
LOG_FILE = open(os.path.join(CWD, 'run.log'), 'w')

class User(threading.Thread):
    def __init__(self, user_name, queries, runs, server):
        threading.Thread.__init__(self)

        self._user_name = user_name
        self._queries = copy(queries)
        self._runs = copy(runs)
        self._server = server

    def output_dir(self):
        return "/dev/null"

    def query(self, d):
        data = None
        try:
            conn = self._server.get_connection()
            conn.request("POST", "", urllib.urlencode([("query",d)]))
            r = conn.getresponse()
            data = r.read()
            conn.close()
        except Exception, e:
            print e, d
            sys.exit(1)
        return data

    def query_with_time(self, d):
        self.query(d)

    def run(self):
        while(self._runs > 0):
            print "Running user %s with run %i" % (self._user_name, self._runs)
            for filename, content in self._queries:
              self.query_with_time(content)
            self._runs -= 1

class Server(object):
    def __init__(self, table_path, log_file=open(os.devnull, 'wb')):
        self.port = int(open("hyrise_server.port").readlines()[0])
        assert(self.port != 0)
        self._starttime = int(time.time())
        print "sever was started server", self.port

    def get_connection(self):
        return httplib.HTTPConnection("localhost", self.port, strict=False)

def load_queries(directory):
    queries = []
    for filename in glob(directory):
        with open(filename) as f:
            queries.append((os.path.basename(filename), f.read()))
    return queries

def set_tables(dirname, queries):    
    table_dir = dirname
    table_name = os.path.basename(dirname)

    def replace_tables(query): 
        replaced = query[1].replace("{{table_name}}", table_name)
        replaced = replaced.replace("{{table_dir}}", table_dir)
        return (query[0], replaced)

    return map(replace_tables, queries)
    
def main():
    server = Server(TABLE_PATH, LOG_FILE)
    users = []

    for dirname in os.walk(TABLE_PATH).next()[1]:
        dirname = os.path.basename(dirname)
        queries = set_tables(dirname, load_queries(QUERIES_DIR))
        users.append(User("%s" % (dirname), queries, 1, server))

    for user in users:
        user.start()

    for user in users:
        user.join()

if __name__ == "__main__":
    main()
