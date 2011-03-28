CC = g++ 
CPPFLAGS = -m32 -I$(HADOOP_INSTALL)/c++/$(PLATFORM)/include
LocalOutDir = /tmp/output
max_temperature: max_temperature.cpp 
	$(CC) $(CPPFLAGS) $< -Wall -L$(HADOOP_INSTALL)/c++/$(PLATFORM)/lib -lhadooppipes \
	-lhadooputils -lpthread -g -O2 -o $@
put:
	hadoop fs -put max_temperature bin/max_temperature
	hadoop fs -put sample.txt sample.txt
run:
	hadoop pipes \
	-D hadoop.pipes.java.recordreader=true \
	-D hadoop.pipes.java.recordwriter=true \
	-input sample.txt \
	-output output2 \
	-program bin/max_temperature
	hadoop fs -get output2 $(LocalOutDir)
	hadoop fs -get output2 ./output2
clean:
	hadoop fs -rmr output2
	hadoop fs -rmr bin/max_temperature
	hadoop fs -rmr sample.txt
	rm -rf $(LocalOutDir)/output2
	rm -rf ./output2


