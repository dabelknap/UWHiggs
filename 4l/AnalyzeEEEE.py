'''
H to ZZ to 4l analyzer for the 4e final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy
import json

Z_MASS = 91.188

class AnalyzeEEEE(MegaBase):
    tree = 'eeee/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree      = tree
        self.outfile   = outfile
        self.event_set = set()
        self.ntuple    = {}
        self.jsonFile  = open('4e_output.json','w')

    def begin(self):
        pass

    def process(self):
        prev_evt = 0
        self.eventCounts = 0
        for row in self.tree:
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
            if not self.z4l_phase_space(row):
                continue
            if not self.HZZ4l_phase_space(row):
                continue

            self.output_ntuple(row)
            self.eventCounts += 1
            self.event_set.add( row.evt )


    def finish(self):
        print ""
        print self.eventCounts

        self.jsonFile.write( json.dumps(self.ntuple,indent=4) )
        self.jsonFile.close()
        pass


    def lepton_trigger(self, row):
        pts = [ row.e1Pt, row.e2Pt, row.e3Pt, row.e4Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20 and pts[1] > 10


    def Z_mass(self, row):
        return 40 < row.e1_e2_MassFsr < 120 and 4 < row.e3_e4_MassFsr < 120


    # The selectors are located here
    def triggers(self, row):
        return (row.doubleEPass == 1)


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

    def z4l_phase_space(self, row):
        return row.MassFsr > 70

    def HZZ4l_phase_space(self, row):
        return row.MassFsr > 70 and row.e3_e4_MassFsr > 12
    
    def output_ntuple(self, rtRow):
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
