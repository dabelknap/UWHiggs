'''
H to ZZ to 4l analyzer for the 4e final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy
import tables as tb
import json
from Event import Event4l
from mcWeighting import make_PUCorrector
from math import floor

Z_MASS = 91.188

class AnalyzeEEEE(MegaBase):
    tree = 'eeee/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree      = tree
        self.outfile   = outfile
        self.event_set = set()
        self.pucorrector = make_PUCorrector()

    def begin(self):
        # Open lepton scale factor files
        self.ele_scale_file = rt.TFile("./LepScale/CombinedMethod_ScaleFactors_RecoIdIsoSip.root", "READ")
        self.ele_scale_hist = self.ele_scale_file.Get("h_electronScaleFactor_RecoIdIsoSip")


        self.h5file = tb.open_file('output.h5', mode='a')
        try:
            self.h5file.removeNode("/EEEE", recursive=True)
        except tb.NodeError:
            pass
        self.h5group = self.h5file.create_group(
                '/',
                'EEEE',
                'Higgs to ZZ to 4e'
                )
        self.h5table = self.h5file.create_table(
                self.h5group,
                'events',
                Event4l,
                'Selected 4e Events'
                )
        self.h5row = self.h5table.row

        with open("./PU/2012/pu_2012.json", 'r') as pu_file:
            self.pu_weights = json.load(pu_file)


    def process(self):
        prev_evt = 0
        self.eventCounts = 0
        for row in self.tree:
            if row.evt in self.event_set:
                continue
            if not self.triggers(row):
                continue
            if not self.Z_mass(row):
                continue
            if not self.lepton_iso(row):
                continue
            if not self.lepton_trigger(row):
                continue
            if not self.qcd_suppress(row):
                continue
            if not self.HZZ4l_phase_space(row):
                continue

            self.event_set.add(row.evt)
            self.store_row(row)
            self.eventCounts += 1

            if self.eventCounts % 1000 == 0:
                self.h5table.flush()


    def finish(self):
        self.ele_scale_file.Close()
        print ""
        print self.eventCounts

        self.h5table.flush()
        self.h5file.close()


    def ele_scale_factor(self, row):
        out = 1.0
        for l in [1, 2, 3, 4]:
            pt = getattr(row, "e%iPt" % l)
            eta = getattr(row, "e%iEta" % l)
            global_bin = self.ele_scale_hist.FindBin(pt, eta)
            #out *= self.ele_scale_hist.GetBinContent(global_bin)
            scl = self.ele_scale_hist.GetBinContent(global_bin)
            if scl < 0.1:
                scl = 1.0
            out *= scl
        return out


    def pu_weight(self, row):
        # If data, don't weight
        if row.run > 2:
            return 1.0
        else:
            return self.pu_weights[str(int(floor(row.nTruePU)))]


    def lep_scale(self, row):
        # If data, don't weight
        if row.run > 2:
            return 1.0
        else:
            return self.ele_scale_factor(row)


    # The selectors are located here
    def triggers(self, row):
        #return (row.doubleEPass == 1)
        return (row.tripleEPass > 0.5 or row.doubleETightPass > 0.5)


    def lepton_trigger(self, row):
        pts = [ row.e1Pt, row.e2Pt, row.e3Pt, row.e4Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20 and pts[1] > 10


    def Z_mass(self, row):
        return 40 < row.e1_e2_MassFsr < 120 and 4 < row.e3_e4_MassFsr < 120


    def lepton_iso(self, row):
        # print "->", row.e1RelPFIsoRho ,  row.e2RelPFIsoRho ,  row.e3RelPFIsoRho ,  row.e4RelPFIsoRho
        return row.e1RelPFIsoRhoFSR < 0.4 and row.e2RelPFIsoRhoFSR < 0.4 and row.e3RelPFIsoRhoFSR < 0.4 and row.e4RelPFIsoRhoFSR < 0.4


    def qcd_suppress(self, row):
        '''
        Return true if opposite-sign leptons have an invariant mass greater than 4 GeV.
        '''
        passed = True

        if row.e1_e2_SS == 0:
            passed = passed and row.e1_e2_Mass > 4

        if row.e1_e3_SS == 0:
            passed = passed and row.e1_e3_Mass > 4

        if row.e1_e4_SS == 0:
            passed = passed and row.e1_e4_Mass > 4

        if row.e2_e3_SS == 0:
            passed = passed and row.e2_e3_Mass > 4

        if row.e2_e4_SS == 0:
            passed = passed and row.e2_e4_Mass > 4

        if row.e3_e4_SS == 0:
            passed = passed and row.e3_e4_Mass > 4

        return passed


    def HZZ4l_phase_space(self, row):
        return row.MassFsr > 70 and row.e3_e4_MassFsr > 12
    

    def store_row(self, rtRow):
        self.h5row['channel']       = '4e'
        self.h5row['event']         = rtRow.evt
        self.h5row['lumi']          = rtRow.lumi
        self.h5row['run']           = rtRow.run

        self.h5row["pu_weight"]     = self.pu_weight(rtRow)
        self.h5row["lep_weight"]    = self.lep_scale(rtRow)

        self.h5row['mass']          = rtRow.MassFsr
        self.h5row['pt']            = rtRow.PtFsr

        self.h5row['z1mass']        = rtRow.e1_e2_MassFsr
        self.h5row['z1pt']          = rtRow.e1_e2_PtFsr

        self.h5row['z2mass']        = rtRow.e3_e4_MassFsr
        self.h5row['z2pt']          = rtRow.e3_e4_PtFsr

        self.h5row['l1ID']          = 11
        self.h5row['l2ID']          = 11
        self.h5row['l3ID']          = 11
        self.h5row['l4ID']          = 11

        self.h5row["l1pt"]          = rtRow.e1Pt
        self.h5row["l2pt"]          = rtRow.e2Pt
        self.h5row["l3pt"]          = rtRow.e3Pt
        self.h5row["l4pt"]          = rtRow.e4Pt

        self.h5row["l1eta"]         = rtRow.e1Eta
        self.h5row["l2eta"]         = rtRow.e2Eta
        self.h5row["l3eta"]         = rtRow.e3Eta
        self.h5row["l4eta"]         = rtRow.e4Eta

        self.h5row["l1phi"]         = rtRow.e1Phi
        self.h5row["l2phi"]         = rtRow.e2Phi
        self.h5row["l3phi"]         = rtRow.e3Phi
        self.h5row["l4phi"]         = rtRow.e4Phi

        self.h5row['KD']            = rtRow.KD

        self.h5row['costheta1']     = rtRow.costheta1
        self.h5row['costheta2']     = rtRow.costheta2
        self.h5row['costhetastar']  = rtRow.costhetastar
        self.h5row['Phi']           = rtRow.Phi
        self.h5row['Phi1']          = rtRow.Phi1

        self.h5row['costheta1_gen']     = rtRow.costheta1_gen
        self.h5row['costheta2_gen']     = rtRow.costheta2_gen
        self.h5row['costhetastar_gen']  = rtRow.costhetastar_gen
        self.h5row['Phi_gen']           = rtRow.Phi_gen
        self.h5row['Phi1_gen']          = rtRow.Phi1_gen

        self.h5row.append()


    def output_ntuple_json(self, rtRow):
        row = {}

        row["event"]   = rtRow.evt
        row["lumi"]    = rtRow.lumi
        row["run"]     = rtRow.run

        row["mass"]    = rtRow.MassFsr
        row["pt"]      = rtRow.PtFsr

        row["z1mass"]  = rtRow.e1_e2_MassFsr
        row["z1pt"]    = rtRow.e1_e2_PtFsr

        row["z2mass"]  = rtRow.e3_e4_MassFsr
        row["z2pt"]    = rtRow.e3_e4_PtFsr

        row["z1l1pt"]  = rtRow.e1Pt
        row["z1l2pt"]  = rtRow.e2Pt
        row["z2l1pt"]  = rtRow.e3Pt
        row["z2l2pt"]  = rtRow.e4Pt

        row["z1l1eta"]  = rtRow.e1Eta
        row["z1l2eta"]  = rtRow.e2Eta
        row["z2l1eta"]  = rtRow.e3Eta
        row["z2l2eta"]  = rtRow.e4Eta

        row["z1l1phi"]  = rtRow.e1Phi
        row["z1l2phi"]  = rtRow.e2Phi
        row["z2l1phi"]  = rtRow.e3Phi
        row["z2l2phi"]  = rtRow.e4Phi

        row["z1l1relIso"]  = rtRow.e1RelPFIsoRhoFSR
        row["z1l2relIso"]  = rtRow.e2RelPFIsoRhoFSR
        row["z2l1relIso"]  = rtRow.e3RelPFIsoRhoFSR
        row["z2l2relIso"]  = rtRow.e4RelPFIsoRhoFSR

        row["channel"] = "4e"

        self.ntuple[rtRow.evt] = row