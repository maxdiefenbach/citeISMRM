

# Description

commandline tool to extract bibtex entries
for ISMRM abstracts from
<https://dev.ismrm.org>


# Usage

    python citeISMRM.py -y 2017 -n 850 # prints bibtex entry
                                       # from 2017 abstract #0850 to stdout
    
    python citeISMRM.py -y 2017 -n 850 -w abstract.bib
    # writes bibtex entry to file abstract.bib
    
    python citeISMRM.py -y 2017 -n 850 -a bibliography.bib
    # appends bibtex entry to file bibliography.bib


# License

MIT License

Copyright (c) 2018 Maximilian N. Diefenbach

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

