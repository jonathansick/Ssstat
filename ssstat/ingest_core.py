#!/usr/bin/env python
# encoding: utf-8
"""
Functions and tools for downloading and reading S3 Logs, and ultimately
adding them into MongoDB.

2012-11-02 - Created by Jonathan Sick
"""

import os
import shutil
import re
from collections import namedtuple
import glob
from datetime import datetime

from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
# from boto.s3.key import Key
import pymongo


def main():
    pass


def download_logs(bucketName, prefix, cacheDir, delete=True):
    """Download log files for this prefix to the cacheDir."""
    cacheDir = os.path.expandvars(cacheDir)
    if not os.path.exists(cacheDir): os.makedirs(cacheDir)

    conn = S3Connection()
    bucket = conn.get_bucket(bucketName)
    results = bucket.list(prefix=prefix)
    for key in results:
        cachedPath = os.path.join(cacheDir, key.name)
        if os.path.exists(cachedPath): os.remove(cachedPath)
        try:
            key.get_contents_to_filename(cachedPath)
            print "Downloading", key.name
            if os.path.exists(cachedPath) and delete:
                print "Deleted downloaded %s" % key.name
                key.delete()
        except S3ResponseError, err:
            print "Error downloading", key.name
            if err.status in [403, 404]:
                key.delete()
            raise


def ingest_logs(prefix, cacheDir):
    """Process log files, adding them to MongoDB."""
    # Setup directory for archiving ingested log files
    archiveDir = os.path.join(cacheDir, "_archive_%s" % prefix)
    if not os.path.exists(archiveDir): os.makedirs(archiveDir)

    conn = pymongo.Connection()
    db = conn.ssstat
    collection = db[prefix]
    collection.ensure_index([('path', 1), ('time', 1)])
    
    # Iterate through files and parse
    pattern = os.path.join(cacheDir, prefix + "*")
    paths = glob.glob(pattern)
    parser = LogParser()
    for path in paths:
        events = parser.parse_file(path)
        for event in events:
            if event is not None:
                insert_event(event, collection)
        pathName = os.path.basename(path)
        archivePath = os.path.join(archiveDir, pathName)
        shutil.move(path, archivePath)


def insert_event(event, collection):
    """docstring for insert_even"""
    doc = {"time": event.datetime, "ip": event.ip, "path": event.key,
        "user_agent": event.user_agent, "referer": event.referer,
        "http_status": event.http_status, "s3_error": event.s3_error,
        "operation": event.operation, "bytes_sent": event.bytes_sent}
    collection.insert(doc, safe=True)


MONTH = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
        "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11,
        "Dec": 12}


class LogParser(object):
    """Parser for S3 Log files.
    
    Borrows snippets from:
        http://blog.kowalczyk.info/article/Parsing-s3-log-files-in-python.html
    """
    def __init__(self):
        super(LogParser, self).__init__()
        _pattern = r'(\S+) (\S+) \[(.*?)\] (\S+) (\S+) ' \
            r'(\S+) (\S+) (\S+) "([^"]+)" ' \
            r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) ' \
            r'"([^"]+)" "([^"]+)"'
        self.parser = re.compile(_pattern)

        # Use a namedtuple to store fields from the log line
        fieldNames = ("bucket_owner", "bucket", "datetime", "ip",
                "requestor_id", "request_id", "operation", "key",
                "http_method_uri_proto", "http_status", "s3_error",
                "bytes_sent", "object_size", "total_time", "turn_around_time",
                "referer", "user_agent")
        self.Event = namedtuple('Event', fieldNames)

    def parse_file(self, path):
        """Produce event objects from the log file `path`."""
        f = open(path, 'r')
        events = [self._parse_line(line) for line in f.readlines()]
        f.close()
        return events

    def _parse_line(self, line):
        """Parse a single line from a log file, producing an Event object."""
        match = self.parser.match(line)
        try:
            results = [match.group(1 + n) for n in xrange(17)]
        except:
            print line
            print "Parsing failure"  # FIXME need to understand this
            return None
        event = self.Event._make(results)
        # Replace timestamp with datetime object
        # e.g. 02/Nov/2012:14:11:14 +0000
        dateStr = event.datetime[:11]
        day, monthStr, year = dateStr.split("/")
        timeStr = event.datetime[12:20]
        hour, minute, sec = timeStr.split(":")
        dt = datetime(int(year), MONTH[monthStr], int(day),
                int(hour), int(minute), int(sec))
        # Replace bytes sent with integer
        bytesSent = event.bytes_sent
        if bytesSent != "-":
            bytesSent = int(bytesSent)
        else:
            bytesSent = 0
        event = event._replace(datetime=dt, bytes_sent=bytesSent)
        return event


def test_parser():
    data = r'e9b5297650a03c924eb3295e70871b615f958c399c9690c30f344ab2e9bbf815 files.jonathansick.ca [02/Nov/2012:14:11:14 +0000] 128.0.0.1 - 3FF4D293FACEC593 WEBSITE.HEAD.OBJECT adsbibdesk/adsbibdesk_3.0.6.zip "HEAD /adsbibdesk/adsbibdesk_3.0.6.zip HTTP/1.1" 200 - - 56730 19 - "-" "-" -'
    p = LogParser()
    print p._parse_line(data)


if __name__ == '__main__':
    main()
    # test_parser()
