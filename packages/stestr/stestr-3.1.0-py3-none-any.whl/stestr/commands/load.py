# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Load data into a repository."""


import errno
import functools
import os
import sys
import warnings

from cliff import command
import subunit
import testtools

from stestr import output
from stestr.repository import abstract as repository
from stestr.repository import util
from stestr import results
from stestr import subunit_trace
from stestr import user_config
from stestr import utils


class Load(command.Command):
    """Load a subunit stream into a repository.

    Failing tests are shown on the console and a summary of the stream
    is printed at the end.

    Without --subunit, the process exit code will be non-zero if the test
    run was not successful. With --subunit, the process exit code is
    non-zero if the subunit stream could not be generated successfully.
    The test results and run status are included in the subunit stream, so
    the stream should be used to determining the result of the run instead
    of the exit code when using the --subunit flag.
    """

    def get_parser(self, prog_name):
        parser = super(Load, self).get_parser(prog_name)
        parser.add_argument("files", nargs="*", default=False,
                            help="The subunit v2 stream files to load into the"
                            " repository")
        parser.add_argument("--partial", action="store_true",
                            default=False,
                            help="DEPRECATED: The stream being loaded was a "
                            "partial run. This option is deprecated and no "
                            "does anything. It will be removed in the future")
        parser.add_argument("--force-init", action="store_true",
                            default=False,
                            help="Initialise the repository if it does not "
                            "exist already")
        parser.add_argument("--subunit", action="store_true",
                            default=False,
                            help="Display results in subunit format.")
        parser.add_argument("--id", "-i", default=None,
                            help="Append the stream into an existing entry in "
                            "the repository")
        parser.add_argument("--subunit-trace", action='store_true',
                            default=False,
                            help="Display the loaded stream through the "
                            "subunit-trace output filter")
        parser.add_argument('--color', action='store_true', default=False,
                            help='Enable color output in the subunit-trace '
                            'output, if subunit-trace output is enabled. If '
                            'subunit-trace is disable this does nothing.')
        parser.add_argument('--abbreviate', action='store_true',
                            dest='abbreviate',
                            help='Print one character status for each test')
        parser.add_argument('--suppress-attachments', action='store_true',
                            dest='suppress_attachments',
                            help='If set do not print stdout or stderr '
                            'attachment contents on a successful test '
                            'execution')
        parser.add_argument('--all-attachments', action='store_true',
                            dest='all_attachments',
                            help='If set print all text attachment contents on'
                            ' a successful test execution')
        parser.add_argument('--show-binary-attachments', action='store_true',
                            dest='show_binary_attachments',
                            help='If set, show non-text attachments. This is '
                            'generally only useful for debug purposes.')
        return parser

    def take_action(self, parsed_args):
        user_conf = user_config.get_user_config(self.app_args.user_config)
        args = parsed_args
        if args.suppress_attachments and args.all_attachments:
            msg = ("The --suppress-attachments and --all-attachments "
                   "options are mutually exclusive, you can not use both "
                   "at the same time")
            print(msg)
            sys.exit(1)
        if getattr(user_conf, 'load', False):
            force_init = args.force_init or user_conf.load.get('force-init',
                                                               False)
            pretty_out = args.subunit_trace or user_conf.load.get(
                'subunit-trace', False)
            color = args.color or user_conf.load.get('color', False)
            abbreviate = args.abbreviate or user_conf.load.get('abbreviate',
                                                               False)
            suppress_attachments_conf = user_conf.run.get(
                'suppress-attachments', False)
            all_attachments_conf = user_conf.run.get(
                'all-attachments', False)
            if not args.suppress_attachments and not args.all_attachments:
                suppress_attachments = suppress_attachments_conf
                all_attachments = all_attachments_conf
            elif args.suppress_attachments:
                all_attachments = False
                suppress_attachments = args.suppress_attachments
            elif args.all_attachments:
                suppress_attachments = False
                all_attachments = args.all_attachments
        else:
            force_init = args.force_init
            pretty_out = args.subunit_trace
            color = args.color
            abbreviate = args.abbreviate
            suppress_attachments = args.suppress_attachments
            all_attachments = args.all_attachments
        verbose_level = self.app.options.verbose_level
        stdout = open(os.devnull, 'w') if verbose_level == 0 else sys.stdout
        load(repo_type=self.app_args.repo_type,
             repo_url=self.app_args.repo_url,
             partial=args.partial, subunit_out=args.subunit,
             force_init=force_init, streams=args.files,
             pretty_out=pretty_out, color=color,
             stdout=stdout, abbreviate=abbreviate,
             suppress_attachments=suppress_attachments, serial=True,
             all_attachments=all_attachments,
             show_binary_attachments=args.show_binary_attachments)


