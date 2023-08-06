# pycflow2dot


## Summary

Draw call graphs for C source code using `dot` and `cflow`.
Typeset PDF with a page per source file and clickable cross-file
function references.

`cflow2dot -i hello_simple.c -f png` produces:

![](https://raw.githubusercontent.com/johnyf/binaries/master/pycflow2dot/hello_simple.png)

from [`hello_simple.c`](https://github.com/johnyf/pycflow2dot/blob/master/examples/simple/hello_simple.c).


## Description

Draw the call graph of C source code using
[cflow](http://en.wikipedia.org/wiki/GNU_cflow) and
[dot](http://www.graphviz.org/).
Output to [LaTeX](https://en.wikipedia.org/wiki/LaTeX),
[dot](https://en.wikipedia.org/wiki/DOT_(graph_description_language)),
[PDF](https://en.wikipedia.org/wiki/PDF),
[SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics),
[PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics),
and from dot to all formats supported
from it. The LaTeX output is obtained by including the SVG via
[Inkscape](http://inkscape.org/)'s LaTeX [export](
    http://tug.ctan.org/info/svg-inkscape/InkscapePDFLaTeX.pdf)
functionality.

Multi-file sources are converted to multiple SVG files, one for each source.
These contain links using the LaTeX package
[hyperref](http://ctan.org/pkg/hyperref), so that after compilation
one can click on the name of a function call and be taken to its definition,
even if that definition is in another page of the PDF, because the function
is defined in another source file than the one corresponding to the current
PDF page.

Note that if a file containing the definition is missing, then the hyperref link
is omitted, so that no dead links result after compiling with LaTeX.
This might be the case of for example the file with the definitions is
available, but is not passed to `pycflow2dot`, e.g., for the purpose of focusing
on a subset of the sources.

For now the LaTeX result has to be manually compiled, though this
extra step will be automated in the future. Multi-SVG export will still be
available, so that the results can be included in a larger document, e.g.,
a report.

`pycflow2dot` is a Python port of the Perl script `cflow2dot`.


## Installation

From the [Python Package Index (PyPI)](https://pypi.org) using the
package installer [`pip`](https://pip.pypa.io):

```shell
pip install pycflow2dot
```

You also need to install the following non-Python dependencies:

- [GNU cflow](http://en.wikipedia.org/wiki/GNU_cflow):
  - `apt install cflow` on Debian GNU/Linux
  - `port install cflow` with [MacPorts](http://www.macports.org/)
- [`dot`](http://www.graphviz.org/):
  - `apt install graphviz`
  - `port install graphviz`

Optionally, [`cpp`](http://en.wikipedia.org/wiki/C_preprocessor) too.


## License

`pycflow2dot` is licensed under the [GNU GPL v3](
    https://www.gnu.org/licenses/gpl-3.0.en.html).
