#include <iostream>
#include <string>

struct PluginInterface {

    virtual ~PluginInterface() { 
    	std::cout << "Destroy PluginInterface" << std::endl;
    }
    
    virtual void start() = 0;
    
    virtual std::string* createString() = 0;

    virtual void destroyString(std::string* str) = 0;

};
