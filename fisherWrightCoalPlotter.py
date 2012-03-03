#!/usr/bin/env python
""" 
fisherWrightCoalPlotter
May 2010
dent earl, dearl (a) soe ucsc edu

Simple script to produce graphviz (http://www.graphviz.org/) 
input files (dot) that depict Fisher-Wright coalescent 
(http://en.wikipedia.org/wiki/Coalescent_theory) events.
"""
########################################
# LICENSE
#
# Copyright (C) 2007-2012 by
# Dent Earl (dearl (a) soe ucsc edu, dentearl (a) gmail com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
########################################
from optparse import OptionParser
import random
import sys

class Node:
   def __init__(self):
      self.parent = None
      self.name = ''
      self.children = []
      self.origAllele = None

class Generation:
   def __init__(self):
      self.name = ''
      self.members = []

def initOptions(parser):
   parser.add_option('-n', '--popSize', dest='n', action="store", default=20,
                     type ='int', help='Number of alleles to simulate. default=%default')
   parser.add_option('-k', '--track', dest='k', action="store", default=5,
                     type ='int', help='Number of alleles to track. default=%default')
   parser.add_option('-g', '--maxGens', dest='maxGens', action="store", default=50,
                     type ='int', help='Maximum number of generations to go back. default=%default')
   parser.add_option('-v', '--verbose', dest='verbose', action="store_true", default=False,
                     help='Verbose output. default=%default')

def checkOptions(options, parser):
   if options.n < options.k:
      parser.error('Error, --popSize %d < --track %d' % (options.n, options.k))
   for s, v in [('--popSize', options.n), ('--track', options.k), ('--maxGens', options.maxGens)]:
      if v < 1:
         parser.error('Error, %s < 1. Choose a value of %s >= 1.' % (s, s))

def initGeneration(g, n, id, k=0, start=False):
   track = 0
   tracked = {}
   while len(g.members) < n:
      ind = Node()
      ind.name = str(id)
      g.members.append(ind)
      id += 1
   if start:
      while track < k:
         ind = random.choice(g.members)
         if ind not in tracked:
            tracked[ind] = 1
            ind.origAllele = ind.name
            track += 1
      
def genPrint(g):
   """ debugging function.
   """
   for m in g.members:
      print '%s nee [%s]' % (m.name, m.origAllele)

def coalesce(g0, g1):
   originalAlleles = {}
   for i in g0.members:
      p = random.choice(g1.members)
      i.parent = p.name
      if i.origAllele != None:
         p.origAllele = i.origAllele
         originalAlleles[p] = 1
      p.children.append(i)
   return len(originalAlleles)

def printHistory(history):
   """ debugging function.
   """
   history.reverse()
   n = 0
   for g in history:
      print 'generation %d' %n
      n+=1
      for m in g.members:
          sys.stdout.write('%s gives rise to ' %(m.name))
          for c in m.children:
             sys.stdout.write('%s ' %(c.name))
          sys.stdout.write('\n')

def dotPrint(history, ogAlleles):
   n = 0
   print """graph G {
\tnode [shape=circle, label=""];
\tnodesep="0.15";
\tsize="6.8,10";
\tranksep="1.0 equally";
\tratio="compress";
\tpackMode="node";
\tedge [color=Gray70];
"""
   for g in history:
      sys.stdout.write('\t{rank=same; ')
      for m in g.members:
         sys.stdout.write('%s ' %(m.name))
      sys.stdout.write('};\n')
   for g in history:
      for m in g.members:
         if m.origAllele in ogAlleles:
            print '\t%s [fillcolor=gray, color=gray, style=filled, dir=none];' % (m.name)
         else:
            print '\t%s [color=Gray60, dir=none];' % (m.name)
         if len(m.children) > 0:
            for c in m.children:
               sys.stdout.write('\t%s -- %s;\n' %(m.name, c.name))
   print '}'

def initOGAlleles(n):
   d = {}
   for i in range(0, n):
      d[ str(i) ] = 1
   return d

def propogateOrigDown(history):
   for g in history:
      for m in g.members:
         if m.origAllele != None:
            for c in m.children:
               c.origAllele = m.origAllele

def generateHistory(options):
   activeAlleles = options.n
   currentGen = 1
   popHistory = []
   g0 = Generation()
   uniqueID = 0
   initGeneration(g0, options.n, uniqueID, k=options.k,  start=True)
   ogAlleles = initOGAlleles(options.n)
   uniqueID += options.n
   popHistory.append(g0)
   gLast = g0
   while (activeAlleles > 1) and (currentGen < options.maxGens+1):
      gNext = Generation()
      initGeneration(gNext, options.n, uniqueID)
      activeAlleles = coalesce(gLast, gNext)
      uniqueID += options.n
      popHistory.append(gNext)
      gLast = gNext
      currentGen += 1
   popHistory.reverse()
   return popHistory, ogAlleles, currentGen

def main():
   usage = ('usage: %prog [options] > output.dot\n\n'
            '%prog can be used to generate Fisher-Wright process Coalescent\n'
            'event plots. Fun for the whole family! Output is in .dot format\n'
            'for use with graphviz\'s (http://www.graphviz.org/) dot program.')
   parser = OptionParser(usage=usage)
   initOptions(parser)
   (options, args) = parser.parse_args()
   checkOptions(options, parser)
   
   popHistory, ogAlleles, currentGen = generateHistory(options)
   dotPrint(popHistory, ogAlleles)
   if options.verbose:
      sys.stderr.write('Number of generations: %d\n' % (currentGen - 1))
   
if __name__ == "__main__":
    main()
