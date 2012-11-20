#!/usr/bin/env python
# encoding: utf-8
"""
Download command for ssstat--download logs without adding to MongoDB.

2012-11-18 - Created by Jonathan Sick
"""


import os
import logging

from cliff.command import Command

import ingest_core


class DownloadCommand(Command):
    """ssstat download"""

    log = logging.getLogger(__name__)

    def get_parser(self, progName):
        """Adds command line options."""
        parser = super(DownloadCommand, self).get_parser(progName)
        parser.add_argument('log_bucket',
            help='Name of S3 Logging Bucket')
        parser.add_argument('prefix',
            help='Prefix for the desired log files')
        parser.add_argument('--cache-dir',
            default=os.path.expandvars("$HOME/.ssstat/cache"),
            action='store',
            dest='cache_dir',
            help='Local directory where logs are cached')
        parser.add_argument('--delete',
            dest='delete',
            default=True,
            type=bool,
            help='Delete downloaded logs from S3')
        return parser

    def take_action(self, parsedArgs):
        """Runs the `ssstat download` command pipeline."""
        self.log.debug("Running ssstat download")

        # Downloads logs into root of cache directory
        ingest_core.download_logs(parsedArgs.log_bucket,
            parsedArgs.prefix, parsedArgs.cache_dir,
            delete=parsedArgs.delete)


def main():
    pass


if __name__ == '__main__':
    main()
