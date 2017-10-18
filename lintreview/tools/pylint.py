from __future__ import absolute_import
import os
import logging
from lintreview.tools import Tool, run_command, process_quickfix
from lintreview.utils import in_path

log = logging.getLogger(__name__)


class Pylint(Tool):

    name = 'pylint'

    pylint_options = []

    def check_dependencies(self):
        """
        See if pylint is on the PATH
        """
        return in_path('pylint')

    def match_file(self, filename):
        base = os.path.basename(filename)
        name, ext = os.path.splitext(base)
        return ext == '.py'

    def process_files(self, files):
        """
        Run code checks with pylint.
        Only a single process is made for all files
        to save resources.
        """
        log.debug('Processing %s files with %s', files, self.name)
        command = self.make_command(files)
        output = run_command(command, split=True, ignore_error=True)
        if not output:
            log.debug('No pylint errors found.')
            return False

        process_quickfix(self.problems, output, lambda name: name)

    def make_command(self, files):
        """
        $ pylint --output-format=parseable --reports=n path/to/file.py
        """
        msg_template = '{path}:{line}: {msg_id} {msg}'
        command = ['pylint', '--reports=n', '--msg-template', msg_template]
        command.extend(files)
        return command
