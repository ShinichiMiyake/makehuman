#!/usr/bin/python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2010

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This module contain the classes needed to load, save and generate (from guides)
makehuman hairs.
"""

import random
import math
import simpleoctree
import aljabr
from collision import collision
from os import path

class Hairgenerator:

    """
    Hair generator make a series of hair sets, one for each hairguide.
    The sum of all hair sets (think of it as tufts) is called hairstyle.
    """

    def __init__(self):

        self.tipMagnet = 0.9
        self.fallingHair = False
        self.hairCoverage = 0.6
         
        self.numberOfHairsClump = 10
        self.numberOfHairsMultiStrand = 20

        self.randomFactClump = 0.5
        self.randomFactMultiStrand = 0.5
        self.randomPercentage = 0.5

        self.hairDiameterClump = 0.006
        self.hairDiameterMultiStrand = 0.006

        self.sizeClump = 0.20
        self.sizeMultiStrand = 0.200
        self.blendDistance = 0.8

        self.tipColor = [0.518, 0.325, 0.125]
        self.rootColor = [0.109, 0.037, 0.007]
        self.guides =[]
        self.version = '1.0 alpha 2'
        self.tags = []
        self.humanVerts = []
        self.path = None

        self.noGuides = 25
        self.gLength = 5.0
        self.noCPoints = 15
        self.gFactor = 1.5
        self.Delta=None #Delta of the very first controlpoint of the very first guide in our guide list! This will be used as a reference
        
    def generateHairStyle1(self):
        """
        Calling this function, for each guide in each guideGroup,
        a new hairtuft will be added to the hairstyle.
        """
     
        #for guideGroup in self.guideGroups: #taking tuples from list of tuples of curves
        hairStyle = []
        for guide in self.guides: #taking curves from a tuple of curves
            hairStyle.append(self.generateHairInterpolation1(guide)) #guide is a curve
        return hairStyle

    def getFromListbyName(self, list, name):
        """
        We should use a dictionary, but for a quick test this function is ok
        """

        for i in list:
            if i.name == name:
                return i
        return None

    def generateHairStyle2(self, Area=0.6, fallingHair=False, humanMesh=None, isCollision=False):
        """
        Calling this function, each guide is interpolated with all other guides
        to add a new strand of hairs to the hairstyle.

        Parameters
        ----------

        No parameters
        """

        # near = 0.08
        # far = 1.6
        hairStyle = []
        if humanMesh == None:
            isCollision = False
        
        if (fallingHair): guideGroups=self.groupFallingHair(Area)
        else: guideGroups = self.groupPeakyHair(Area)
        for guideGroup in guideGroups:
            if len(guideGroup) > 0:

                # Find the bounding box of the cloud of controlPoints[2]

                #print 'WORKING ON GROUP %s' % guideGroup
                guideOrder = {}
                xMin = 1000
                xMax = -1000
                yMin = 1000
                yMax = -1000
                zMin = 1000
                zMax = -1000
                for guide in guideGroup:
                    p = guide[2]
                    #print guide.name, p
                    if p[0] < xMin:
                        xMin = p[0]
                    if p[0] > xMax:
                        xMax = p[0]

                    if p[1] < yMin:
                        yMin = p[1]
                    if p[1] > yMax:
                        yMax = p[1]

                    if p[2] < zMin:
                        zMin = p[2]
                    if p[2] > zMax:
                        zMax = p[2]
                diffX = xMax - xMin
                diffY = yMax - yMin
                diffZ = zMax - zMin

                # print "DIFF",diffX,diffY,diffZ

                # Find the main dimension of bounding box

                if diffX > diffY and diffX > diffZ:
                    mainDirection = 0
                if diffY > diffX and diffY > diffZ:
                    mainDirection = 1
                if diffZ > diffX and diffZ > diffY:
                    mainDirection = 2

                print 'MaindDirection', mainDirection

                # Order the guides along the main dimension

                for guide1 in guideGroup:
                    p1 = guide1[2]
                    guideOrder[p1[mainDirection]] = guide1

                guideKeys = guideOrder.keys()
                guideKeys.sort()
                for i in range(len(guideKeys) - 1):
                    k1 = guideKeys[i]
                    k2 = guideKeys[i + 1]
                    guide1 = guideOrder[k1]
                    guide2 = guideOrder[k2]
                    #print 'INTERP. GUIDE', guide1.name, guide2.name
                    hairStyle.append(self.generateHairInterpolation2(guide1, guide2, humanMesh, isCollision))
        return hairStyle

    def generateHairInterpolation1(self, guide):
        hSet = [] #empty list of list of curves  #HairGroup(hairName).. one whole group of hairstrands
        nVerts = len(guide)
        interpFactor1 = 0
        incr = 1.0 / self.numberOfHairsClump

        for n in xrange(self.numberOfHairsClump):
            interpFactor1 += incr
            interpFactor2 = 0

            xRand = self.sizeClump * random.random()
            yRand = self.sizeClump * random.random()
            zRand = self.sizeClump * random.random()
            offsetVector = [xRand, yRand, zRand]

            for n2 in xrange(self.numberOfHairsClump):
                h = [] #an empty strand (curve) with nVerts controlpoints, we make this as a list of triples.. triples cannot be reassigned! but we need to assign only once anyway
                interpFactor2 += incr
                for i in range(nVerts):
                    if nVerts > 3:
                        clumpIndex = nVerts - 2
                    else:
                        clumpIndex = nVerts - 1

                    magnet = 1.0 - (i / float(clumpIndex)) * self.tipMagnet
                    if random.random() < self.randomPercentage:
                        xRand = (self.sizeClump * random.random()) * self.randomFactClump
                        yRand = (self.sizeClump * random.random()) * self.randomFactClump
                        zRand = (self.sizeClump * random.random()) * self.randomFactClump
                        randomVect = [xRand, yRand, zRand]
                    else:
                        randomVect = [0, 0, 0]

                    vert1 = guide[i]
                    h.append([vert1[0] + offsetVector[0] * magnet + randomVect[0], vert1[1] + offsetVector[1] * magnet + randomVect[1], vert1[2]
                                            + offsetVector[2] * magnet + randomVect[2]])
                hSet.append(h)
        #hairStyle.append(hSet) #list of (list of curves) clumps
        return hSet

    # humanMesh is a blender object.. the format can be changed later on if the necessity arises!
    # for the time being we have a blender object and gravity direction is [0,-1,0]

    def generateHairInterpolation2(self, guide1, guide2, humanMesh, isCollision, startIndex=9, gravity=True):
        if isCollision:
            octree = simpleoctree.SimpleOctree(humanMesh.getData().verts, 0.08)
        #hairName = 'strand%s-%s' % (guide1.name, guide2.name)
        hSet = [] #HairGroup(hairName)

        if len(guide1) >= len(guide2):
            longerGuide = guide1
            shorterGuide = guide2
        else:
            longerGuide = guide2
            shorterGuide = guide1

        nVerts = min([len(guide1), len(guide2)])
        interpFactor = 0
        vertsListToModify1 = []
        vertsListToModify2 = []

        for n in range(self.numberOfHairsMultiStrand):
            h = []
            interpFactor += 1.0 / self.numberOfHairsMultiStrand
            for i in range(len(longerGuide)):
                if random.random() < self.randomPercentage:
                    xRand = (self.sizeMultiStrand * random.random()) * self.randomFactMultiStrand
                    yRand = (self.sizeMultiStrand * random.random()) * self.randomFactMultiStrand
                    zRand = (self.sizeMultiStrand * random.random()) * self.randomFactMultiStrand
                    randomVect = [xRand, yRand, zRand]
                else:
                    randomVect = [0, 0, 0]

                if i == 0:
                    i2 = 0
                if i == len(longerGuide) - 1:
                    i2 = len(shorterGuide) - 1
                else:
                    i2 = int(round((i * len(shorterGuide)) / len(longerGuide)))

                vert1 = longerGuide[i]
                vert2 = shorterGuide[i2]

                # Slerp

                dotProd = aljabr.vdot(aljabr.vnorm(vert1), aljabr.vnorm(vert2))

                # Python is not perfect with numerical accuracy.. we need to do this for very small angle between guides
                # this occurs when we do collision detection

                if dotProd > 1:
                    angleBetweenGuides = 0.0
                else:
                    angleBetweenGuides = math.acos(aljabr.vdot(aljabr.vnorm(vert1), aljabr.vnorm(vert2)))
                denom = math.sin(angleBetweenGuides)
                if denom == 0.0:  # controlpoints of some guides coincide
                    vert1[0] = ((self.randomPercentage * self.sizeMultiStrand) * random.random()) * self.randomFactMultiStrand + vert1[0]
                    vert1[1] = ((self.randomPercentage * self.sizeMultiStrand) * random.random()) * self.randomFactMultiStrand + vert1[1]
                    vert1[2] = ((self.randomPercentage * self.sizeMultiStrand) * random.random()) * self.randomFactMultiStrand + vert1[2]
                    vert1 = aljabr.vadd(vert1, randomVect)
                    angleBetweenGuides = math.acos(aljabr.vdot(aljabr.vnorm(vert1), aljabr.vnorm(vert2)))
                    denom = math.sin(angleBetweenGuides)
                f1 = math.sin((1 - interpFactor) * angleBetweenGuides) / denom
                f2 = math.sin(interpFactor * angleBetweenGuides) / denom
                newVert = aljabr.vadd(aljabr.vmul(vert1, f1), aljabr.vmul(vert2, f2))

                # Uncomment the following line we use lerp instead slerp
                # newVert = aljabr.vadd(aljabr.vmul(vert1,(1-interpFactor)),aljabr.vmul(vert2,interpFactor))

                h.append((newVert[0] + randomVect[0], newVert[1] + randomVect[1], newVert[2] + randomVect[2]))
            if isCollision:
                print 'h is: ', h
                for j in (0, len(h)):
                    h[i][2] = -h[i][2]  # Renderman to Blender coordinates!
                collision(h, humanMesh, octree.minsize, startIndex, gravity)
                for j in (0, len(h)):
                    h[i][2] = -h[i][2]  # Blender to Renderman coordinates!
            hSet.append(h)
        return hSet

    def saveHairs(self, path):
        """
        Save a file containing the info needed to build the hairstyle,
        strating from the hair guides and using some parameters.
        """

        try:
            fileDescriptor = open(path, 'w')
        except:
            print 'Impossible to save %s' % path
            return

        fileDescriptor.write('written by makehair 1.0\n')
        fileDescriptor.write('version %s\n' % self.version)
        fileDescriptor.write('tags ')
        for tag in self.tags:
            fileDescriptor.write('%s ' % tag)
        fileDescriptor.write('\n')

        fileDescriptor.write('tipMagnet %f\n' % self.tipMagnet)
        fileDescriptor.write('numberOfHairsClump %i\n' % self.numberOfHairsClump)
        fileDescriptor.write('numberOfHairsMultiStrand %i\n' % self.numberOfHairsMultiStrand)
        fileDescriptor.write('randomFactClump %f\n' % self.randomFactClump)
        fileDescriptor.write('randomFactMultiStrand %f\n' % self.randomFactMultiStrand)
        fileDescriptor.write('randomPercentage %f\n' % self.randomPercentage)
        fileDescriptor.write('hairDiameterClump %f\n' % self.hairDiameterClump)
        fileDescriptor.write('hairDiameterMultiStrand %f\n' % self.hairDiameterMultiStrand)
        fileDescriptor.write('sizeClump %f\n' % self.sizeClump)
        fileDescriptor.write('sizeMultiStrand %f\n' % self.sizeMultiStrand)
        fileDescriptor.write('blendDistance %f\n' % self.blendDistance)

        fileDescriptor.write('tipcolor %f %f %f\n' % (self.tipColor[0], self.tipColor[1], self.tipColor[2]))
        fileDescriptor.write('rootcolor %f %f %f\n' % (self.rootColor[0], self.rootColor[1], self.rootColor[2]))

        for guideGroup in self.guideGroups:
            fileDescriptor.write('guideGroup %s\n' % guideGroup)
            for guide in guideGroup.guides:
                #fileDescriptor.write('guide %s ' % guide.name)

                # Write points coord

                for cP in guide.controlPoints:
                    fileDescriptor.write('%f %f %f ' % (cP[0], cP[1], cP[2]))
                fileDescriptor.write('\n')

        for guideGroup in self.guideGroups:
            print 'guidegroup', guideGroup
            for guide in self.guideGroups[guideGroup]:
                #fileDescriptor.write('delta %s ' % guide.name)

                # Write points nearest body verts

                for cP in guide:
                    distMin = 1000
                    for i in range(len(self.humanVerts)):  # later we optimize this using octree
                        v = self.humanVerts[i]
                        dist = aljabr.vdist(cP, v)
                        if dist < distMin:
                            distMin = dist
                            nearVert = v
                            nearVertIndex = i
                    delta = aljabr.vsub(cP, nearVert)
                    fileDescriptor.write('%i %f %f %f ' % (nearVertIndex, delta[0], delta[1], delta[2]))
                fileDescriptor.write('\n')
        fileDescriptor.close()

    def extractSubList(self, listToSplit, sublistLength):
        listOfLists = []
        for i in xrange(0, len(listToSplit), sublistLength):
            listOfLists.append(listToSplit[i:i + sublistLength])
        return listOfLists

    def loadHairs(self, name):
        try:
            name = path.splitext(name)[0]
            objFile = open(name + ".obj")
            fileDescriptor = open(name+".hair")
        except:
            print 'Unable to load .obj and .hair file of %s' % name
            return

        #self.resetHairs()
        self.path = name
        for data in fileDescriptor:
            datalist = data.split()
            if datalist[0] == 'written':
                pass
            elif datalist[0] == 'version':
                pass
            elif datalist[0] == 'tags':
                pass
            elif datalist[0] == 'tipMagnet':
                self.tipMagnet = float(datalist[1])
            elif datalist[0] == 'numberOfHairsClump':
                self.numberOfHairsClump = int(datalist[1])
            elif datalist[0] == 'numberOfHairsMultiStrand':
                self.numberOfHairsMultiStrand = int(datalist[1])
            elif datalist[0] == 'hairCoverage':
                self.hairCoverage = float(datalist[1])
            elif datalist[0] == 'fallingHair':
                self.fallingHair = bool(datalist[1])
            elif datalist[0] == 'randomFactClump':
                self.randomFactClump = float(datalist[1])
            elif datalist[0] == 'randomFactMultiStrand':
                self.randomFactMultiStrand = float(datalist[1])
            elif datalist[0] == 'randomPercentage':
                self.randomPercentage = float(datalist[1])
            elif datalist[0] == 'hairDiameterClump':
                self.hairDiameterClump = float(datalist[1])
            elif datalist[0] == 'hairDiameterMultiStrand':
                self.hairDiameterMultiStrand = float(datalist[1])
            elif datalist[0] == 'sizeClump':
                self.sizeClump = float(datalist[1])
            elif datalist[0] == 'sizeMultiStrand':
                self.sizeMultiStrand = float(datalist[1])
            elif datalist[0] == 'blendDistance':
                self.blendDistance = float(datalist[1])
            elif datalist[0] == 'tipcolor':

                self.tipColor[0] = float(datalist[1])
                self.tipColor[1] = float(datalist[2])
                self.tipColor[2] = float(datalist[3])
            elif datalist[0] == 'rootcolor':
                self.rootColor[0] = float(datalist[1])
                self.rootColor[1] = float(datalist[2])
                self.rootColor[2] = float(datalist[3])
                
        fileDescriptor.close()
        
        guidePoints=[]
        temp =[]
        #currentGroup=None
        #guideName = None
        self.guides = [] #set of curves
        #Forget the format of manuel make your own!
        reGroup = True
        for data in objFile:
            datalist = data.split()
            if datalist[0] == "v":
                for i in xrange(1,4):
                    datalist[i] = float(datalist[i])
                temp.append(datalist[1:])
            elif datalist[0] == "curv":
                #n = len(datalist[3:])
                #guidePoints=[None]*n
                for index in datalist[3:]:
                    guidePoints.append(temp[int(index)])
                temp=[]
            elif datalist[0] == "end":
                #used for collision:
                if guidePoints[0][1] < guidePoints[len(guidePoints)-1][1]: #is the first point lower than the last control point? 
                    guidePoints.reverse()
                self.guides.append(guidePoints); #apppend takes a deep copy
                #self.addHairGuide(guidePoints, guideName,currentGroup)
                #if currentGroup == None: reGroup = True;
                guidePoints=[]
                
        objFile.close()
        #if reGroup: self.populateGuideGroups(guides,0.6)

    #guides is of type list of curves
    #self.guideGroups is a list of tuples (as in pairs) of guides (curves)
    def groupFallingHair(self,Area):
        guideGroups =[]
        N= len(self.guides)
        #pair[n] contains the index of the guide that should be a guide-pair partner with the nth-guide
        pairs=[-1]*N
        #bunch of infinities
        areas = [-1e6]*N
        print "Number of strands: ", N
        for i in xrange(0,len(self.guides)):
            if (pairs[i]>-1) and pairs[pairs[i]]==i: continue 
            for j in xrange(i+1,len(self.guides)):                
                B = curvePairArea(self.guides[i],self.guides[j])
                if (B==0): continue #duplicate strands can occur!
                #taking greatest lower bound to Area
                #exerimental
                #n=math.fabs(len(self.guides[i])-len(self.guides[j]))
                if areas[j]<B and B<=Area:
                    areas[j] = B
                    areas[i] = B
                    pairs[j] = i
                    pairs[i] = j
            if pairs[i]> -1:
                guideGroups.append((self.guides[i],self.guides[pairs[i]]))
        print "Number of Guide Groups to be rendered: ", len(guideGroups)
        return guideGroups
        
    def groupPeakyHair(self,Area):
        guideGroups =[]
        N= len(self.guides)
        #pair[n] contains the index of the guide that should be a guide-pair partner with the nth-guide
        pairs=[-1]*N
        #bunch of infinities
        areas = [1e6]*N
        print "Number of strands: ", N
        for i in xrange(0,len(self.guides)):
            if (pairs[i]>-1) and pairs[pairs[i]]==i: continue 
            for j in xrange(i+1,len(self.guides)):                
                B = curvePairArea(self.guides[i],self.guides[j])
                if (B==0): continue #duplicate strands can occur!
                #taking least upper bound to Area
                if areas[j]>B and B>=Area:
                    areas[j] = B
                    areas[i] = B
                    pairs[j] = i
                    pairs[i] = j
            if pairs[i]> -1:
                guideGroups.append((self.guides[i],self.guides[pairs[i]]))
        print "Number of Guide Groups to be rendered: ", len(guideGroups)
        return guideGroups


def curvePairArea(c1, c2):
    #returns infinity if the curve Pair dont have almost the same c.p.
    #good fix for long hair interpolation!
    #TODO: write a guideline/tutorial about control points
    if math.fabs(len(c1)-len(c2)) > 3: return 1e6
    d1=None
    d2=None
    if len(c1)>len(c2):
        d1=c1
        d2=c2
    else:
        d1=c2
        d2=c1
    A=0
    temp=0
    n=len(d1)-1
    for i in xrange(1,len(d2)):
        try:
            if i>len(d1):
                temp = aljabr.convexQuadrilateralArea(d1[n-1],d2[i-1],d2[i],d1[n])
            else:
                temp = aljabr.convexQuadrilateralArea(d1[i-1],d2[i-1],d2[i],d1[i])
        except:
            return 0
        A = A+temp
    return A
