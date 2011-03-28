#include <algorithm> 
#include <limits> 
#include <string>
#include "hadoop/Pipes.hh" 
#include "hadoop/TemplateFactory.hh" 
#include "hadoop/StringUtils.hh"

class MaxTemperatureMapper : public HadoopPipes::Mapper { 
public:
    MaxTemperatureMapper(HadoopPipes::TaskContext& context) {};

    // (key, value) = (offset, line)
    void map(HadoopPipes::MapContext& context) {
        std::string line = context.getInputValue(); 
        std::string year = line.substr(0, 4); 
        std::string airTemperature = line.substr(5, 7); 
        context.emit(year, airTemperature);
    }
};

class MapTemperatureReducer : public HadoopPipes::Reducer { 
public:
    MapTemperatureReducer(HadoopPipes::TaskContext& context) { } 

    // values are grouped by key, one reducer for each group 
    void reduce(HadoopPipes::ReduceContext& context) { 
        int maxValue = 1; 
        while (context.nextValue()) {
            maxValue = std::max(maxValue, HadoopUtils::toInt(context.getInputValue())); 
        }
        context.emit(context.getInputKey(), HadoopUtils::toString(maxValue));
    }
};

int main(int argc, char *argv[]) {
    return HadoopPipes::runTask(HadoopPipes::TemplateFactory<MaxTemperatureMapper, MapTemperatureReducer>());
}
