//
/// Copyright (c) 2018 Alibaba-inc.
///
/// All rights reserved.
/// @file   logger.h
/// @brief
/// @author  chenyan
/// @version 1.0
/// @date    2019-12-27

#ifndef VENUSLOG_H
#define VENUSLOG_H

#include <log4cplus/logger.h>
#include <log4cplus/fileappender.h>
#include <log4cplus/layout.h>
#include <log4cplus/ndc.h>
#include <log4cplus/helpers/loglog.h>
#include <log4cplus/helpers/property.h>
#include <log4cplus/loggingmacros.h>


#include <stdint.h>
#include <string>
#include <algorithm>

#include "define.h"

#define LOGGER_PATH "/var/log/venus/venus_engine_cpp.log"

using namespace log4cplus;

namespace venus {
	extern Logger g_logger;
	
	class VenusLog {
	public:
		VenusLog(void);
		~VenusLog(void);
		static VenusLog* getInstance();

	private:
		static VenusLog *instance;
	};

#define VENUS_DEBUG_LOG(...) do {\
		LOG4CPLUS_DEBUG_FMT(g_logger, __VA_ARGS__);\
	}while(0)
	
#define VENUS_INFO_LOG(...) do {\
		LOG4CPLUS_INFO_FMT(g_logger, __VA_ARGS__);\
	}while(0)

#define VENUS_ERROR_LOG(...) do {\
		LOG4CPLUS_ERROR_FMT(g_logger, __VA_ARGS__);\
	}while(0)

}

#endif


