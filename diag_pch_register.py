# All Rights Reserved.

import sys
import traceback
import re
from base import Module as baseModule
from com.log import getLogger
from config.configuration import CONF

VERSION = "1.0.3"

LOG = getLogger()

class Module(baseModule):
    def __init__(self, version):
        super(Module, self).__init__("Diag PCH Register", version)
        LOG.info("enter into __init__.")

        self.content = dict()
        self.content["registers"] = list()

        self.grantley_dict = {
            "0x00 0x03":
                [
                    dict(cause="BIT0: Host Partition Reset Timeout", source="Unknown"),
                    dict(cause="BIT1: Sx Entry Timeout", source="Reserve"),
                    dict(cause="BIT2: Host Partition Reset Promotion", source="Unknown"),
                    dict(cause="BIT3: Host SMBus Message", source="Reverve"),
                    None,
                    dict(cause="BIT5: ME Set Power Button Status", source="Mainboard(ME)"),
                    None,
                    None
                ],
            "0x03 0x03":
                [
                    dict(cause="BIT0: SUS Well Power Failure Status", source="Power Error"),
                    dict(cause="BIT1: Power Button Override", source="Human Error"),
                    None,
                    dict(cause="BIT3: PCH Catastrophic Temperature Event", source="Mainboard(PCH)"),
                    dict(cause="BIT4: ME-Initiated Power Button Override", source="Mainboard(ME)"),
                    dict(cause="BIT5: CPU Thermal Trip", source="Mainboard(CPU)"),
                    dict(cause="BIT6: ME-Initiated Global Reset", source="Mainboard(ME)"),
                    dict(cause="BIT7: TXT Reset# With Policy 1", source="TXT")
                ],
            "0x04 0x03":
                [
                    dict(cause="BIT0: Reset control Firmware Watchdog Timer", source="Mainboard(Firmware)"),
                    dict(cause="BIT1: ME Firmware Watchdog Timer", source="Mainboard(ME)"),
                    dict(cause="BIT2: Global Reset Firmware", source="Mainboard(Firmware reset)"),
                    dict(cause="BIT3: PCH_PWROK Failure", source="Mainboard(PCH_PWROK Loss)"),
                    dict(cause="BIT4: SYS_PWROK Failure", source="Mainboard(SYS_PWROK loss)"),
                    dict(cause="BIT5: AS Well Power Failure", source="Mainboard(ASW power loss)"),
                    dict(cause="BIT6: After G3 Status", source="Mainboard G3"),
                    None
                ],
            "0x05 0x03":
                [
                    dict(cause="BIT0: RWC 0b Resume CPU Thermal Runaway Watchdog Timer", source="Mainboard(CPU)"),
                    dict(cause="BIT1: RWC 0b Resume ME HW Uncorrectable Error", source="Mainboard(ME)"),
                    dict(cause="BIT2: ADR Reset", source="Mainboard(ADR GPIO)"),
                    None,
                    None,
                    None,
                    None,
                    None
                ]
        }

        self.purley_dict = {
            "0xfc 0x02":
                [
                    None,
                    dict(cause="BIT1: AC RU Error", source="Reserve"),
                    dict(cause="BIT2: IE Firmware Watchdog Timer", source="Mainboard(IE)"),
                    dict(cause="BIT3: IE HW Uncorrectable Error", source="Mainboard(IE)"),
                    dict(cause="BIT4: IE Unexpected Shutdown Error", source="Mainboard(IE)"),
                    dict(cause="BIT5: IE Unexpected Error", source="Mainboard(IE)"),
                    dict(cause="BIT6: IE-Initiated Power Button Override", source="Mainboard(IE)"),
                    dict(cause="BIT7: IE-Initiated Global Reset", source="Mainboard(IE)")
                 ],
            "0x00 0x03":
                [
                    dict(cause="BIT0: Host Partition Reset Timeout", source="Unknown"),
                    dict(cause="BIT1: Sx Entry Timeout", source="Reserve"),
                    dict(cause="BIT2: Host Partition Reset Promotion", source="Unknown"),
                    dict(cause="BIT3: Host SMBus Message", source="Human Error"),
                    dict(cause="BIT4: PMC 3 Strike Boot Failure Counter", source="Mainboard"),
                    None,
                    None,
                    None
                 ],
            "0x01 0x03":
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    dict(cause="BIT7: IE Set Power Button Status", source="Mainboard(IE)")
                ],
            "0x03 0x03":
                [
                    None,
                    dict(cause="BIT1: Power Button Override", source="Human Error"),
                    dict(cause="BIT2: PMC SUS RAM Uncorrectable Error", source="Power Error"),
                    dict(cause="BIT3: PCH Catastrophic Temperature Event", source="Mainboard(PCH)"),
                    dict(cause="BIT4: ME-Initiated Power Button Override", source="Mainboard(ME)"),
                    dict(cause="BIT5: CPU Thermal Trip", source="Mainboard(CPU)"),
                    dict(cause="BIT6: ME-Initiated Global Reset", source="Mainboard(ME)"),
                    None
                ],
            "0x04 0x03":
                [
                    dict(cause="BIT0: PMC Watchdog Timer", source="Power Error"),
                    dict(cause="BIT1: ME Firmware Watchdog Timer", source="Mainboard(ME)"),
                    dict(cause="BIT2: PMC Global Reset", source="Power Error"),
                    dict(cause="BIT3: PCH_PWROK Failure", source="Mainboard(PCH)"),
                    dict(cause="BIT4: SYS_PWROK Failure", source="Mainboard(PCH)"),
                    None,
                    dict(cause="BIT6: Intel ME Unexpected Shutdown Error", source="Mainboard(ME)"),
                    dict(cause="BIT7: Intel ME Unexpected Error", source="Mainboard(ME)")
                ],
            "0x05 0x03":
                [
                    dict(cause="BIT0: CPU Thermal Runaway Watchdog Timer", source="Mainboard"),
                    dict(cause="BIT1: ME HW Uncorrectable Error", source="Mainboard(ME)"),
                    dict(cause="BIT2: ADR GPIO Reset", source="Mainboard(ADR GPIO)"),
                    None,
                    None,
                    None,
                    None,
                    None
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
        except:
            LOG.error(traceback.format_exc())
            err_msg = "Open file failed. file:%s" % filename
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        if out:
            segments = out.split("---")
            try:
                if self.platform == CONF.UNKNOWN_PLATFORM:
                    fru_info = segments[0].strip()
                    lines = fru_info.split("\n")
                    for line in lines:
                        if "Chassis Part Number" in line:
                            part_number = line.split(':')[1].strip()
                            number = list(re.findall('(\d+)', part_number)[0])[0]
                            if '3' in number or '4' in number:
                                self.platform = CONF.GRANTLEY_PLATFORM
                            elif '5' in number or '6' in number:
                                self.platform = CONF.PURLEY_PLATFORM
                            else:
                                err_msg = "Unknown platform: %s" % part_number
                                LOG.error(err_msg)
                                self.set_unknown(err_msg)
                                return False, err_msg

                            break
            except:
                LOG.error(traceback.format_exc())
                err_msg = "Not find valid platform"
                LOG.error(err_msg)
                self.set_unknown(err_msg)
                return False, err_msg


            try:
                for segment in segments:
                    if 'ipmitool' in segment:
                        pch_registers = segment.strip()
                        lines = pch_registers.split("\n\n")

                        for line in lines:
                            keys = line.split('\n')[0].strip()
                            key = keys.split(' ')[-2] + ' ' + keys.split(' ')[-1]

                            values = line.split('\n')[1].strip()
                            value = values.split(' ')[9]

                            register = dict(
                                key=key,
                                value=value,
                                result=list()
                            )

                            self.content["registers"].append(register)
                        break
            except:
                LOG.error(traceback.format_exc())
                err_msg = "Parse pch register failed."
                LOG.error(err_msg)
                self.set_unknown(err_msg)
                return False, err_msg

        return True, ""

    def diagnostic(self):
        super(Module, self).diagnostic()
        LOG.info("enter into diagnostic.")

        if self.platform == CONF.GRANTLEY_PLATFORM:
            diag_dict = self.grantley_dict
        elif self.platform == CONF.PURLEY_PLATFORM or self.platform == CONF.WHITLEY_PLATFORM or self.platform == CONF.CEDAR_IDLAND_PLATFORM:
            diag_dict = self.purley_dict
        else:
            err_msg = "Unknown platform : %s" % self.platform
            LOG.error(err_msg)
            self.set_unknown(err_msg)
            return False, err_msg

        def _get_bitvalue(value, idx):
            return (int(value, 16) >> idx) & 0x01

        for register in self.content["registers"]:
            try:
                key = register['key']
                value = '0x' + register['value']

                if diag_dict.has_key(key):
                    check_list = diag_dict[key]
                    for idx, check in enumerate(check_list):
                        if not check:
                            continue

                        bit_v = _get_bitvalue(value, idx)
                        if bit_v > 0:
                            register['result'].append(check)
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

        for register in self.content['registers']:
            if len(register['result']) > 0:
                self.result = CONF.FAULT
                for result in register['result']:
                    if not result['source'] in self.source:
                        self.source.append(result['source'])

                self.cause.extend(register['result'])


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
