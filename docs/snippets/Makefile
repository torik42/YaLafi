
all: yalafi yalafi.shell
yalafi: $(patsubst %.tex,%.plain,$(wildcard *.tex))
yalafi.shell: $(patsubst %.tex,%.out,$(wildcard *.tex))

%-de.plain: %-de.tex
	python -m yalafi --lang de-DE $< > $@

%.plain: %.tex
	python -m yalafi --lang en-GB $< > $@

%-de.out: %-de.tex
	python -m yalafi.shell --language de-DE --server my $< > $@

%.out: %.tex
	python -m yalafi.shell --language en-GB --server my $< > $@
