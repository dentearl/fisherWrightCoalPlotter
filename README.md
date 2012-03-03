# fisherWrightCoalPlotter
(c) The Author

## Author
[Dent Earl](https://github.com/dentearl/)

## Dependencies
* [graphviz](http://www.graphviz.org/) for the <code>dot</code> program.

## Description
Use this script to create nifty looking figures for your slides and papers that show Fisher-Wright model [Coalescent](http://en.wikipedia.org/wiki/Coalescent_theory) event plots. Amaze your friends!

## Usage
    [d@d fisherWrightCoalPlot]$ ./fisherWrightCoalPlotter.py --help
    Usage: fisherWrightCoalPlotter.py [options]
    
    fisherWrightCoalPlotter.py can be used to generate Fisher-Wright process Coalescent
    event plots. Fun for the whole family!
    
    Options:
      -h, --help            show this help message and exit
      -n N, --popSize=N     Number of alleles to simulate. default=20
      -k K, --track=K       Number of alleles to track. default=5
      -g MAXGENS, --maxGens=MAXGENS
                            Maximum number of generations to go back. default=50
      -v, --verbose         Verbose output. default=False

## Examples
Note that the example images shown here are converted from vectors (.ps / .pdf) into .png so that they can be displayed on the web.
    ./fisherWrightCoalPlotter.py --popSize 10 > example1.dot && \
        dot -Tps2 example1.dot > example1.ps && \
        ps2pdf example1.ps example1.pdf
![Example image](https://github.com/dentearl/fisherWrightCoalPlotter/raw/master/exampleImages/example01.png)

    ./fisherWrightCoalPlotter.py --popSize 20 --track 10 > example2.dot && \
        dot -Tps2 example2dot > example2.ps && \
        ps2pdf example2.ps example2.pdf
![Example image](https://github.com/dentearl/fisherWrightCoalPlotter/raw/master/examplesImages/example02.png)

    ./fisherWrightCoalPlotter.py --popSize 100 --track 10 --maxGens 100 > example3.dot && \
        dot -Tps2 example3.dot > example3.ps && \
        ps2pdf example3.ps example3.pdf
![Example image](https://github.com/dentearl/fisherWrightCoalPlotter/raw/master/examplesImages/example03.png)
