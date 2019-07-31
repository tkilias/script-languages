package(default_visibility = ["//visibility:public"])

cc_binary(
	name = "library.so",
	linkshared = 1,
	srcs = 
    		[
		"library.cc",
		"library.h"
		],
)

cc_binary(
	name = "main",
	linkopts = ["-ldl"],
	srcs = 
		[
		"library.h",
		"main.cc"
		],
)
