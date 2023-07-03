SHELL := /bin/zsh

all: latex logo favicon

resolutions := 16 32 48 64 96 128 256 512 1024 2048
apple-resolutions := 57 60 72 76 114 120 144 152 180

latex: ../out/pdf/logo-dark.pdf ../out/pdf/logo-light.pdf ../out/pdf/logo-text-dark.pdf ../out/pdf/favicon.pdf

logo: ../out/png/logo-dark.png ../out/png/logo-light.png ../out/png/logo-text-dark.png

../out/png/%.png: ../out/pdf/%.pdf
	convert -resize 600x1000 -density 10000 -background transparent -gravity center $< $@

favicon: $(foreach res, $(resolutions), ../out/favicon/favicon-$(res)x$(res).png) $(foreach res, $(apple-resolutions), ../out/favicon/apple-touch-icon-$(res)x$(res).png)

../out/favicon/favicon-%.png: ../out/pdf/favicon.pdf
	convert -resize $* -extent $* -density 10000 -background transparent -gravity center $< $@

../out/favicon/apple-touch-icon-%.png: ../out/pdf/favicon.pdf
	convert -resize $* -extent $* -density 10000 -background transparent -gravity center $< $@

../out/pdf/%.pdf: %.tex
	pdflatex $<
	mv $(<:.tex=.pdf) ../out/pdf/
	rm $*.aux $*.log