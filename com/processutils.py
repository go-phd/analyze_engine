# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2020 Alibaba-inc.
# All Rights Reserved.


"""
System-level utilities and helper functions.
"""

import os
import random
import shlex
import signal
import subprocess
import time
from threading import Timer

import log as logging

from config.configuration import CONF

LOG = logging.getLogger()


class InvalidArgumentError(Exception):
    def __init__(self, message=None):
        super(InvalidArgumentError, self).__init__(message)


class UnknownArgumentError(Exception):
    def __init__(self, message=None):
        super(UnknownArgumentError, self).__init__(message)


class ProcessExecutionError(Exception):
    def __init__(self, stdout=None, stderr=None, exit_code=None, cmd=None,
                 description=None):
        self.exit_code = exit_code
        self.stderr = stderr
        self.stdout = stdout
        self.cmd = cmd
        self.description = description

        if description is None:
            description = "Unexpected error while running command."
        if exit_code is None:
            exit_code = '-'
        message = ("%s\nCommand: %s\nExit code: %s\nStdout: %r\nStderr: %r"
                   % (description, cmd, exit_code, stdout, stderr))
        super(ProcessExecutionError, self).__init__(message)


class NoRootWrapSpecified(Exception):
    def __init__(self, message=None):
        super(NoRootWrapSpecified, self).__init__(message)


def _subprocess_setup():
    # Python installs a SIGPIPE handler by default. This is usually not what
    # non-Python subprocesses expect.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def execute(*cmd, **kwargs):
    """Helper method to shell out and execute a command through subprocess.
    Allows optional retry.
    :param cmd:             Passed to subprocess.Popen.
    :type cmd:              string
    :param process_input:   Send to opened process.
    :type proces_input:     string
    :param check_exit_code: Single bool, int, or list of allowed exit
                            codes.  Defaults to [0].  Raise
                            :class:`ProcessExecutionError` unless
                            program exits with one of these code.
    :type check_exit_code:  boolean, int, or [int]
    :param delay_on_retry:  True | False. Defaults to True. If set to True,
                            wait a short amount of time before retrying.
    :type delay_on_retry:   boolean
    :param attempts:        How many times to retry cmd.
    :type attempts:         int
    :param run_as_root:     True | False. Defaults to False. If set to True,
                            the command is prefixed by the command specified
                            in the root_helper kwarg.
    :type run_as_root:      boolean
    :param root_helper:     command to prefix to commands called with
                            run_as_root=True
    :type root_helper:      string
    :param shell:           whether or not there should be a shell used to
                            execute this command. Defaults to false.
    :type shell:            boolean
    :param loglevel:        log level for execute commands.
    :type loglevel:         int.  (Should be logging.DEBUG or logging.INFO)
    :returns:               (stdout, stderr) from process execution
    :raises:                :class:`UnknownArgumentError` on
                            receiving unknown arguments
    :raises:                :class:`ProcessExecutionError`
    """

    process_input = kwargs.pop('process_input', None)
    check_exit_code = kwargs.pop('check_exit_code', [0])
    ignore_exit_code = False
    delay_on_retry = kwargs.pop('delay_on_retry', True)
    attempts = kwargs.pop('attempts', 1)
    run_as_root = kwargs.pop('run_as_root', False)
    root_helper = kwargs.pop('root_helper', '')
    shell = kwargs.pop('shell', False)
    # loglevel = kwargs.pop('loglevel', logging.DEBUG)
    timeout_sec = kwargs.pop('timeout_sec', -1)
    if not isinstance(timeout_sec, int):
        try:
            timeout_sec = int(timeout_sec)
        except:
            timeout_sec = -1

    if isinstance(check_exit_code, bool):
        ignore_exit_code = not check_exit_code
        check_exit_code = [0]
    elif isinstance(check_exit_code, int):
        check_exit_code = [check_exit_code]

    if kwargs:
        raise UnknownArgumentError(('Got unknown keyword args '
                                     'to utils.execute: %r') % kwargs)

    if run_as_root and hasattr(os, 'geteuid') and os.geteuid() != 0:
        if not root_helper:
            raise NoRootWrapSpecified(
                message=('Command requested root, but did not specify a root '
                         'helper.'))
        cmd = shlex.split(root_helper) + list(cmd)

    cmd = map(str, cmd)
    # sanitized_cmd = strutils.mask_password(' '.join(cmd))

    while attempts > 0:
        attempts -= 1
        timer = None
        try:
            # LOG.log(loglevel, _('Running cmd (subprocess): %s'),
            # sanitized_cmd)
            _PIPE = subprocess.PIPE  # pylint: disable=E1101

            if os.name == 'nt':
                preexec_fn = None
                close_fds = False
            else:
                preexec_fn = _subprocess_setup
                close_fds = True

            obj = subprocess.Popen(cmd,
                                   stdin=_PIPE,
                                   stdout=_PIPE,
                                   stderr=_PIPE,
                                   close_fds=close_fds,
                                   preexec_fn=preexec_fn,
                                   shell=shell)
            result = None
            kill_proc = lambda p: p.kill()
            if timeout_sec != -1:
                timer = Timer(timeout_sec, kill_proc, [obj])
                timer.start()
            if process_input is not None:
                result = obj.communicate(process_input)
            else:
                result = obj.communicate()
            obj.stdin.close()  # pylint: disable=E1101
            _returncode = obj.returncode  # pylint: disable=E1101
            if _returncode:
                # LOG.log(loglevel, ('Result was %s') % _returncode)
                if not ignore_exit_code and _returncode not in check_exit_code:
                    (stdout, stderr) = result
                    # sanitized_stdout = strutils.mask_password(stdout)
                    # sanitized_stderr = strutils.mask_password(stderr)
                    raise ProcessExecutionError(exit_code=_returncode,
                                                stdout=stdout,
                                                stderr=stderr,
                                                cmd=cmd)
            return result
        except ProcessExecutionError:
            if not attempts:
                raise
            else:
                #LOG.log(loglevel, ('%r failed. Retrying.'), cmd)
                if delay_on_retry:
                    time.sleep(random.randint(20, 200) / 100.0)
        finally:
            # NOTE(termie): this appears to be necessary to let the subprocess
            #               call clean something up in between calls, without
            #               it two execute calls in a row hangs the second one
            time.sleep(0)
            if timer:
                timer.cancel()


