# All Rights Reserved.

import os
import sys
import traceback
import csv
import shutil
import time, datetime
from base import Module as baseModule
from com.log import getLogger
from com import processutils
from config.configuration import CONF

VERSION = "1.0.0"
LOG = getLogger()

class Module(baseModule):
    def __init__(self, version):
        super(Module, self).__init__("Diag Huawei Arm", version)
        LOG.info("enter into __init__.")

        self.content = dict(sel=list(),
                            fdm_log="",
                            fdm_out_out=""
                            )

        self.sel_check_list_dict = ["0x0000001D", "0x08000001", "0x06000007", "0x02000013", "0x01000017"]

    def prepare(self):
        super(Module, self).prepare()
        LOG.info("enter into prepare.")

        if len(self.files) != 1:
            err_msg = "files is invalid, files : %s" % self.files
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        filename = self.files[0]

        cmd = "tar -zxvf %s" % filename
        out, err = processutils.trycmd(cmd, shell=True, timeout_sec=10)
        if err:
            err_msg = "execute %s fail. %s" % (cmd, err)
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        sensor_alarm_log_path = "./dump_info/AppDump/sensor_alarm"
        cmd = "tar -xvf %s/sel.tar" % sensor_alarm_log_path
        out, err = processutils.trycmd(cmd, shell=True, timeout_sec=10)
        if err:
            err_msg = "execute %s fail. %s" % (cmd, err)
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        with open("eo_sel.csv", 'r') as f:
            spamreader = csv.reader(f)
            for idx, row in enumerate(spamreader):
                if idx == 0:
                    continue

                self.content['sel'].append(row)

        with open("./dump_info/LogDump/fdm_log", 'r') as f:
            fdm_log = f.read()
            self.content['fdm_log'] = fdm_log

        with open("./dump_info/LogDump/fdm_output", 'r') as f:
            fdm_out_out = f.read()
            self.content['fdm_out_out'] = fdm_out_out


        try:
            os.remove('eo_sel.csv')
            shutil.rmtree('dump_info')
        except:
            LOG.error("remove fail.")

        return True, ""

    def diagnostic(self):
        super(Module, self).diagnostic()
        LOG.info("enter into diagnostic111.")

        try:
            deasserted_list = list()
            for sel in self.content['sel']:
                if sel[5] == 'Deasserted':
                    deasserted_list.append(dict(id=sel[0], description=sel[3], gen_time=sel[4], event_code=sel[6]))

            LOG.debug("deasserted_list : %s" % deasserted_list)

            for sel in self.content['sel']:
                if sel[5] == 'Asserted':
                    event_code = int(sel[6], 16)
                    try:
                        a_time = datetime.datetime.strptime(sel[4], '%Y-%m-%d %H:%M:%S')
                    except:
                        a_time = datetime.datetime.strptime(sel[4], '%Y/%m/%d %H:%M')

                    for deasserted in deasserted_list:
                        if int(deasserted['event_code'], 16) == event_code + 1:
                            try:
                                d_time = datetime.datetime.strptime(deasserted['gen_time'], '%Y-%m-%d %H:%M:%S')
                            except:
                                d_time = datetime.datetime.strptime(sel[4], '%Y/%m/%d %H:%M')

                            delta = d_time - a_time

                            if delta.days >= 0 and deasserted['description'] == sel[3]:
                                LOG.info("(id:%s, event_code:%s) is asserted and is already deasserted (id:%s, event_code:%s)"
                                         % (sel[0], sel[6], deasserted['id'], deasserted['event_code']))
                                break
                    else:
                        if sel[6] in self.sel_check_list_dict:
                            if not self.timestamp:
                                now_time = datetime.datetime.now()
                            else:
                                now_time = datetime.datetime.strptime(self.timestamp, '%Y%m%d%H%M%S')

                            delta = now_time - a_time
                            if delta.seconds >= 0 and delta.seconds < CONF.DELTA_MAX_SECONDS:
                                LOG.debug(sel)
                                self.result = CONF.FAULT
                                self.source.append(sel[2])
                                self.cause.append(sel[3])
        except:
            LOG.error(traceback.format_exc())
            err_msg = "diagnose abord."
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
