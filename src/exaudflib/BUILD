package(default_visibility = ["//visibility:public"])
exports_files(["exascript.i"])

load("//:variables.bzl", "VM_ENABLED_DEFINES")

cc_library(
    name = "scriptoptionlines",
    hdrs = ["scriptoptionlines.h"],
    srcs = ["scriptoptionlines.cc","scriptoptionlines.h"],
    copts= ["-fno-lto"],
    # We deactivate link time optimization, because otherwise we get the following linker/compiler error while linking/compiling exaudfclient
    # function ExecutionGraph::extractOptionLine(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, unsigned long&, std::function<void (char const*)>): error: undefined reference to 'std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > std::operator+<char, std::char_traits<char>, std::allocator<char> >(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, char const*)'
)

cc_library(
    name = "script_data_transfer_objects",
    srcs = ["script_data_transfer_objects.cc","script_data_transfer_objects.h"],
    hdrs = ["script_data_transfer_objects.h"],
    copts= select({
        "//:benchmark": ["-fno-lto"],
        "//conditions:default": []
    })
    # We deactivate link time optimization for benchmark, 
    # because otherwise we get linker/compiler error while linking/compiling exaudfclient
    # Benchmark causes this, because it doesn't refer it its implementation.

)

cc_library(
    name = "script_data_transfer_objects_wrapper",
    srcs = ["script_data_transfer_objects_wrapper.cc","script_data_transfer_objects_wrapper.h"],
    deps = [":script_data_transfer_objects"],
    hdrs = ["script_data_transfer_objects_wrapper.h"],
    copts= select({
        "//:benchmark": ["-fno-lto"],
        "//conditions:default": []
    })
    # We deactivate link time optimization for benchmark,
    # because otherwise we get linker/compiler error while linking/compiling exaudfclient
    # Benchmark causes this, because it doesn't refer it its implementation.
)

# A collection target for the case that language container want to include all public headers of exaudflib
cc_library(
    name = "header",
    hdrs = [
        "exaudflib.h",
    ],
)

# A collection target for the case that language container want to depent on all public libraries of exaudflib
# which won't leak protobuf through linker namespaces. Caution: Can't be used for the target libexaudflib-complete.so,
# because this target declares the libraries only as deps.
cc_library( #TODO might be not working as expected
    name = "exaudflib-deps",
    deps = [":script_data_transfer_objects",":script_data_transfer_objects_wrapper"],
)

genrule(
    name = "zmqcontainer_proto",
    cmd = """
            TMPDIR=`mktemp -d`
            cp $< "$$TMPDIR"
            (cd "$$TMPDIR"
            $$PROTOBUF_BIN -I. zmqcontainer.proto --cpp_out=.)
            cp "$$TMPDIR"/zmqcontainer.pb.cc $(location zmqcontainer.pb.cc)
            cp "$$TMPDIR"/zmqcontainer.pb.h $(location zmqcontainer.pb.h)""",
    outs = ["zmqcontainer.pb.cc","zmqcontainer.pb.h"],
    srcs = ["zmqcontainer.proto"]
)

cc_library(
    name = "zmqcontainer",
    hdrs = [":zmqcontainer_proto"],
    srcs = [":zmqcontainer_proto"],
    deps = ["@protobuf//:protobuf"]
)

# Do not depend on this library in the langauge container or exaudfclient. 
# The only target which must depend on it is //:libexaudflib-complete.so.
# If you depend on this target you will load protobuf into your linker namespace
# which might cause problems with tensorflow. If you need //exaudflib:exaudflib.h,
# "//exaudflib:scriptoptionlines","//exaudflib:script_data_transfer_objects" or
# "//exaudflib:script_data_transfer_objects_wrapper" in the language container 
# depend directly on them
cc_library(
    name = "exaudflib",
    srcs = ["exaudflib.cc"],
    linkstatic = 1,
    defines = VM_ENABLED_DEFINES,
    deps = [":exaudflib-deps", ":zmqcontainer", "@zmq//:zmqlib", ":header", "//:debug_message_h"],
)