def trycmd(*args, **kwargs):
    """A wrapper around execute() to more easily handle warnings and errors.
    Returns an (out, err) tuple of strings containing the output of
    the command's stdout and stderr.  If 'err' is not empty then the
    command can be considered to have failed.
    :discard_warnings   True | False. Defaults to False. If set to True,
                        then for succeeding commands, stderr is cleared
    """
    LOG.debug("trycmd: args: %s  kwargs: %s" % (args, kwargs))
    discard_warnings = kwargs.pop('discard_warnings', False)
    save_cmds = CONF.protected_commands
    save_cmds = save_cmds.split(",")
    try:
        for cmd in save_cmds:
            cmd = cmd.strip()
            if cmd in args[0]:
                if "timeout_sec" not in kwargs:
                    kwargs["timeout_sec"] = int(CONF.execute_timeout_seconds)
                    break
    except:
        pass
    try:
        out, err = execute(*args, **kwargs)
        failed = False
    except ProcessExecutionError as exn:
        out, err = '', str(exn)
        failed = True
    except Exception as e:
        out, err = '', str(e)
        failed = True

    if not failed and discard_warnings and err:
        # Handle commands that output to stderr but otherwise succeed
        err = ''

    return out, err


def ssh_execute(ssh, cmd, process_input=None,
                addl_env=None, check_exit_code=True):
    LOG.debug(('Running cmd (SSH): %s'), cmd)
    if addl_env:
        raise InvalidArgumentError(('Environment not supported over SSH'))

    if process_input:
        # This is (probably) fixable if we need it...
        raise InvalidArgumentError(('process_input not supported over SSH'))

    stdin_stream, stdout_stream, stderr_stream = ssh.exec_command(cmd)
    channel = stdout_stream.channel

    # NOTE(justinsb): This seems suspicious...
    # ...other SSH clients have buffering issues with this approach
    stdout = stdout_stream.read()
    stderr = stderr_stream.read()
    stdin_stream.close()

    exit_status = channel.recv_exit_status()

    # exit_status == -1 if no exit code was returned
    if exit_status != -1:
        LOG.debug(('Result was %s') % exit_status)
        if check_exit_code and exit_status != 0:
            raise ProcessExecutionError(exit_code=exit_status,
                                        stdout=stdout,
                                        stderr=stderr,
                                        cmd=cmd)

    return stdout, stderr


def byteify(input):
    if isinstance(input, dict):
        t = {}
        for k, v in input.iteritems():
            t.update({byteify(k): byteify(v)})
        return t
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
