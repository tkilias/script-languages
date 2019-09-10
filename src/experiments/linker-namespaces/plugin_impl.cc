#include <iostream>
#include <string>
#include "plugin_impl.h"


void PluginImpl::start() {
	std::cout << "Plugin::start" << std::endl;
}

PluginImpl::~PluginImpl() {
	std::cout << "Destroy PluginImpl" << std::endl;
}

std::string* PluginImpl::createString(){
	std::cout << "PluginImpl::createString" << std::endl;
  std::string* str =  new std::string("String from Plugin");
  return str;
}

void PluginImpl::destroyString(std::string* str){
	std::cout << "PluginImpl::destroyString" << std::endl;
  delete str;
}
