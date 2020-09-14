# All Rights Reserved.

import os
import sys
import traceback
import re
import datetime
from base import Module as baseModule
from com.log import getLogger
from com import processutils
from config.configuration import CONF

VERSION = "1.0.1"
LOG = getLogger()

class Module(baseModule):
    def __init__(self, version):
        super(Module, self).__init__("Diag BlackBox", version)
        LOG.info("enter into __init__.")

        self.content = dict(rawlog=list())

    def prepare(self):
        super(Module, self).prepare()
        LOG.info("enter into prepare.")

        if len(self.files) != 1:
            err_msg = "files is invalid, files : %s" % self.files
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        filename = self.files[0]

        try:
            with open(filename, 'r') as f:
                out = f.read()

            if out:
                lines = out.split("\n")
                for line in lines:
                    line = line.strip()
                    if line == "":
                        continue

                    self.content['rawlog'].append(line)
        except:
            LOG.error(traceback.format_exc())
            err_msg = "Parse blackbox failed."
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        return True, ""

    def _diag_cpu_vr_fault(self):
        try:
            for line in self.content['rawlog']:
                if "CPU VR FAULT ASSERTED" in line:
                    dict_info = dict(datetime="", description="")
                    r = re.match(r"^\[(?P<datetime>[\w\s\w\s\w\s\d:\d:\d]+)\]\s*:\s*(?P<description>[\w|\s]+)", line)
                    if r:
                        dict_info.update(r.groupdict())

                    log_time = datetime.datetime.strptime(dict_info['datetime'], '%b %d %Y %H:%M:%S')
                    if not self.timestamp:
                        now_time = datetime.datetime.now()
                    else:
                        now_time = datetime.datetime.strptime(self.timestamp, '%Y%m%d%H%M%S')

                    delta = now_time - log_time
                    if delta.seconds >= 0 and delta.seconds < CONF.DELTA_MAX_SECONDS:
                        self.result = CONF.FAULT
                        self.source.append('mainboard')
                        self.cause.append(line)
                        break
        except:
            LOG.error(traceback.format_exc())
            err_msg = "_diag_log abord."
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

    def diagnostic(self):
        super(Module, self).diagnostic()
        LOG.info("enter into diagnostic.")

        self._diag_cpu_vr_fault()

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
