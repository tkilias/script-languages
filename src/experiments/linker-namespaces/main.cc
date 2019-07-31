#include <dlfcn.h>
#include <iostream>
#include <assert.h>
#include <string>
#include "library.h"

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
	auto handle = dlmopen(LM_ID_NEWLM, library_path.c_str(), RTLD_NOW);

	PluginInterface* (*fn)(void) = reinterpret_cast<PluginInterface* (*)(void)>(dlsym(handle, "createPlugin"));
	assert(fn != nullptr);
	auto plugin = fn();
	plugin->start();
	auto my_string = new std::string("test");
	plugin->destroy_string(my_string);
	
	std::cout << "Attempting to delete plugin from library namespace in main namespace" << std::endl;
	delete plugin;
	std::cout << "END main()" << std::endl;
	return 0;
}
