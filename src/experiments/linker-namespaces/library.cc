#include <iostream>
#include <string>
#include "plugin_impl.h"

extern "C" {
  PluginInterface* createPlugin() {
    std::cout << "createPlugin Library" << std::endl;
    auto ret = new PluginImpl();
    return ret;
  }
}
