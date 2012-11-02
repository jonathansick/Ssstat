#!/usr/bin/env python
# encoding: utf-8
"""
Ssstat: S3 Log Analytics with MongoDB.

2012-11-02 - Created by Jonathan Sick
"""

import os
import optparse

from boto.s3.connection import S3Connection
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


def download_logs(bucketName, prefix, cacheDir):
    """docstring for download_logs"""
    cacheDir = os.path.expandvars(cacheDir)
    if not os.path.exists(cacheDir): os.makedirs(cacheDir)

    conn = S3Connection()
    bucket = conn.create_bucket(bucketName)
    results = bucket.list(prefix=prefix)
    for key in results:
        print key.name


if __name__ == '__main__':
    main()
