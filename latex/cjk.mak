all:
	latex cjk.tex
	dvips cjk.dvi
	ps2pdf cjk.ps
