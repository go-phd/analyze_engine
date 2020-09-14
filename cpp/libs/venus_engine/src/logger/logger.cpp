
#include "logger.h"

using namespace std;

namespace venus {
	Logger g_logger;
		
	VenusLog::VenusLog(){
        log4cplus::initialize ();
        //helpers::LogLog::getLogLog()->setInternalDebugging(true);	//log4cplus debug info

        /* step 1: Instantiate an appender object */
        SharedFileAppenderPtr _append(
	        new RollingFileAppender(LOG4CPLUS_TEXT(LOGGER_PATH), 512*1024, 4,
	            true, true));
        _append->setName(LOG4CPLUS_TEXT("venus_log"));

        /* step 2: Instantiate a layout object */
        string pattern = "%D{%Y/%m/%d %H:%M:%S} [%p]  - %m [%l]%n";

        /* step 3: Attach the layout object to the appender */
        //_append->setLayout( std::auto_ptr<Layout>(new TTCCLayout()) );
        //_append->getloc();
        _append->setLayout(std::auto_ptr<Layout>(new PatternLayout(pattern)));

        /* step 4: Instantiate a logger object */
        g_logger = Logger::getInstance(LOG4CPLUS_TEXT("[VENUS]"));

        /* step 5: Attach the appender object to the logger  */
        g_logger.addAppender(SharedAppenderPtr(_append.get()));

        VENUS_INFO_LOG("VenusLog init ok");
	}
	 
	VenusLog::~VenusLog(){
        log4cplus::Logger::shutdown();
	}

	VenusLog *VenusLog::instance = new VenusLog();

}


