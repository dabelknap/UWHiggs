'''
H to ZZ to 4l analyzer for the 4mu final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy
import json

Z_MASS = 91.188

class AnalyzeMMMM( MegaBase ):
    tree = 'mmmm/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree      = tree
        self.outfile   = outfile
        self.event_set = set()
        self.ntuple    = {}
        self.jsonFile  = open('4m_output.json','w')

    def begin(self):
        # self.mytree = self.book('./', 'hzz4m', 'hzz4m', type=rt.TTree)
        # self.mytree.CopyAddresses( self.tree )
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
            if not self.HZZ4l_phase_space(row):
                continue

            self.output_ntuple(row)
            self.eventCounts += 1
            self.event_set.add( row.evt )
            # self.mytree.Fill()


    def finish(self):
        print ""
        print self.eventCounts

        self.jsonFile.write( json.dumps(self.ntuple,indent=4) )
        self.jsonFile.close()

        pass


    # The selectors are located here
    def triggers(self, row):
        return (row.doubleMuPass == 1)


    def lepton_iso(self, row):
        return row.m1RelPFIsoRhoFSR < 0.4 and row.m2RelPFIsoRhoFSR < 0.4 and row.m3RelPFIsoRhoFSR < 0.4 and row.m4RelPFIsoRhoFSR < 0.4


    def lepton_trigger(self, row):
        pts = [ row.m1Pt, row.m2Pt, row.m3Pt, row.m4Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20.0 and pts[1] > 10.0


    def disambiguate_Zcands(self, row):
        '''
        Check that in the n-tuple row m1/m2 correspond to the first Z, and m3/m4 the second Z
        '''
        passed = True
        passed = passed and (row.m1_m2_SS == 0 and row.m3_m4_SS == 0)                        # make sure lepton pairs are opposite sign
        passed = passed and (row.m1Pt > row.m2Pt and row.m3Pt > row.m4Pt)                    # first lepton of a Z cand. should be leading in pt
        passed = passed and ( abs(row.m1_m2_Mass - Z_MASS) < abs(row.m3_m4_Mass - Z_MASS) )  # Z1 is closest to nominal Z mass

        return passed


    def qcd_suppress(self, row):
        '''
        Return true if opposite-sign leptons have an invariant mass greater than 4 GeV.
        '''
        passed = True

        if row.m1_m2_SS == 0:
            passed = passed and row.m1_m2_Mass > 4.0

        if row.m1_m3_SS == 0:
            passed = passed and row.m1_m3_Mass > 4.0

        if row.m1_m4_SS == 0:
            passed = passed and row.m1_m4_Mass > 4.0

        if row.m2_m3_SS == 0:
            passed = passed and row.m2_m3_Mass > 4.0

        if row.m2_m4_SS == 0:
            passed = passed and row.m2_m4_Mass > 4.0

        if row.m3_m4_SS == 0:
            passed = passed and row.m3_m4_Mass > 4.0

        return passed

    def z4l_phase_space(self, row):
        return row.MassFsr > 70.0

    def Z_mass(self, row):
        return 40.0 < row.m1_m2_MassFsr < 120.0 and 4.0 < row.m3_m4_MassFsr < 120.0

    def HZZ4l_phase_space(self, row):
        return row.MassFsr > 70.0 and row.m3_m4_MassFsr > 12.0

    def output_ntuple(self, rtRow):
        row = {}

        row["event"]   = rtRow.evt
        row["lumi"]    = rtRow.lumi
        row["run"]     = rtRow.run

        row["mass"]    = rtRow.MassFsr
        row["pt"]      = rtRow.PtFsr

        row["z1mass"]  = rtRow.m1_m2_MassFsr
        row["z1pt"]    = rtRow.m1_m2_PtFsr

        row["z2mass"]  = rtRow.m3_m4_MassFsr
        row["z2pt"]    = rtRow.m3_m4_PtFsr

        row["z1l1pt"]  = rtRow.m1Pt
        row["z1l2pt"]  = rtRow.m2Pt
        row["z2l1pt"]  = rtRow.m3Pt
        row["z2l2pt"]  = rtRow.m4Pt

        row["z1l1eta"]  = rtRow.m1Eta
        row["z1l2eta"]  = rtRow.m2Eta
        row["z2l1eta"]  = rtRow.m3Eta
        row["z2l2eta"]  = rtRow.m4Eta

        row["z1l1phi"]  = rtRow.m1Phi
        row["z1l2phi"]  = rtRow.m2Phi
        row["z2l1phi"]  = rtRow.m3Phi
        row["z2l2phi"]  = rtRow.m4Phi

        row["z1l1relIso"]  = rtRow.m1RelPFIsoRhoFSR
        row["z1l2relIso"]  = rtRow.m2RelPFIsoRhoFSR
        row["z2l1relIso"]  = rtRow.m3RelPFIsoRhoFSR
        row["z2l2relIso"]  = rtRow.m4RelPFIsoRhoFSR

        self.ntuple[rtRow.evt] = row
