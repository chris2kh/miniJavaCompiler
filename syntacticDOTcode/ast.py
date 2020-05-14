#!/usr/bin/python
# -*- coding: utf-8 -*-

from graphviz import GraphViz


class Node(GraphViz): 
    def __init__(self, children, category):
      GraphViz.__init__(self, children, category)
    
    def myPrint(self, tab):
      print tab + "   "+ "|"
      print tab + "   "+ "+->"+ self.category
      for child in self.children:
        try:
          child.myPrint(tab+"   ")
        except:
          print tab +"   " + "   " + "|"
          print tab +"   " + "   " + "*->" + str(child)