call_graph:
	cflow2dot -i user.c lib.c -f pdf

build:
	gcc user.c lib.c

latex:
	cflow2dot --input-filenames user.c lib.c \
		--output-format svg --latex-svg \
		--multi-page --layout dot
	mkdir -p img
	cp cflow0.svg ./img/cflow0.svg
	cp cflow1.svg ./img/cflow1.svg
	xelatex --interaction=nonstopmode --shell-escape main.tex
	# second run to ensure hyperref links are correct
	xelatex --interaction=nonstopmode --shell-escape main.tex
