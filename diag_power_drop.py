# All Rights Reserved.

import sys
import traceback
import re
import copy
import datetime
from base import Module as baseModule
from com.log import getLogger
from config.configuration import CONF

VERSION = "1.0.3"
LOG = getLogger()

class Module(baseModule):
    def __init__(self, version):
        super(Module, self).__init__("Diag Power Drop", version)
        LOG.info("enter into __init__.")

        self.content = dict(sel=[],
                            event_data_raw=dict()
                            )

        self.power_drop_dict = {
            (CONF.INSPUR_VENDER, CONF.INVENTEC_VENDER):
                [
                    dict(err_code="0x00", signal="P1V8_PCH_STBY", source="Mainboard(PCH)"),
                    dict(err_code="0x01", signal="PVNN_PCH_STBY", source="Mainboard(PCH)"),
                    dict(err_code="0x02", signal="P1V05_PCH_STBY", source="Mainboard(PCH)"),
                    dict(err_code="0x03", signal="PCH_SLP_S4_N", source="Mainboard(PCH)"),
                    dict(err_code="0x04", signal="P12V", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x05", signal="P5V", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x06", signal="P3V3", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x07", signal="P2V5_M0_ABC_VPP", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x08", signal="P2V5_M0_DEF_VPP", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x09", signal="P2V5_M1_ABC_VPP", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0a", signal="P2V5_M1_DEF_VPP", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0b", signal="PVDDQ_CPU0_ABC_DDR4", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0c", signal="PVDDQ_CPU0_DEF_DDR4", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0d", signal="PVDDQ_CPU1_ABC_DDR4", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0e", signal="PVDDQ_CPU1_DEF_DDR4", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0f", signal="P0V6_M0_ABC_VTT", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x10", signal="P0V6_M0_DEF_VTT", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x11", signal="P0V6_M1_ABC_VTT", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x12", signal="P0V6_M1_DEF_VTT", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x13", signal="PVCCIO_CPU0", source="Mainboard(CPU0)"),
                    dict(err_code="0x14", signal="PVCCIO_CPU1", source="Mainboard(CPU1)"),
                    dict(err_code="0x15", signal="PVCCIN_CPU0", source="Mainboard(CPU0)"),
                    dict(err_code="0x16", signal="PVCCIN_CPU1", source="Mainboard(CPU1)"),
                    dict(err_code="0x17", signal="PVCCSA_CPU0", source="Mainboard(CPU0)"),
                    dict(err_code="0x18", signal="PVCCSA_CPU1", source="Mainboard(CPU1)"),
                    dict(err_code="0x19", signal="PGD_PROC_PWRGD_CPLD", source="Reserve(PCH)"),
                    dict(err_code="0x1a", signal="PGD_PCH_PWROK", source="Reserve(PCH)"),
                    dict(err_code="0x1b", signal="PGD_SYS_PWROK", source="Reserve(PCH)"),
                    dict(err_code="0x1c", signal="PLTRST_N", source="Reserve(PCH)")
                ],
            (CONF.FOXCON_VENDER):
                [
                    dict(err_code="0x00", signal="Indicate CPU0 P2V5 VPP ABC MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x01", signal="Indicate CPU1 P2V5 VPP ABC MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x02", signal="Indicate CPU0 P2V5 VPP DEF MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x03", signal="Indicate CPU1 P2V5 VPP DEF MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x04", signal="Indicate P3V3 main power fault", source="Mainboard(SYS)"),
                    dict(err_code="0x05", signal="Indicate P5V main power fault", source="Mainboard(SYS)"),
                    dict(err_code="0x06", signal="Indicate 12V main power fault", source="Mainboard(SYS)"),
                    dict(err_code="0x07", signal="Indicate CPU0 PVTT ABC MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x08", signal="Indicate CPU1 PVTT ABC MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x09", signal="Indicate CPU0 PVTT DEF MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0a", signal="Indicate CPU1 PVTT DEF MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0b", signal="Indicate CPU0 PVDDQ ABC MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0c", signal="Indicate CPU1 PVDDQ ABC MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0d", signal="Indicate CPU0 PVDDQ DEF MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0e", signal="Indicate CPU1 PVDDQ DEF MEM power fault", source="Mainboard(MEMOEY)"),
                    dict(err_code="0x0f", signal="Indicate CPU0 PVCCSA power fault", source="Mainboard(CPU0)"),
                    dict(err_code="0x10", signal="Indicate CPU1 PVCCSA power fault", source="Mainboard(CPU1)"),
                    dict(err_code="0x11", signal="Indicate CPU0 PVCCIN power fault", source="Mainboard(CPU0)"),
                    dict(err_code="0x12", signal="Indicate CPU1 PVCCIN power fault", source="Mainboard(CPU1)"),
                    dict(err_code="0x13", signal="Indicate CPU0 PVCCIO power fault", source="Mainboard(CPU0)"),
                    dict(err_code="0x14", signal="Indicate CPU1 PVCCIO power fault", source="Mainboard(CPU1)"),
                    dict(err_code="0x15", signal="Indicate PCH PVNN AUX power fault", source="Mainboard(PCH)"),
                    dict(err_code="0x16", signal="Indicate PCH P1V05 AUX power fault", source="Mainboard(PCH)")
                ]
        }

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
                segments = out.split("\n\n")
                for segment in segments:
                    if 'SEL Record ID' not in segment:
                        lines = segment.split("\n")
                        for line in lines:
                            self.content['sel'].append(line)
                    else:
                        power_drop = segment.strip()
                        lines = power_drop.split("\n")

                        for line in lines:
                            if "Event Data (RAW)" in line:
                                key = line.split(':')[0].strip()
                                value = line.split(':')[1].strip()

                                event_data_raw = dict(
                                    key=key,
                                    value=value,
                                    result=None
                                )

                                self.content.update(dict(event_data_raw=event_data_raw))
                                return True, ""
        except:
            LOG.error(traceback.format_exc())
            err_msg = "parse file failed. file : %s" % filename
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        return True, ""

    def diagnostic(self):
        super(Module, self).diagnostic()
        LOG.info("enter into diagnostic.")

        for vender in self.power_drop_dict:
            if self.vender in vender:
                power_drop_list = self.power_drop_dict[vender]
                break
        else:
            err_msg = "vender is invalid, vender : %s" % self.vender
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        try:
            for line in self.content['sel']:
                if 'Power_drop' in line:
                    data = line.split('|')[1].strip()
                    time = line.split('|')[2].strip()
                    a_time = data + ' ' + time

                    log_time = datetime.datetime.strptime(a_time, '%m/%d/%Y %H:%M:%S')
                    if not self.timestamp:
                        now_time = datetime.datetime.now()
                    else:
                        now_time = datetime.datetime.strptime(self.timestamp, '%Y%m%d%H%M%S')

                    delta = now_time - log_time
                    LOG.debug(delta)

                    if delta.seconds >= 0 and delta.seconds < CONF.DELTA_MAX_SECONDS:
                        self.result = CONF.FAULT
                        LOG.info("have power drop sel : %s" % line)
                        break
            else:
                return True, ""
        except:
            LOG.error(traceback.format_exc())
            err_msg = "parse selfail."
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        if self.content.has_key('event_data_raw'):
            value = self.content['event_data_raw']['value']
            err_code = '0x' + re.findall(r'.{2}', value)[1]

            try:
                for power_drop in power_drop_list:
                    if power_drop['err_code'] == err_code:
                        self.content['event_data_raw']['result'] = copy.deepcopy(power_drop)
                        break
                else:
                    err_msg = "no match err code : %s" % value
                    LOG.error(err_msg)
                    self.set_unknown(err_msg)
                    return False, err_msg
            except:
                LOG.error(traceback.format_exc())
                err_msg = "no match err code : %s" % value
                LOG.error(err_msg)
                self.set_unknown(err_msg)
                return False, err_msg

        return True, ""

    def finish(self):
        super(Module, self).finish()
        LOG.info("enter into finish.")

        if self.content.has_key('event_data_raw'):
            if self.content['event_data_raw'].has_key('result') and self.content['event_data_raw']['result']:
                self.result = CONF.FAULT

                result = self.content['event_data_raw']['result']
                self.source.append(result['source'])
                self.cause.append(result['signal'])

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
