#!/usr/bin/env python
# encoding: utf-8
"""
Insert command for ssstat--insert pre-downloaded logs into MongoDB.

2012-11-18 - Created by Jonathan Sick
"""

import os
import logging

from cliff.command import Command

import ingest_core


class InsertCommand(Command):
    """ssstat insert"""

    log = logging.getLogger(__name__)

    def get_parser(self, progName):
        """Adds command line options."""
        parser = super(InsertCommand, self).get_parser(progName)
        parser.add_argument('prefix',
            help='Prefix for the desired log files')
        parser.add_argument('--cache-dir',
            default=os.path.expandvars("$HOME/.ssstat/cache"),
            action='store',
            dest='cache_dir',
            help='Local directory where logs are cached')
        return parser

    def take_action(self, parsedArgs):
        """Runs the `ssstat insert` command pipeline."""
        self.log.debug("Running ssstat insert")

        # Add downloaded logs into MongoDB (and archive)
        ingest_core.ingest_logs(parsedArgs.prefix, parsedArgs.cache_dir)


def main():
    pass


if __name__ == '__main__':
    main()
