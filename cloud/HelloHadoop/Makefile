JarFile="sample-0.1.jar"
MainFunc="Sample.WordCount"
LocalOutDir="/tmp/output"

all:help
jar:
	jar -cvf ${JarFile} -C bin/ .

run:
	hadoop jar ${JarFile} ${MainFunc} input output

clean:
	hadoop fs -rmr output

output:
	rm -rf ${LocalOutDir}
	hadoop fs -get output ${LocalOutDir}
	vi ${LocalOutDir}/part-r-00000  

help:
	  @echo "Usage:"
	  @echo " make jar     - Build Jar File."
	  @echo " make clean   - Clean up Output directory on HDFS."
	  @echo " make run     - Run your MapReduce code on Hadoop."
	  @echo " make output  - Download and show output file"
	  @echo " make help    - Show Makefile options."
	  @echo " "
	  @echo "Example:"
	  @echo " make jar; make run; make output; make clean"
