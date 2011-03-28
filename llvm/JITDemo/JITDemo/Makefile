CXXFLAGS += -W -Wall -O3 `llvm-config --cxxflags`
LDFLAGS += `llvm-config --ldflags --libs`

all: out/JITDemo test

test: tests/data.c
	clang $< -emit-llvm -c -o data.bc
	
out/%: src/%.cpp Makefile
	mkdir -p out
	clang++ $< -g -o $@ $(CXXFLAGS) $(LDFLAGS)

clean:
	rm -f out/* tests/*.bc
