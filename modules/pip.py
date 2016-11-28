import os
import shlex
from argh import add_commands

class Plugin(object):

    config = None
    helper = None

    def __init__(self, config, helper):
        self.config = config
        self.helper = helper


    def pip(self, *args):
        if len(args) == 1:
            args = shlex.split(args[0])

        self.helper.setup_virtualenv()

        binargs = ['pip'] + list(args)
        os.execvp(binargs[0], binargs)


def initialize(config, argparser, helper):
    mod = Plugin(config, helper)
    add_commands(argparser, [mod.pip])
