#!/usr/bin/env python
# encoding: utf-8
"""
Ssstat: S3 Log Analytics with MongoDB.

2012-11-02 - Created by Jonathan Sick
"""

import os
import optparse
import re
from collections import namedtuple

from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
# from boto.s3.key import Key


def main():
    parser = optparse.OptionParser(version="0.0.1",
            usage="Usage: $prog [options]")
    parser.add_option('-b', '--bucket', help="S3 Log Bucket",
            dest="bucket_name", default=None)
    parser.add_option('-d', '--cache-dir', help="Log file cache directory",
            dest="cache_dir", default=None)
    parser.add_option('-p', '--prefix',
            help="Prefix for the desired log files",
            dest="prefix", default=None)
    opts, args = parser.parse_args()

    if (opts.bucket_name is not None) \
            and (opts.cache_dir is not None) \
            and (opts.prefix is not None):
        download_logs(opts.bucket_name, opts.prefix, opts.cache_dir)


def download_logs(bucketName, prefix, cacheDir, delete=True):
    """docstring for download_logs"""
    cacheDir = os.path.expandvars(cacheDir)
    if not os.path.exists(cacheDir): os.makedirs(cacheDir)

    conn = S3Connection()
    bucket = conn.create_bucket(bucketName)
    results = bucket.list(prefix=prefix)
    for key in results:
        cachedPath = os.path.join(cacheDir, key.name)
        if os.path.exists(cachedPath): os.remove(cachedPath)
        try:
            key.get_contents_to_filename(cachedPath)
            if os.path.exists(cachedPath) and delete:
                key.delete()
        except S3ResponseError, err:
            print "Error downloading", key.name
            if err.status in [403, 404]:
                key.delete()
            raise


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
        results = [match.group(1 + n) for n in xrange(17)]
        event = self.Event._make(results)
        return event


def test_parser():
    data = r'e9b5297650a03c924eb3295e70871b615f958c399c9690c30f344ab2e9bbf815 files.jonathansick.ca [02/Nov/2012:14:11:14 +0000] 128.0.0.1 - 3FF4D293FACEC593 WEBSITE.HEAD.OBJECT adsbibdesk/adsbibdesk_3.0.6.zip "HEAD /adsbibdesk/adsbibdesk_3.0.6.zip HTTP/1.1" 200 - - 56730 19 - "-" "-" -'
    p = LogParser()
    print p._parse_line(data)


if __name__ == '__main__':
    main()
    # test_parser()
