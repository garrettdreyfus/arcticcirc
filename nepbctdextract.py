import scipy
import scipy.io as sio
import numpy as np
from progress.bar import Bar
from profile import Profile
import pickle
import gsw


#generate a unique id
def idgenerator():
    if not hasattr(idgenerator,"id"):
        idgenerator.id=0
    idgenerator.id = idgenerator.id+1
    return idgenerator.id


def nepbCTDExtract(fname,savepath):
    ctddata = sio.loadmat(fname)
    lats = np.asarray(ctddata["lat"])[0]
    lons = np.asarray(ctddata["lon"])[0]
    pres = np.asarray(ctddata["Pint"]).T[0]
    sals = np.asarray(ctddata["Sint"]).T
    thetas = np.asarray(ctddata["Tint"]).T
    CT = np.asarray(ctddata["CT"]).T
    SA = np.asarray(ctddata["Sint_abs"]).T
    nspres = np.asarray(ctddata["P_gamma"]).T
    PV = np.asarray(ctddata["PV"]).T
    ns = np.asarray(ctddata["P_gref"])
    profiles = []
    for p in Bar("profile").iter(range(len(lats))):
        data = {}
        knownns = {}
        knownpv = {}
        if lats[p]>20 and lons[p]<0 or lons[p] > 170:
            data["lat"]=lats[p]
            data["lon"]=lons[p]
            data["temp"]=[]
            data["sal"]=[]
            data["pres"]=[]
            for j in range(len(pres)):
                if ~np.isnan(sals[p][j]) and ~np.isnan(thetas[p][j]) and ~np.isnan(pres[j])\
                        and abs(pres[j]) < 10000 and abs(thetas[p][j])<30 and abs(sals[p][j])<50:
                    insitutemp = thetas[p][j]
                    practicalsal = sals[p][j]
                    singlepres = abs(pres[j])
                    abssal = gsw.SA_from_SP(practicalsal,singlepres,lons[p],lats[p])
                    conservativetemp = gsw.CT_from_t(abssal,insitutemp,singlepres)
                    if abs(abssal-SA[p][j]) > 0.001:
                        print("saldiff = ",abssal-SA[p][j])
                    if abs(conservativetemp-CT[p][j]) > 0.001:
                        print("tempdiff = ",conservativetemp-CT[p][j])
                    data["temp"].append(insitutemp)
                    data["sal"].append(practicalsal)
                    data["pres"].append(singlepres)
            for a in range(len(ns)):
                knownns[ns[a][0]]=nspres[p][a]
            for a in range(len(ns)):
                knownpv[ns[a][0]]=PV[p][a]
            data["knownns"]=knownns
            data["knownpv"]=knownpv

            if len(data["pres"])>4 and max(data["pres"])>1500:
                eyed=idgenerator()
                p=Profile(eyed,data)
                profiles.append(p)
                
    with open(savepath, 'wb') as outfile:
        pickle.dump(profiles, outfile)

nepbCTDExtract("data/newnepbdata.mat","data/nepbctdprofiles.pickle")

