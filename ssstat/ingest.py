#!/usr/bin/env python
# encoding: utf-8
"""
Ingest command for ssstat--download logs from S3 and add to MongoDB.

2012-11-18 - Created by Jonathan Sick
"""

import os
import logging

from cliff.command import Command

import ingest_core


class IngestCommand(Command):
    """ssstat ingest."""

    log = logging.getLogger(__name__)

    def get_parser(self, progName):
        """Adds command line options."""
        parser = super(IngestCommand, self).get_parser(progName)
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
        """Runs the `ssstat ingest` command pipeline."""
        self.log.debug("Running ssstat ingest")

        # Downloads logs into root of cache directory
        ingest_core.download_logs(parsedArgs.log_bucket,
            parsedArgs.prefix, parsedArgs.cache_dir,
            delete=parsedArgs.delete)

        # Add downloaded logs into MongoDB (and archive)
        ingest_core.ingest_logs(parsedArgs.prefix, parsedArgs.cache_dir)


def main():
    pass


if __name__ == '__main__':
    main()
