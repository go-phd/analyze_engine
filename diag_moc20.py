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

VERSION = "1.0.0"
LOG = getLogger()

class Module(baseModule):
    def __init__(self, version):
        super(Module, self).__init__("Diag MOC 20", version)
        LOG.info("enter into __init__.")

        self.content = dict(messages=list()
                            )

    def prepare(self):
        super(Module, self).prepare()
        LOG.info("enter into prepare.")

        if len(self.files) != 1:
            err_msg = "files is invalid, files : %s" % self.files
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        filename = self.files[0]

        cmd = "tar -xvf %s" % filename
        out, err = processutils.trycmd(cmd, shell=True, timeout_sec=10)
        if err:
            err_msg = "execute %s fail. %s" % (cmd, err)
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        with open("./onekeylog/LogDump/operate_log/messages", 'r') as f:
            out = f.read()

        if out:
            lines = out.split("\n")
            try:
                for line in lines:
                    line = line.strip()
                    if line == "":
                        continue

                    self.content['messages'].append(line)
            except:
                LOG.error(traceback.format_exc())
                err_msg = "Parse messages failed."
                LOG.error(err_msg)
                self.set_unknown(err_msg)
                return False, err_msg

        return True, ""

    def _diag_lbtn_pwrdown(self):
        try:
            for line in self.content['messages']:
                if "Write CPLD BMC_LBTN_PWRDOWN_CTL_BIT Successfully" in line:
                    dict_info = dict(datetime="")
                    r = re.match(r"^(?P<datetime>[\w\s\w\s\w\s\d:\d:\d]+)[\s|\w]*", line)
                    if r:
                        dict_info.update(r.groupdict())

                    log_time = datetime.datetime.strptime(dict_info['datetime'].strip(), '%b %d %H:%M:%S')
                    if not self.timestamp:
                        now_time = datetime.datetime.now()
                    else:
                        now_time = datetime.datetime.strptime(self.timestamp, '%Y%m%d%H%M%S')
                    delta = now_time - log_time
                    LOG.debug(delta)

                    if delta.seconds >= 0 and delta.seconds < CONF.DELTA_MAX_SECONDS:
                        self.result = CONF.FAULT
                        self.source.append('Human Error')
                        self.cause.append(line)
                        break

        except:
            LOG.error(traceback.format_exc())
            err_msg = "_diag_lbtn_pwrdown abord."
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

    def diagnostic(self):
        super(Module, self).diagnostic()
        LOG.info("enter into diagnostic.")

        self._diag_lbtn_pwrdown()

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
