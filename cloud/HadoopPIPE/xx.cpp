#include <algorithm> 
#include <limits> 
#include <string>
#include "hadoop/Pipes.hh" 
#include "hadoop/TemplateFactory.hh" 
#include "hadoop/StringUtils.hh"
using namespace std;
using namespace HadoopUtils;

class MaxTemperatureMapper : public HadoopPipes::Mapper { 
public:
    MaxTemperatureMapper(HadoopPipes::TaskContext& context) {};
    void map(HadoopPipes::MapContext& context) {
        string line = context.getInputValue(); 
        string year = line.substr(0, 4); 
        string airTemperature = line.substr(5, 7); 
        context.emit(year, airTemperature);
    }
};

class MapTemperatureReducer : public HadoopPipes::Reducer { 
public:
    MapTemperatureReducer(HadoopPipes::TaskContext& context) { } 
    void reduce(HadoopPipes::ReduceContext& context) { 
        int maxValue = 1; 
        while (context.nextValue()) {
            maxValue = max(maxValue, toInt(context.getInputValue())); 
        }
        context.emit(context.getInputKey(), toString(maxValue));
    }
};

int main(int argc, char *argv[]) {
    return HadoopPipes::runTask(HadoopPipes::TemplateFactory<MaxTemperatureMapper, MapTemperatureReducer>());
}
