#!/usr/bin/env python
# encoding: utf-8
"""
Application control module for Ssstat, a MongoDB-back analytics tool for
Amazon S3 buckets.

2012-11-18 - Created by Jonathan Sick
"""

import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class SsstatApp(App):
    """Cliff-based application manager for Ssstat."""

    log = logging.getLogger(__name__)

    def __init__(self):
        super(SsstatApp, self).__init__(
            description='S3 Analytics in MongoDB',
            version='0.0.2',
            command_manager=CommandManager('ssstat.app'))

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    ssstatApp = SsstatApp()
    return ssstatApp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