def load(force_init=False, in_streams=None,
         partial=False, subunit_out=False, repo_type='file', repo_url=None,
         run_id=None, streams=None, pretty_out=False, color=False,
         stdout=sys.stdout, abbreviate=False, suppress_attachments=False,
         serial=False, all_attachments=False, show_binary_attachments=False):
    """Load subunit streams into a repository

    This function will load subunit streams into the repository. It will
    output to STDOUT the results from the input stream. Internally this is
    used by the run command to both output the results as well as store the
    result in the repository.

    :param bool force_init: Initialize the specified repository if it hasn't
        been created.
    :param list in_streams: A list of file objects that will be saved into the
        repository
    :param bool partial: DEPRECATED: Specify the input is a partial stream.
        This option is deprecated and no longer does anything. It will be
        removed in the future.
    :param bool subunit_out: Output the subunit stream to stdout
    :param str repo_type: This is the type of repository to use. Valid choices
        are 'file' and 'sql'.
    :param str repo_url: The url of the repository to use.
    :param run_id: The optional run id to save the subunit stream to.
    :param list streams: A list of file paths to read for the input streams.
    :param bool pretty_out: Use the subunit-trace output filter for the loaded
        stream.
    :param bool color: Enabled colorized subunit-trace output
    :param file stdout: The output file to write all output to. By default
        this is sys.stdout
    :param bool abbreviate: Use abbreviated output if set true
    :param bool suppress_attachments: When set true attachments subunit_trace
        will not print attachments on successful test execution.
    :param bool all_attachments: When set true subunit_trace will print all
        text attachments on successful test execution.
    :param bool show_binary_attachments: When set to true, subunit_trace will
        print binary attachments in addition to text attachments.

    :return return_code: The exit code for the command. 0 for success and > 0
        for failures.
    :rtype: int
    """
    if partial:
        warnings.warn('The partial flag is deprecated and has no effect '
                      'anymore')

    try:
        repo = util.get_repo_open(repo_type, repo_url)
    except repository.RepositoryNotFound:
        if force_init:
            try:
                repo = util.get_repo_initialise(repo_type, repo_url)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                repo_path = repo_url or './stestr'
                stdout.write('The specified repository directory %s already '
                             'exists. Please check if the repository already '
                             'exists or select a different path\n'
                             % repo_path)
                exit(1)
        else:
            raise
    # Not a full implementation of TestCase, but we only need to iterate
    # back to it. Needs to be a callable - its a head fake for
    # testsuite.add.
    if in_streams:
        streams = utils.iter_streams(in_streams, 'subunit')
    elif streams:
        opener = functools.partial(open, mode='rb')
        streams = map(opener, streams)
    else:
        streams = [sys.stdin]

    def mktagger(pos, result):
        return testtools.StreamTagger([result], add=['worker-%d' % pos])

    def make_tests():
        for pos, stream in enumerate(streams):
            # Calls StreamResult API.
            case = subunit.ByteStreamToStreamResult(
                stream, non_subunit_name='stdout')
            decorate = functools.partial(mktagger, pos)
            case = testtools.DecorateTestCaseResult(case, decorate)
            yield (case, str(pos))
    if not run_id:
        inserter = repo.get_inserter()
    else:
        inserter = repo.get_inserter(run_id=run_id)

    retval = 0
    if serial:
        for stream in streams:
            # Calls StreamResult API.
            case = subunit.ByteStreamToStreamResult(
                stream, non_subunit_name='stdout')
            result = _load_case(inserter, repo, case, subunit_out, pretty_out,
                                color, stdout, abbreviate,
                                suppress_attachments, all_attachments,
                                show_binary_attachments)
            if result or retval:
                retval = 1
            else:
                retval = 0
    else:
        case = testtools.ConcurrentStreamTestSuite(make_tests)
        retval = _load_case(inserter, repo, case, subunit_out, pretty_out,
                            color, stdout, abbreviate, suppress_attachments,
                            all_attachments, show_binary_attachments)

    return retval


def _load_case(inserter, repo, case, subunit_out, pretty_out,
               color, stdout, abbreviate, suppress_attachments,
               all_attachments, show_binary_attachments):
    if subunit_out:
        output_result, summary_result = output.make_result(inserter.get_id,
                                                           output=stdout)
    elif pretty_out:
        outcomes = testtools.StreamToDict(
            functools.partial(subunit_trace.show_outcome, stdout,
                              enable_color=color, abbreviate=abbreviate,
                              suppress_attachments=suppress_attachments,
                              all_attachments=all_attachments,
                              show_binary_attachments=show_binary_attachments))
        summary_result = testtools.StreamSummary()
        output_result = testtools.CopyStreamResult([outcomes, summary_result])
        output_result = testtools.StreamResultRouter(output_result)
        cat = subunit.test_results.CatFiles(stdout)
        output_result.add_rule(cat, 'test_id', test_id=None)
    else:
        try:
            previous_run = repo.get_latest_run()
        except KeyError:
            previous_run = None
        output_result = results.CLITestResult(
            inserter.get_id, stdout, previous_run)
        summary_result = output_result.get_summary()
    result = testtools.CopyStreamResult([inserter, output_result])
    result.startTestRun()
    try:
        case.run(result)
    finally:
        result.stopTestRun()
    if pretty_out and not subunit_out:
        start_times = []
        stop_times = []
        for worker in subunit_trace.RESULTS:
            for test in subunit_trace.RESULTS[worker]:
                if not test['timestamps'][0] or not test['timestamps'][1]:
                    continue
                start_times.append(test['timestamps'][0])
                stop_times.append(test['timestamps'][1])
        if not start_times or not stop_times:
            sys.stderr.write("\nNo tests were successful during the run")
            return 1
        start_time = min(start_times)
        stop_time = max(stop_times)
        elapsed_time = stop_time - start_time
        subunit_trace.print_fails(stdout)
        subunit_trace.print_summary(stdout, elapsed_time)
    if not results.wasSuccessful(summary_result):
        return 1
    else:
        return 0
