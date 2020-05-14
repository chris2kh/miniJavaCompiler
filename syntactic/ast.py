#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node: 
    def __init__(self, children, category):
      self.children = children
      self.category = category
    
    def myPrint(self, tab):
      print tab + "   "+ "|"
      print tab + "   "+ "+->"+ self.category
      for child in self.children:
        try:
          child.myPrint(tab + "   ")
        except:
          print tab + "   " + "   " + "|"
          print tab + "   " + "   " + "*->" + str(child)