# All Rights Reserved.

import sys
import datetime
from pprint import pprint
import traceback
from optparse import OptionParser
from com.log import getLogger
from config.configuration import CONF

LOG = getLogger()

def option_parser(version):
    parser = OptionParser(version=version,
                          usage=("Usage: %prog [options]\n "
                                 "Venus Enigne Tools."))
    parser.add_option('-p', '--platform', dest='platform',
                      default=CONF.UNKNOWN_PLATFORM,
                      choices=[CONF.GRANTLEY_PLATFORM, CONF.PURLEY_PLATFORM, CONF.WHITLEY_PLATFORM,
                               CONF.CEDAR_IDLAND_PLATFORM, CONF.UNKNOWN_PLATFORM],
                      help="cpu platform [%s, %s, %s, %s, %s]" % (
                      CONF.GRANTLEY_PLATFORM, CONF.PURLEY_PLATFORM, CONF.WHITLEY_PLATFORM, CONF.CEDAR_IDLAND_PLATFORM,
                      CONF.UNKNOWN_PLATFORM))
    parser.add_option('-v', '--vender', dest='vender',
                      default=CONF.UNKNOWN_VENDER,
                      choices=[CONF.INSPUR_VENDER, CONF.INVENTEC_VENDER, CONF.FOXCON_VENDER, CONF.UNKNOWN_VENDER],
                      help="vender [%s, %s, %s,  %s]" % (
                          CONF.INSPUR_VENDER, CONF.INVENTEC_VENDER, CONF.FOXCON_VENDER, CONF.UNKNOWN_VENDER))
    parser.add_option('-t', '--timestamp', dest='timestamp',
                      default=None,
                      help="timestamp format is %Y%m%d%H%M%S, example:20191226100526.")
    parser.add_option('-f', '--file', dest='file',
                      default='',
                      help="file for analysis.")

    return parser

class Module(object):
    def __init__(self, name="Base", version=""):
        LOG.info("enter into __init__.")
        self.name = name
        self.version = version
        self.result = CONF.HEALTH
        self.source = list()
        self.cause = list()
        self.content = None

        try:
            parser = option_parser(version)
            opts, args = parser.parse_args()
        except:
            LOG.error(traceback.format_exc())
            sys.exit(1)

        self.platform = opts.platform
        self.vender = opts.vender
        self.timestamp = opts.timestamp
        if opts.file:
            self.files = opts.file.split(",")
        else:
            self.files = []
        LOG.info("platform : %s, vender : %s, timestamp : %s, files : %s" % (self.platform, self.vender, self.timestamp, self.files))

    def check(self):
        LOG.info("enter into check.")
        return True, ""

    def prepare(self):
        LOG.info("enter into prepare.")
        ret, err = self.check()
        if not ret:
            return ret, err

        return True, ""

    def diagnostic(self):
        LOG.info("enter into diagnostic.")

    def finish(self):
        LOG.info("enter into finish.")

    def output(self):
        output_data = dict(name=self.name,
                           version=self.version,
                           timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           diagnosis=dict(result=self.result,
                                          source=self.source,
                                          cause=self.cause,
                                          content=self.content
                                          )
                           )

        pprint(output_data)

    def set_unknown(self, err_msg):
        self.cause.append(err_msg)
        self.result = CONF.UNKNOWN