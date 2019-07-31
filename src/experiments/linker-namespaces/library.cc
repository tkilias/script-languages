#include <iostream>
#include <string>
#include "library.h"

struct PluginImpl : PluginInterface {

    void start() override {
    	std::cout << "Plugin::start" << std::endl;
    }
    
    void destroy_string(std::string* not_my_string) override {
    	std::cout << "Plugin::destroy_string(not_my_string)" << std::endl;
	delete not_my_string;
    }

    ~PluginImpl() override {
	std::cout << "Destroy PluginImpl" << std::endl;
    }
};


extern "C" {
  PluginInterface* createPlugin() {
    std::cout << "createPlugin" << std::endl;
    auto ret = new PluginImpl();
    return ret;
  }
}
