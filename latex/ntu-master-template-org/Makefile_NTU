MAIN=thesis

.SUFFIXES: .tex

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex ntu.sty
	pdflatex $(MAIN)
	bibtex $(MAIN)
	pdflatex $(MAIN)
	pdflatex $(MAIN)

.tex: 
	pdflatex $*
	pdflatex $*

clean:
	rm -f *.log *.aux *.dvi *.lof *.lot *.toc *.bbl *.blg

clean-pdf: 
	rm -f *.pdf

clean-all: clean clean-pdf
