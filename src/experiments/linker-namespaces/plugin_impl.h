#include "plugin.h"

struct PluginImpl : PluginInterface {
	void start() override;
	
  std::string* createString() override;

  void destroyString(std::string* str) override;

	~PluginImpl() override;

};
