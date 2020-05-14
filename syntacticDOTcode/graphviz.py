#!/usr/bin/python
# -*- coding: utf-8 -*-

class GraphViz():
  def __init__(self, children, category):
      self.children = children
      self.category  = category
  
  # function that appends code recursively  
  def appendCode(self, idNumber):
    # first append current node code
    self.id = idNumber
    DOTcode = str(self.id)+ " [label = \"" + self.category +\
                 "\", shape=\"polygon\", sides=\"4\"]\n"
    
    for child in self.children:
      # create a link to each one of my children
      idNumber += 1
      DOTcode  += str(self.id) + " -> " + str(idNumber) + "\n"
      
      try:
        # append my non terminal child code to my own code
        (temp, idNumber) = child.appendCode(idNumber)
        DOTcode += temp
      except:
        # if you are here, its because you are a terminal child
        # append your code manually
        DOTcode += str(idNumber) + " [label = \"" + str(child) +\
                      "\", color =\"#f6d6ed\", style=\"filled\"]\n"
    
    # return code I have appended so far, and last created id
    # so my node brothers are aware of the correct id they should continue from 
    return (DOTcode, idNumber)
  
  def generateDOTcode(self):
    (DOTcode, i) = self.appendCode(0)
    return "digraph G {\n" + DOTcode + "}"