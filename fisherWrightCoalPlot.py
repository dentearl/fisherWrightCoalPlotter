#!/usr/bin/env python
"""
"""
from optparse import OptionParser
import random
import sys

def initOptions(parser):
   """initOptions()
   """
   parser.add_option('-n', '--popsize',dest='n', action="store", default=20,
                     type ='int', help='Number of alleles to simulate.')
   parser.add_option('-v', '--verbose',dest='verbose', action="store_true", default=False,
                     help='Verbose output.')
   parser.add_option('-k', '--track',dest='k', action="store", default=5,
                     type ='int', help='Number of alleles to track.')
   parser.add_option('-g', '--maxGens',dest='maxGens', action="store", default=50,
                     type ='int', help='Maximum number of generations to go back.')


def checkOptions(options):
   """checkOptions() 
   """
   if options.k > options.n:
      sys.stderr.write('Error, k > n. Choose a value of k <= n.\n')
      sys.exit(2)
   
class Node:
   def __init__(self):
      self.parent=None
      self.name=''
      self.children=[]
      self.origAllele=None

class Generation:
   def __init__(self):
      self.name=''
      self.members=[]

def initGeneration(g, n, id, k=0, start=False):
   track=0
   tracked={}
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
            track+=1
      
def genPrint(g):
   for m in g.members:
      print m.name + ' nee ['+str(m.origAllele)+']'

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
   history.reverse()
   n = 0
   for g in history:
      print 'generation %d' %n
      n+=1
      for m in g.members:
          sys.stdout.write('%s gives rise to ' %( m.name ))
          for c in m.children:
             sys.stdout.write('%s ' %( c.name ))
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
      sys.stdout.write( '{rank=same; ')
      for m in g.members:
         sys.stdout.write('%s ' %(m.name))
      sys.stdout.write('};\n')
   for g in history:
      for m in g.members:
         if m.origAllele in ogAlleles:
            print '%s [fillcolor=gray, color=gray, style=filled, dir=none];' % ( m.name )
         else:
            print '%s [color=Gray60, dir=none];' % ( m.name )
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

def main():
   parser=OptionParser()
   initOptions(parser)
   (options, args) = parser.parse_args()
   checkOptions(options)
   activeAlleles = options.n
   currentGen = 1
   popHistory=[]
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
#      sys.stderr.write('gen: %d, activeAlleles: %d\n' %(currentGen, activeAlleles))
      uniqueID += options.n
      popHistory.append(gNext)
      gLast = gNext
      currentGen += 1
   popHistory.reverse()
   dotPrint(popHistory, ogAlleles)
   if options.verbose:
      sys.stderr.write('Number of gens: %d\n' % (currentGen - 1))
   
if __name__ == "__main__":
    main()
