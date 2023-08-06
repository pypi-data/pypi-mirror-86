
import argparse

from notebuild.shell import run_shell, run_shell_list
from notejob.run.core import start
from notetool.tool.log import log

logger = log("notebuild")


class JobScheduler:
    def __init__(self):
        pass

    def start(self):
        logger.info("start")
        start()

    def stop(self):
        logger.info("stop")

    def restart(self):
        self.stop()
        self.start()


def command_line_parser():
    parser = argparse.ArgumentParser(description="Test")
    parser.add_argument('command')
    args = parser.parse_args()
    return args


def notejob():
    args = command_line_parser()
    job = JobScheduler()
    if args.command == 'run':
        job.start()
    elif args.command == 'start':
        job.start()
    elif args.command == 'stop':
        job.stop()
    elif args.command == 'restart':
        job.restart()
