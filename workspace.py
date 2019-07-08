import nstools
import saloffset
import matplotlib.pyplot as plt
import pickle
from mpl_toolkits.basemap import Basemap
import numpy as np
import json
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyproj
import copy
    

#offsets, profiles, deepestindex = saloffset.runSalinityOffsetTool(["data/1500mprofiles.json"],["ODEN_AGAVE"])

##profiles,deepestindex = nstools.extractProfilesBox(["data/1500mprofiles.json"],-180,180,65,90)
##profiles,deepestindex = nstools.removeNorwegianSea(profiles)
#nstools.plotCruise(profiles,"IPY 2007")
##print(offsets)
#profiles = nstools.filterCruises(profiles,offsets.keys())
#profiles = saloffset.applyOffsets(profiles,offsets)

#fileObject = open("1500NoNorwegian.pickle",'wb')  
## load the object from the file into var b
#b = pickle.dump([offsets,profiles,deepestindex],fileObject)  
#fileObject.close()


#USING CORRECTED PICKLED SURFACES TO MAP NEUTRAL SURFACES USING PEER SEARCH

#fileObject = open("1500NoNorwegian.pickle",'rb')  
#offsets,profiles,deepestindex = pickle.load(fileObject)
#fileObject.close()

#nstools.plotCruise(profiles,"IPY 2007")
#deepestindex = nstools.deepestProfile(profiles)
##profilechoice = random.choice(nstools.profileInBox(profiles,-180,180,60,90))
#profilechoice = profiles[deepestindex]
#surfaces = {}
#for d in range(200,4000,200)[::-1]:
    #print(d)
    #surfaces.update(nstools.peerSearch(profiles.copy(),deepestindex,d,profilechoice,1000))

#nstools.graphSurfaces(surfaces)

#fileObject = open(str(profilechoice.eyed)+".pickle",'wb')  
## load the object from the file into var b
#b = pickle.dump(surfaces,fileObject)  
#fileObject.close()

##############################################
## 

#fileObject = open("data/286364.pickle",'rb')  
#surfaces = pickle.load(fileObject)
#fileObject.close()
#fileObject = open("data/1500NoNorwegian.pickle",'rb')  
#offsets,profiles,deepestindex = pickle.load(fileObject)
#fileObject.close()
#tempSurfs = {}
#for d in surfaces.keys():
    #tempSurf = [[],[],[],[]]
    #for l in range(len(surfaces[d][0])):
        #p = nstools.getProfileById(profiles,surfaces[d][3][l])
        #t,s = p.atPres(surfaces[d][2][l])
        #pv = p.potentialVorticity(surfaces[d][2][l])
        ##if pv and pv <0:
            ##print(pv)
            ##print(p.lat,p.lon,p.eyed)
            ##print(surfaces[d][2][l])
            ###nstools.plotProfile(p)
        ##elif pv:
        #tempSurf[0].append(surfaces[d][0][l])
        #tempSurf[1].append(surfaces[d][1][l])
        #tempSurf[2].append(-surfaces[d][2][l])
        #tempSurf[3].append(surfaces[d][3][l])
    ##tempSurffinal = [[],[],[],[]]
    ##m = np.mean(tempSurf[2])
    ##s = np.std(tempSurf[2])
    ##for j in range(len(tempSurf[2])):
        ##if m-2*s < tempSurf[2][j] < m + 2*s:
            ##tempSurffinal[0].append(tempSurf[0][j])
            ##tempSurffinal[1].append(tempSurf[1][j])
            ##tempSurffinal[2].append(-tempSurf[2][j])
            ##tempSurffinal[3].append(tempSurf[3][j])

    #if len(tempSurf[0])>5:
        #tempSurfs[d] = tempSurf

#nstools.graphSurfaces(tempSurfs)

#####################################################################
#print(runSalinityOffsetTool(glob.glob("data/3000m2007profiles.json"),["Polarstern_ARK-XXIII_2"]))
#singleSalinityOffsetRun("data/2000mprofiles.json","LOUIS_S._ST._LAURENT_18SN940","HUDSON_HUDSON2")
#profiles,deepestindex = nstools.extractProfilesMonths("data/3000m2008profiles.json",range(13))
#nstools.plotCruise(nstools.cruiseSearch(profiles,"LOUIS_S._ST._LAURENT_18SN940",1994),"name")

#print("DONE WITH EXTRACTING PROFILES")
#surfaces = nstools.search(profiles,deepestindex)
#print("DONE FINDING SURFACES")
#with open('data/surfaces.json', 'w') as outfile:
    #json.dump(surfaces, outfile)
#json_file = open("data/surfaces.json") 
#surfaces = json.load(json_file)
#print("NOW GRAPHING")
#nstools.graphSurfaces(surfaces)
#######################################33333


#fileObject = open("data/286364.pickle",'rb')  
#surfaces = pickle.load(fileObject)
#fileObject.close()
fileObject = open("data/1500NoNorwegian.pickle",'rb')  
offsets,profiles,deepestindex = pickle.load(fileObject)
#nstools.findNeighboringPoints(profiles,profiles[2].lat,profiles[2].lon)
#nstools.plotASpiral(profiles)
#fileObject.close()
#print("Everythings loaded up")
#surfaces = nstools.addDataToSurfaces(profiles,surfaces,2)
#with open('data/surfacesWithData.pickle', 'wb') as outfile:
    #pickle.dump(surfaces, outfile)
fileObject = open("data/surfacesWithData.pickle",'rb')  
surfaces = pickle.load(fileObject)
originalsurfaces = copy.deepcopy(surfaces)
surfaces =nstools.surfacesToXYZPolar(surfaces)
#nstools.graphTransects(nstools.filterSurfacesByLine(originalsurfaces,40),0)
    ###############
interpolatedsurfaces = {}
for k in surfaces.keys():
    x = surfaces[k][0]
    y = surfaces[k][1]
    z = surfaces[k][2][0]
    d = surfaces[k][2][1:]
    #print(list(zip(x,y,z)))
    #x,y,z = nstools.deduplicateXYZ(x,y,z)
    x,y,z,d = nstools.removeDiscontinuities(x,y,z,radius=0.1,auxdata=d)
    xi,yi,zi,di = nstools.interpolateSurfaceGAM(x,y,z,d)
    #xi,yi,zi,di = nstools.interpolateSurface(x,y,z,d)

    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(x,y,z)

    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ##ax.scatter(xi,yi,zi,c=di[1])
    #ax.scatter(xi,yi,zi)

    #plt.show()
    #interpolatedsurfaces.update(nstools.removeOutlierSurfaces(nstools.xyzToSurface(xi,yi,zi,di,k)))
    interpolatedsurfaces.update(nstools.xyzToSurfacePolar(xi,yi,zi,di,k))

#nstools.graphNeighbors(interpolatedsurfaces,(nstools.generateNeighborsLists(interpolatedsurfaces)))
#nstools.graphSurfaces(interpolatedsurfaces,0,show=False,savepath="refpics/RUN3GAMPOLAR/")
#nstools.graphSurfaces(nstools.filterSurfacesByLine(interpolatedsurfaces,40),0,show=True)
#nstools.graphTransects(nstools.filterSurfacesByLine(interpolatedsurfaces,40),0)
for i in range(0,4):
    nstools.graphSurfaces(interpolatedsurfaces,i,show=False,savepath="refpics/RUN3GAMPOLAR/")
    #nstools.graphSurfaces(interpolatedsurfaces,i,show=True)


