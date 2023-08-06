This example requires:

- [XeLaTeX](https://en.wikipedia.org/wiki/XeTeX): a LaTeX typesetting engine
- [`svglatex.sty`](https://github.com/johnyf/latex_packages/blob/master/svglatex.sty):
  a LaTeX package for including SVG files via SVGLaTeX
- [SVGLaTeX](https://github.com/johnyf/svglatex): a Python package for exporting
  SVG graphics to PDF for the graphics and LaTeX for the text.
- `pycflow2dot`

To create a PDF document with two pages invoke:

```shell
make latex
```

To create the files `cflow0.pdf` and `cflow1.pdf` invoke:

```shell
make call_graph
```

To build an executable from the files `user.c`, `lib.c`, `lib.h`,
assuming that [`gcc`](https://en.wikipedia.org/wiki/GNU_Compiler_Collection)
is installed:

```shell
make build
```
