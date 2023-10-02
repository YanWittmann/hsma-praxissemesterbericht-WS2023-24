# Makefile für praksem. Mit pdflatex, bevorzugt auf 
# Linux Rechnern und libreoffice installiert
PDFLATEX=pdflatex -interaction=nonstopmode
BIBTEX=bibtex
SOFFICE=soffice
ZIP=zip
RM=rm
MKDIR=mkdir

STYLES=hsmalogo.sty hsmalogosw.pdf blindtext.sty
DRAWINGS=ablauf.odg
INCLUDE_DRAWINGS=ablauf.pdf
IMAGES=
MAIN=praksem
TEXFILES=$(MAIN).tex preamble.tex vorspann.tex hyphenations.tex glossar.tex
BIB=praksem.bib
INCLUDE_BIB=$(MAIN).bbl # spaeter nochmal manuell
# INCLUDE_BIB=$(MAIN)1.bbl $(MAIN)2.bbl # spaeter nochmal manuell, getrennt
TOPACK= $(STYLES) $(BIB) $(DRAWINGS) $(IMAGES) $(TEXFILES) Makefile $(MAIN).pdf

$(MAIN): $(MAIN).pdf

# bewusst nicht erstes Ziel
all: bib $(MAIN).pdf LaTeXPraksem.zip

LaTeXPraksem.zip: $(TOPACK) 
	-$(RM) -rf LaTeXPraksem
	$(MKDIR) LaTeXPraksem
	cp $(TOPACK) LaTeXPraksem
	$(ZIP) -r LaTeXPraksem.zip LaTeXPraksem
	$(RM) -rf LaTeXPraksem

$(MAIN).pdf: $(TEXFILES) $(STYLES) $(INCLUDE_DRAWINGS) $(INCLUDE_BIB)

# für das convert braucht man ImageMagick
zeichnungjpg.jpg: zeichnung.pdf
	convert zeichnung.pdf zeichnungjpg.jpg
zeichnungpng.png: zeichnung.pdf
	convert zeichnung.pdf zeichnungpng.png


# das ist mit einem Literaturverzeichnis
bib: $(MAIN).bbl
	-$(BIBTEX) $(MAIN)
$(MAIN).bbl: $(MAIN).tex $(MAIN).bib
	-$(BIBTEX) $(MAIN)

# Das wäre mit geteilter Literatur und Online-Quellen
#bib: $(MAIN)1.bbl $(MAIN)2.bbl
# Bibliography geht nur manuell wegen bibtopic
# Nachteil: make erstellt bei jedem Durchlauf das PDF neu. 
# Vorteil: Es geht auch von Anfang an, für Leute (die Mehrheit),
#          die nicht schauen. 
#bib: $(MAIN)1.bbl $(MAIN)2.bbl
#$(MAIN)1.bbl: praksem.bib $(MAIN)1.aux
#	-$(BIBTEX) $(MAIN)1
#$(MAIN)2.bbl: online.bib $(MAIN)2.aux
#	-$(BIBTEX) $(MAIN)2

glos:
	makeglossaries $(MAIN)

# Das erste Mal TeXen wegen Bibliographie
# Das allererste Mal ist die Bibliographie noch nicht drin.
$(MAIN).aux: 
	$(PDFLATEX) $(MAIN).tex
# fuer getrennte Bibliography
$(MAIN)1.aux: 
	$(PDFLATEX) $(MAIN).tex
$(MAIN)2.aux: 
	$(PDFLATEX) $(MAIN).tex

.PHONY: clean bib glos

RERUN = "(There were undefined |Rerun to get (cross-references|the bars))"

.SUFFIXES: .odg .tex .pdf

.tex.pdf: bib
	$(PDFLATEX) $*.tex
    # nochmal wenn notwendig
	egrep $(RERUN) $*.log && ($(PDFLATEX) $*.tex) ; true
    # und nochmal wenn notwendig
	egrep $(RERUN) $*.log && ($(PDFLATEX) $*.tex) ; true

.odg.pdf:
	$(SOFFICE) --headless --convert-to pdf $*.odg

clean:
	-$(RM) $(MAIN).pdf *.lof *.log *.lot *.aux *.toc *.blg *.glg *.glo *.gls *.its
	-$(RM) $(INCLUDE_DRAWINGS) $(INCLUDE_BIB)

TOPUB=LaTeXPraksem.zip praksem.pdf
pub: $(TOPUB)
	chmod a+r $(TOPUB)
	scp -rp $(TOPUB) peter@www.pbma.de:/var/www/html/latex
