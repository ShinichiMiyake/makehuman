"""
===========================  ===============================================================
Project Name:                **MakeHuman**
Product Home Page:           http://www.makehuman.org/
Google Home Page:            http://code.google.com/p/makehuman/
Authors:                     Manuel Bastioni
Copyright(c):                MakeHuman Team 2001-2009
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://sites.google.com/site/makehumandocs/developers-guide
===========================  ===============================================================


This module contain the classes needed to load, save and generate (from guides)
makehuman hairs. 
"""

import random
import math
import simpleoctree


class Hair:
    """
    Hair is just a sequence of control points, to be rendered as a
    spline.
    """
    def __init__(self):
        self.controlPoints = []

class HairGuide(Hair):
   """
   Hair guide is a special hair type. It's used as a parent hair to
   generate an hair set (tuft). On the contrary of the normal hair,
   hairguide has a name.
   """
   def __init__(self,name):
       Hair.__init__(self)
       self.name = name         

class HairSet:
    """
    Hairset is basically a set of hair object. Usually they are randomly
    generated upon a hair guide.
    """
    def __init__(self,name):
        self.name = name
        self.hairs = []        

class Hairgenerator:
    """
    Hair genrator make a series of hair sets, one for each hairguide.
    The sum of all hair sets (think of it as tufts) is called hairstyle.
    """

    def __init__(self, humanMesh):

        self.hairStyle = []
        self.numberOfHairs = 90
        self.percOfRebels = 1.0
        self.clumptype = 1.0
        self.tuftSize = 0.150
        self.randomFact = 0.0
        self.hairDiameter = 0.006
        self.tipColor = [0.518,0.325,0.125]
        self.rootColor = [0.109, 0.037, 0.007]
        self.guides = []
        self.version = "1.0 alpha 2"
        self.tags = []
        self.octree = simpleoctree.SimpleOctree(humanMesh.verts)

    def addHairGuide(self,curve, curveName):
        g = HairGuide(curveName)
        g.name = curveName
        for p in curve:
            g.controlPoints.append([p[0],p[1],p[2]])
        self.guides.append(g)

    def generateHairStyle(self):
        for guide in self.guides:            
            self.generateHairSets(guide)

    def generateHairSets(self,guide):
        hSet = HairSet(guide.name)
        p =int(100/self.percOfRebels)
        nVerts = len(guide.controlPoints)
        rebelHair = range(0,nVerts,p)

        for n in range (self.numberOfHairs):
            h = Hair()
            vertsListToModify = []
            for c in guide.controlPoints:
                vertsListToModify.append([c[0],c[1],c[2]])

            delta1= self.tuftSize*random.uniform(-1.0,1.0)
            delta2= self.tuftSize*random.uniform(-1.0,1.0)
            delta3= self.tuftSize*random.uniform(-1.0,1.0)

            rebelVal = random.uniform(0,self.randomFact)
            for i in range(nVerts):
                vert = vertsListToModify[i]
                #Position is an int to indicate the position along the hair
                #because  we assume all verts have a incremental index,
                #from the root of the hair to the tip.
                index = float(i)/nVerts
                tipMagnet = 1.0-index+(index*self.clumptype)
                if n in rebelHair:
                    h.controlPoints.append([vert[0]+delta1+rebelVal,\
                                                vert[1]+delta2+rebelVal,\
                                                -vert[2]+delta3+rebelVal])
                else:
                    h.controlPoints.append([vert[0]+delta1*tipMagnet,\
                                                vert[1]+delta2*tipMagnet,\
                                                -vert[2]+delta3*tipMagnet])
            hSet.hairs.append(h)
        self.hairStyle.append(hSet)


    def saveHairs(self,path):
        """
        Save a file containing the info needed to build the hairstyle,
        strating from the hair guides and using some parameters.
        """
        try:
            fileDescriptor = open(path, "w")
        except:
            print "Impossible to save %s"%(path)
            return

        fileDescriptor.write("written by makehair 1.0\n")
        fileDescriptor.write("version %s\n"%(self.version))
        fileDescriptor.write("tags ")
        for tag in self.tags:
            fileDescriptor.write("%s "%(tag))
        fileDescriptor.write("\n")
        fileDescriptor.write("numberofhairs %i\n"%(self.numberOfHairs))
        fileDescriptor.write("percofrebels %f\n"%(self.percOfRebels))
        fileDescriptor.write("clumptype %f\n"%(self.clumptype))
        fileDescriptor.write("tuftsize %f\n"%(self.tuftSize))
        fileDescriptor.write("randomfact %f\n"%(self.randomFact))
        fileDescriptor.write("hairdiameter %f\n"%(self.hairDiameter))
        fileDescriptor.write("tipcolor %f %f %f\n"%(self.tipColor[0],self.tipColor[1],self.tipColor[2]))
        fileDescriptor.write("rootcolor %f %f %f\n"%(self.rootColor[0],self.rootColor[1],self.rootColor[2]))

        for guide in self.guides:
            fileDescriptor.write("%s "%(guide.name))
            for cP in guide.controlPoints:
                fileDescriptor.write("%f %f %f "%(cP[0],cP[1],cP[2]))
            fileDescriptor.write("\n")
        fileDescriptor.close()
    
    def extractSubList(self,listToSplit,sublistLength):        
        listOfLists = []
        for i in xrange(0, len(listToSplit), sublistLength):
            listOfLists.append(listToSplit[i: i+sublistLength])
        return listOfLists


    
    def loadHairs(self, path):        
        try:
            fileDescriptor = open(path)
        except:
            print "Impossible to load %s"%(path)
            return
            
        self.guides = []
        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == "written":
                pass
            elif datalist[0] == "version":
                pass
            elif datalist[0] == "tags":
                pass
            elif datalist[0] == "numberofhairs":
                self.numberOfHairs = int(datalist[1])
            elif datalist[0] == "percofrebels":
                self.percOfRebels = float(datalist[1])
            elif datalist[0] == "clumptype":
                self.clumpyype = float(datalist[1])
            elif datalist[0] == "tuftsize":
                self.tuftSize = float(datalist[1])
            elif datalist[0] == "randomfact":
                self.randomFact = float(datalist[1])
            elif datalist[0] == "hairdiameter":
                self.hairDiameter = float(datalist[1])
            elif datalist[0] == "tipcolor":
                self.tipColor[0] = float(datalist[1])
                self.tipColor[1] = float(datalist[2])
                self.tipColor[2] = float(datalist[3])
            elif datalist[0] == "rootcolor":
                self.rootColor[0] = float(datalist[1])
                self.rootColor[1] = float(datalist[2])
                self.rootColor[2] = float(datalist[3])
            else: 
                controlPointsCoo = datalist[1:]
                for i in range(len(controlPointsCoo)):
                    controlPointsCoo[i] = float(controlPointsCoo[i])
                guidePoints = self.extractSubList(controlPointsCoo,3)
                self.addHairGuide(guidePoints, datalist[0])
        fileDescriptor.close()
                
                
                
            
                
            
        


