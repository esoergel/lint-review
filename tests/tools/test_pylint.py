from __future__ import absolute_import
from lintreview.review import Problems
from lintreview.review import Comment
from lintreview.tools.pylint import Pylint
from unittest import TestCase
from nose.tools import eq_, assert_in, assert_not_in


class TestPylint(TestCase):

    class fixtures:
        no_errors = 'tests/fixtures/pylint/no_errors.py'
        has_errors = 'tests/fixtures/pylint/has_errors.py'

    def setUp(self):
        self.problems = Problems()
        self.tool = Pylint(self.problems)

    def test_match_file(self):
        self.assertFalse(self.tool.match_file('test.php'))
        self.assertFalse(self.tool.match_file('test.js'))
        self.assertFalse(self.tool.match_file('dir/name/test.js'))
        self.assertTrue(self.tool.match_file('test.py'))
        self.assertTrue(self.tool.match_file('dir/name/test.py'))

    def test_process_files__one_file_pass(self):
        self.tool.process_files([self.fixtures.no_errors])
        eq_([], self.problems.all(self.fixtures.no_errors))

    def test_process_files__one_file_fail(self):
        self.tool.process_files([self.fixtures.has_errors])
        problems = self.problems.all(self.fixtures.has_errors)
        eq_(4, len(problems))

        fname = self.fixtures.has_errors
        expected = Comment(fname, 7, 7,
                           'C0330 Wrong continued indentation (add 9 spaces).')
        eq_(expected, problems[0])

        expected = Comment(fname, 5, 5, "W0613 Unused argument 'self'")
        eq_(expected, problems[-1])

    def test_process_files_two_files(self):
        self.tool.process_files([self.fixtures.no_errors,
                                 self.fixtures.has_errors])

        eq_([], self.problems.all(self.fixtures.no_errors))

        problems = self.problems.all(self.fixtures.has_errors)
        eq_(4, len(problems))

        fname = self.fixtures.has_errors
        expected = Comment(fname, 7, 7,
                           'C0330 Wrong continued indentation (add 9 spaces).')
        eq_(expected, problems[0])

        expected = Comment(fname, 5, 5, "W0613 Unused argument 'self'")
        eq_(expected, problems[-1])

    def test_process_files__ignore(self):
        options = {
            'disable': 'W0611,W0613'
        }
        self.tool = Pylint(self.problems, options)
        self.tool.process_files([self.fixtures.has_errors])
        problems = self.problems.all(self.fixtures.has_errors)
        eq_(4, len(problems))
        for p in problems:
            assert_not_in('W0611', p.body)
            assert_not_in('W0613', p.body)

    # def test_process_files__line_length(self):
        # options = {
            # 'max-line-length': '10'
        # }
        # self.tool = Pylint(self.problems, options)
        # self.tool.process_files([self.fixtures.has_errors])
        # problems = self.problems.all(self.fixtures.has_errors)
        # eq_(10, len(problems))
        # expected = Comment(self.fixtures.has_errors, 1, 1,
                           # 'E501 line too long (23 > 10 characters)')
        # eq_(expected, problems[0])

    # def test_process_files__select(self):
        # options = {
            # 'select': 'W603'
        # }
        # self.tool = Pylint(self.problems, options)
        # self.tool.process_files([self.fixtures.has_errors])
        # problems = self.problems.all(self.fixtures.has_errors)
        # eq_(1, len(problems))
        # for p in problems:
            # assert_in('W603', p.body)
