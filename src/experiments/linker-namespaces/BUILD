package(default_visibility = ["//visibility:public"])

cc_library(
	name = "plugin",
	srcs = 
    		[
		"plugin_impl.cc",
		"plugin.h",
		"plugin_impl.h"
		],
	hdrs = ["plugin.h"]
)

cc_binary(
	name = "library.so",
	linkshared = 1,
	srcs = [
		"library.cc",
		],
	deps = ["plugin"]
)

cc_binary(
	name = "main",
	linkopts = ["-ldl"],
	srcs = 
		[
		"main.cc",
    "plugin.h"
		],
)
