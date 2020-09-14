//
/// Copyright (c) 2018 Alibaba-inc.
///
/// All rights reserved.
/// @file   demo_lib.h
/// @brief
/// @author  chenyan
/// @version 1.0
/// @date    2019-12-27

#ifndef DEMO_LIB_H
#define DEMO_LIB_H

#include <stdint.h>
#include <string>
#include <algorithm>

#include "define.h"



namespace venus {
	class DemoLib {
	public:
		DemoLib(void);
		~DemoLib(void);
		static DemoLib* getInstance();

	private:
		static DemoLib *instance;
	};
}

#endif


