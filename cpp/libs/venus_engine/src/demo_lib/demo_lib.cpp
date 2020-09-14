
#include "demo_lib.h"
#include "logger.h"


namespace venus {
	DemoLib::DemoLib(){
		VENUS_INFO_LOG("DemoLib init ok");
	}

	DemoLib::~DemoLib(){
		VENUS_INFO_LOG("DemoLib exit ok");
	}

	DemoLib *DemoLib::instance = NULL;

	DemoLib* DemoLib::getInstance(){
		if (!instance) {
			instance = new DemoLib();
		}

		return instance;
	}
}


