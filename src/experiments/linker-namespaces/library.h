#include <iostream>
#include <string>

struct PluginInterface {

    virtual ~PluginInterface() { 
    	std::cout << "Destroy PluginInterface" << std::endl;
    }
    
    virtual void start() = 0;

    virtual void destroy_string(std::string* not_my_string) = 0;
};

//extern "C" {
//  PluginInterface* createPlugin();
//}
