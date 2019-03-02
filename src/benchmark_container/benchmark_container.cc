#ifndef ENABLE_BENCHMARK_VM
#define ENABLE_BENCHMARK_VM
#endif

#include "debug_message.h"
#include "benchmark_container.h"
#include "exaudflib/exaudflib.h"
#include <iostream>
#include <string>
#include <functional>
#include <map>
#include <sstream>
#include <unistd.h>
#include <ext/stdio_filebuf.h>
#include <fstream>
#include <sys/types.h>
#include <sys/wait.h>
#include <thread>
#include <mutex>
#include <type_traits>
#include <string>

using namespace SWIGVMContainers;
using namespace std;

#define DECLARE_TIME(var) clock_t  time_counter_start_##var; clock_t time_counter_stop_##var
#define START_TIME(var) time_counter_start_##var=clock()
#define STOP_TIME(var)  time_counter_stop_##var=clock()
#define GET_TIME_SEC(var)  (double) (time_counter_stop_##var-time_counter_start_##var)/CLOCKS_PER_SEC


BenchmarkVM::BenchmarkVM(bool checkOnly)
    : meta(), inp(), outp(&inp)

{
    if (meta.inputType()  != MULTIPLE
            || meta.outputType() != MULTIPLE)
    {
        throw SWIGVM::exception("BENCHMARK language container only support SET-EMITS UDFs");
    }
}

void BenchmarkVM::shutdown()
{
}

bool BenchmarkVM::run()
{
    DBG_FUNC_BEGIN(cerr);
    DECLARE_TIME(fetch);
    //DECLARE_TIME(emit);
    int count = 0;
    int iteration = 0;
    cerr << "Input Columns:" << endl;
    for (unsigned int col = 0; col<meta.inputColumnCount(); col++) {
        cerr << "Column " << col << ": " << meta.inputColumnName(col) << " " << meta.inputColumnTypeName(col) << endl;
    }
    try {
        try {
            cerr << "Begin fetch" << endl;
            
            START_TIME(fetch);
            bool hasNext = false;
            
            do {
                
                //cerr << "Begin iteration " << iteration << endl;
                iteration++;
                for (unsigned int col = 0; col<meta.inputColumnCount(); col++) {           
                    switch (meta.inputColumnType(col))
                    {
                        case DOUBLE:
                            {
                                auto v=inp.getDouble(col);
                                if(v==0.0){
                                    count++;
                                }
                            }
                            break;
                        case INT32:
                            {
                                auto v=inp.getInt32(col);
                                if(v==0){
                                    count++;
                                }
                            }
                            break;
                        case INT64:
                            {
                                auto v=inp.getInt64(col);
                                if(v==0){
                                    count++;
                                }
                            }
                            break;
                        case STRING:
                            {
                                auto v=new string(inp.getString(col));
                                if(v->empty()){
                                    count++;
                                }
                            }
                            break;                                                
                        default:
                            break;
                    }
                }
                hasNext = inp.next();
            } while (hasNext);
            STOP_TIME(fetch);
            cerr << "End fetch" << endl;
        } catch (std::exception& err) {
            lock_guard<mutex> lock(exception_msg_mtx);
            exception_msg = err.what();
            cerr << "Exception BenchmarkVM::run " << exception_msg << endl;
        }

        try {
            cerr << "Begin emit" << endl;
            {
                double fetch_time=GET_TIME_SEC(fetch);
                string str1 = "fetch_time: " + std::to_string(fetch_time);
                outp.setString(0,str1.c_str(),strlen(str1.c_str()));
                outp.next();
            }
            {
                string str1 = "count: " + std::to_string(count);
                outp.setString(0,str1.c_str(),strlen(str1.c_str()));
                outp.next();
            }
            {
                string str1 = "iteration: " + std::to_string(iteration);
                outp.setString(0,str1.c_str(),strlen(str1.c_str()));
                outp.next();
            }
            outp.flush();
            cerr << "End emit" << endl;
        } catch (std::exception& err) {
            lock_guard<mutex> lock(exception_msg_mtx);
            exception_msg = err.what();
            cerr << "Exception BenchmarkVM::run " << exception_msg << endl;
        }
        
        if (exception_msg.size() > 0) {
            throw SWIGVM::exception(exception_msg.c_str());
        }

    } catch (std::exception& ex) {
        lock_guard<mutex> lock(exception_msg_mtx);
        exception_msg = ex.what();
        cerr << "Exception BenchmarkVM::run " << exception_msg << endl;
    }
    DBG_FUNC_END(cerr);
    return true;  // done
}

const char* BenchmarkVM::singleCall(single_call_function_id_e fn, const ExecutionGraph::ScriptDTO& args)
{
    throw SWIGVM::exception("singleCall not supported for the STREAMING language container");
}
