# All Rights Reserved.

import os
import sys
import traceback
import re
from base import Module as baseModule
from com.log import getLogger
from com import processutils
from config.configuration import CONF

VERSION = "1.0.0"
LOG = getLogger()

class Module(baseModule):
    def __init__(self, version):
        super(Module, self).__init__("Diag Demo", version)
        LOG.info("enter into __init__.")

    def prepare(self):
        super(Module, self).prepare()
        LOG.info("enter into prepare.")

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.demo_app_path = os.path.join(base_dir, CONF.bin_dir, "demo_app")
        if not os.path.exists(self.demo_app_path):
            err_msg = "%s not exists" % self.demo_app_path
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        return True, ""

    def diagnostic(self):
        super(Module, self).diagnostic()
        LOG.info("enter into diagnostic.")

        cmd = "%s --addr=0x123456" % self.demo_app_path
        out, err = processutils.trycmd(cmd, shell=True, timeout_sec=10)
        if err:
            err_msg = "execute %s fail. %s" % (cmd, err)
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        return True, ""

    def finish(self):
        super(Module, self).finish()
        LOG.info("enter into finish.")

def entry():
    LOG.info("args: %s" % sys.argv)

    module = Module(VERSION)
    ret, err = module.prepare()
    if ret:
        ret, err = module.diagnostic()
        if ret:
            LOG.info("diagnose OK")
            module.finish()
        else:
            LOG.info("diagnose failed, err is : %s" % err)
    else:
        LOG.error("prepare failed, err is : %s" % err)

    module.output()


if __name__ == '__main__':
    entry()
