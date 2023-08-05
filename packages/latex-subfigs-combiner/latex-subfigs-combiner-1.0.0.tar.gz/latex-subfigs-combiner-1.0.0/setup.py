# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latex_subfigs_combiner']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0']

entry_points = \
{'console_scripts': ['combine-subfigs = '
                     'latex_subfigs_combiner.combine_subfigures:main']}

setup_kwargs = {
    'name': 'latex-subfigs-combiner',
    'version': '1.0.0',
    'description': 'Python script for combining LaTeX figures composed of subfigures.',
    'long_description': '# LaTeX Subfigs Combiner\n\nPython script for combining LaTeX figures composed of subfigures\n\n---\n\n## What\n\nThis package provides a simple Python script for combining LaTeX figures composed of subfigures into single PDF files, i.e. one PDF per composite figure.\n\n## Why\n\nIf you have ever tried to publish on scientific journals, you have probably encountered at least _one_ journal that either does not accept LaTeX [`subfigures`](https://www.ctan.org/pkg/subcaption) or will combine your composite figures during production with a very high chance of making a mess (both scenarios are completely unreasonable, but yet they happen sometimes).\nOf course, you really like those shiny composite LaTeX figures and do not want to waste time painstakingly stitching them together by hand (e.g. using Inkscape).\nThis Python script provides an hands-free automated solution to this problem.\n\n## How\n\nThe job is done by parsing the given TeX file, extracting the preamble, setting the page style to empty, extracting the `figure` environments that contain `subfigures`, compiling to a PDF via [`latexmk`](https://www.ctan.org/pkg/latexmk/), and then crop each figure to a separate PDF file using [`pdfcrop`](https://www.ctan.org/pkg/pdfcrop).\n\n---\n\n## Installation\n\nEasy peasy via `pip` or equivalent\n\n```bash\npip install latex-subfigs-combiner\n```\n\n## Usage\n\nIn a terminal, simply run `combine-subfigs` on your LaTeX main file\n\n```bash\ncombine-subfigs /path/to/my/awesome/paper.tex\n```\n\nThis will produce all the composite figures in a directory named `composite-figures` at the location you called the script from.\n\nBy default, the output figures will be named as `fig_1.pdf`, `fig_2.pdf`, etc.\nIf you want to change the output directory or the filename prefix `fig_` of the figures, you can use the optional arguments `--target_dir` and `--prefix`, respectively.\nExecute `combine-subfigs -h` for more details.\n\n---\n\n## Tips are welcomed! :love_you_gesture:\n\nIf you found this useful, feel free to offer me a beer :beer: via [PayPal](https://paypal.me/GiovanniBordiga/3 "Send tip via PayPal") or [send me a few sats](http://deadcat.epizy.com/ "Send tip via LN") :zap:.\n',
    'author': 'Giovanni Bordiga',
    'author_email': 'gio.61192@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GiovanniBordiga/latex-subfigs-combiner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
