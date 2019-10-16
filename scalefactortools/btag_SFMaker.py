import ROOT as ROOT
import os
sys.path.append('../../ExoPieProducer/ExoPieAnalyzer/')
from Year import era

def weightbtag(reader, flav, pt, eta):
    sf_c = reader.eval_auto_bounds('central', flav, eta, pt)
    sf_low = reader.eval_auto_bounds('down', flav, eta, pt)
    sf_up  = reader.eval_auto_bounds('up', flav, eta, pt)
    btagsf = [sf_c, sf_low, sf_up]

def jetflav(flav):
    if flav == 5:
        flavor = 0
    elif flav == 4:
        flavor = 1
    else:
        flavor = 2
    return flavor


def getBeff(pt,eta,flav):
    if flav == 5:
        ybin = b_med_eff.GetXaxis().FindBin(eta)
        xbin = b_med_eff.GetYaxis().FindBin(pt)
        btag_eff = b_med_eff.GetBinContent(xbin,ybin)
        return btag_eff
    elif flav == 4:
        ybin = c_med_eff.GetXaxis().FindBin(eta)
        xbin = c_med_eff.GetYaxis().FindBin(pt)
        ctag_eff = c_med_eff.GetBinContent(xbin,ybin)
        return ctag_eff
    elif flav!=4 and flav!=5:
        ybin = udsg_med_eff.GetXaxis().FindBin(eta)
        xbin = udsg_med_eff.GetYaxis().FindBin(pt)
        lighttag_eff = udsg_med_eff.GetBinContent(xbin,ybin)
        return lighttag_eff

ROOT.gROOT.ProcessLine('.L btagSF_Files/BTagCalibrationStandalone.cpp+')

## ThinJets
if era=='2016':
    calib1 = ROOT.BTagCalibrationStandalone('deepcsv', 'btagSF_Files/2016_csv/DeepCSV_Moriond17_B_H.csv')
elif era=='2017':
    calib1 = ROOT.BTagCalibrationStandalone('deepcsv', 'btagSF_Files/2017_csv/DeepCSV_94XSF_V4_B_F.csv')
elif era=='2018':
    calib1 = ROOT.BTagCalibrationStandalone('deepcsv', 'btagSF_Files/2018_csv/DeepCSV_102XSF_V1.csv')

reader1 = ROOT.BTagCalibrationStandaloneReader( 0, "central", othersys)
reader1.load(calib1, 0,  "comb" )
reader1.load(calib1, 1,  "comb" )
reader1.load(calib1, 2,  "incl" )

def btag_weight(nJets,ptList,etalist,flavlist):
    P_MC = 1.0
    P_Data = 1.0
    btagweight = 1.0
    for i in range(nJets):
        tag_eff = getBeff(ptList[i],etalist[i],flavlist[i])
        P_MC *= (1-tag_eff)
        reader1.eval_auto_bounds('central', 0, 2.4, 30.)
        SF_jet = []
        SF_jet=weightbtag(reader1, jetflav(flavlist[i]), ptList[i], etalist[i])
        P_Data *= (1 - SF_jet[0] *tag_eff)
    if P_MC > 0:
        btagweight = P_Data/P_MC
        return btagweight
