MAIN=thesis
DRAFT=draft

TEX=$(wildcard *.tex)
BIB=$(wildcard *.bib)
STY=$(wildcard *.sty)

.SUFFIXES: .tex

all: $(MAIN).pdf
draft: $(DRAFT).pdf

thesis.bib.orig: thesis.bib
	sed -i ".orig" 's/^title = {\([^{}]*\)}/title = {{\1}}/' $<
	sed -i ".orig" 's/^title = {LLVM\(.*\)}/title = {{LLVM\1}}/' $<

$(MAIN).pdf: $(TEX) $(BIB) $(STY) thesis.bib.orig
	xelatex $(MAIN)
	bibtex $(MAIN)
	xelatex $(MAIN)
	xelatex $(MAIN)
	#dvips -t a4paper -f < $(MAIN).dvi > $(MAIN).ps
	#ps2pdf $(MAIN).ps $@

$(DRAFT).pdf: $(DRAFT).tex $(TEX) $(BIB) $(STY) fig/*
	latex $(DRAFT)
	bibtex $(DRAFT)
	latex $(DRAFT)
	latex $(DRAFT)
	dvips -t a4paper -f < $(DRAFT).dvi > $(DRAFT).ps
	ps2pdf $(DRAFT).ps $@

clean:
	rm -f *.log *.aux *.dvi *.lof *.lot *.toc *.bbl *.blg *.pdf *.ps *.orig *.out
