LLVM_HOME = /home/modcarl/llvm-124522
CPP = g++
all:
	$(CPP) -I$(LLVM_HOME)/include/clang/ \
  	`$(LLVM_HOME)/bin/llvm-config --cxxflags` \
  	-fno-rtti -c tut01_pp.cpp
	$(CPP) `$(LLVM_HOME)/bin/llvm-config --ldflags` \
	  -lLLVMSupport -lLLVMSystem -lLLVMBitReader -lLLVMBitWriter \
	  -lclangBasic -lclangLex -lclangDriver \
	  -o tut01 tut01_pp.o
test:
	$(CPP) -I$(LLVM_HOME)/include/clang/ \
  	`$(LLVM_HOME)/bin/llvm-config --cxxflags` \
  	-fno-rtti -c xx.cpp
	$(CPP) `$(LLVM_HOME)/bin/llvm-config --ldflags` \
	  -lLLVMSupport -lLLVMSystem -lLLVMBitReader -lLLVMBitWriter \
	  -lclangBasic -lclangLex -lclangDriver \
	  -o tut01 xx.o

test2:
	$(CPP) -I$(LLVM_HOME)/include/clang/ \
  	`$(LLVM_HOME)/bin/llvm-config --cxxflags` \
  	-fno-rtti  sample.cpp
	$(CPP) `$(LLVM_HOME)/bin/llvm-config --ldflags` \
	  -lLLVMSupport  -lLLVMBitReader -lLLVMBitWriter \
	  -lclangBasic -lclangLex -lclangDriver \
	  -o tut01 sample.o
test3:
	$(CPP) -I$(LLVM_HOME)/include/clang/ \
  	`$(LLVM_HOME)/bin/llvm-config --cxxflags` \
  	-fno-rtti -c xx.cpp
	$(CPP) `$(LLVM_HOME)/bin/llvm-config --ldflags` \
	  -lLLVMSupport -lLLVMSystem -lLLVMBitReader -lLLVMBitWriter \
	  -lclangBasic -lclangLex -lclangDriver \
	  -o tut01 xx.o
