#LLVM_HOME = /home/modcarl/llvm-2.8
#LLVM_HOME = /home/modcarl/clang-2.6/llvm+clang-2.6-i686-linux
#LLVM_HOME = /home/modcarl/clang-2.6/llvm-2.7/clang+llvm-2.7-i686-linux
LLVMHOME = /home/modcarl/llvm-124522
LLVMCONFIG = $(LLVMHOME)/bin/llvm-config
CXXFLAGS = -g -fno-rtti \
		 `$(LLVMCONFIG) --cxxflags`

LDFLAGS= `$(LLVMCONFIG) --ldflags`
#LIBS= -lclangBasic -lclangLex -lclangDriver -lclangFrontend -lclangParse \
#		-lclangAST -lclangSema -lclangAnalysis
LIBS=  -lclangDriver -lclangAnalysis -lclangFrontend\
		-lclangIndex -lclangSema -lclangAST -lclangParse -lclangLex \
		-lclangBasic 
#	-lclangFrontend -lclangSema -lclangAST -lclangParse -lclangLex \
#	-lclangBasic
#	Driver, Frontend, Analysis,
#	Index, Sema, AST, Parse, Lex, Basic

CPP = clang++
all:
	clang++ easy.cpp $(CXXFLAGS) \
	-o tut1 $(LIBS) `$(LLVMCONFIG) --ldflags --libs all`


