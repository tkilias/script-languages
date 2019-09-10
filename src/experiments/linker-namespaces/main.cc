#include <dlfcn.h>
#include <iostream>
#include <assert.h>
#include <string>
#include "plugin.h"

void check_load_error(void* handle){
  if(!handle){
    std::cout << "Error:" << dlerror() << std::endl;
    exit(-1);
  }
}

void* load_in_base_namespace_via_dlmopen(std::string& library_path){	
	auto namespace_id = LM_ID_BASE;
	std::cout << "load via dlmopen  in namespace LM_ID_BASE" << std::endl;
	auto handle = dlmopen(namespace_id, library_path.c_str(), RTLD_NOW);
  check_load_error(handle);
  return handle;
}

void* load_in_new_namespace_via_dlmopen(std::string& library_path){	
	auto namespace_id = LM_ID_NEWLM;
	std::cout << "load via dlmopen in namespace LM_ID_NEWLM" << std::endl;
	auto handle = dlmopen(namespace_id, library_path.c_str(), RTLD_NOW);
  check_load_error(handle);
  return handle;
}

void* load_via_dlopen(std::string& library_path){	
	std::cout << "load via dlopen" << std::endl;
	auto handle = dlopen(library_path.c_str(), RTLD_NOW);
  check_load_error(handle);
  return handle;
}

int main(int argc, char *argv[]) {
	std::cout << "START main()" << std::endl;

	if(argc!=2){
		std::cerr << "Path is missing in commandline parameter" << std::endl;
		return 1;
	}

	auto path = std::string{argv[1]};
	std::cout << "Path: " << path << std::endl;

	auto library_path = path+"/library.so";
	std::cout << "LibraryPath: " << library_path << std::endl;
	
//  auto handle = load_in_new_namespace_via_dlmopen(library_path);
//  auto handle = load_in_base_namespace_via_dlmopen(library_path);
  auto handle = load_via_dlopen(library_path);
  
  std::cout << "handle:" << handle << std::endl;

	PluginInterface* (*fn)(void) = reinterpret_cast<PluginInterface* (*)(void)>(dlsym(handle, "createPlugin"));
	assert(fn != nullptr);
	auto plugin = fn();
	
	plugin->start();

  std::string* strFromLibrary=plugin->createString();
	std::cout << "Attempting to delete string from Plugin in main namespace" << std::endl;
  delete strFromLibrary;

  std::string* strFromMain=new std::string("String from Main");
  plugin->destroyString(strFromMain);

	std::cout << "Attempting to delete plugin from library namespace in main namespace" << std::endl;
	delete plugin;
	std::cout << "END main()" << std::endl;
	return 0;
}
