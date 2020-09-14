#include <gflags/gflags.h>
#include <iostream>
#include <string>

#include "venus_engine.h"
#include "define.h"


using namespace std;
using namespace venus;

#define DEMO_APP_VERSION "1.0.0"

DEFINE_bool(r, false, "read register value");
DEFINE_bool(w, false, "write register value");
DEFINE_int32(addr, -1, "the register addr");
DEFINE_int32(mask, 0, "the register mask");
DEFINE_int32(value, -1, "the register value");
DEFINE_string(name, "", "the software property name");

/*
static bool ValidateAddr(const char* name, int32_t value) {
    if (value >  0 && value < 0xffff) {
        return true;
    }
    printf("Invalid value for %s: %d\n", name, (int)value);
    return false;
}

static const bool addr_dummy = gflags::RegisterFlagValidator(&FLAGS_addr, &ValidateAddr);

*/

static bool ValidateMask(const char* name, int32_t value) {
    if (value >=  0) {
        return true;
    }
	
    printf("Invalid value for %s: %d\n", name, (int)value);
    return false;
}

static const bool mask_dummy = gflags::RegisterFlagValidator(&FLAGS_mask, &ValidateMask);

static bool ValidateValue(const char* name, int32_t value) {
    if (FLAGS_w && value <  0) {
		printf("Invalid value for %s: %d, must be > 0\n", name, (int)value);
    	return false;
	}

    return true;
}

static const bool value_dummy = gflags::RegisterFlagValidator(&FLAGS_value, &ValidateValue);

int main(int argc,char* argv[]) {
	
	gflags::SetVersionString(DEMO_APP_VERSION);
	string usage_str = "Usage:";
	usage_str+=argv[0];
	gflags::SetUsageMessage(usage_str);
	gflags::ParseCommandLineFlags(&argc, &argv, true);

	std::cout << "addr:" << FLAGS_addr << std::endl;
	std::cout << "mask:" << FLAGS_mask << std::endl;
	std::cout << "value:" << FLAGS_value << std::endl;
	std::cout << "name:" << FLAGS_name << std::endl;

	VENUS_DEBUG_LOG("addr : 0x%x", FLAGS_addr);
	printf("%s, %d\n", __func__, __LINE__);
	DemoLib *DemoLib = DemoLib::getInstance();
	printf("DemoLib = %p\n", DemoLib);

	return 0;
}



