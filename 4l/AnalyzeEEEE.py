'''
H to ZZ to 4l analyzer for the 4e final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy

Z_MASS = 91.188

class AnalyzeEEEE(MegaBase):
    tree = 'eeee/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree      = tree
        self.outfile   = outfile
        self.event_set = set()

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
            print row.evt, " ", row.Mass, " ", row.e1_e2_Mass, " ", row.e3_e4_Mass, " ", row.e1Pt, " ", row.e2Pt, " ", row.e3Pt, " ", row.e4Pt
            self.eventCounts += 1
            self.event_set.add( row.evt )


    def finish(self):
        print ""
        print self.eventCounts
        print self.event_set
        pass


    def lepton_trigger(self, row):
        pts = [ row.e1Pt, row.e2Pt, row.e3Pt, row.e4Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20 and pts[1] > 10


    def Z_mass(self, row):
        return 40 < row.e1_e2_Mass < 120 and 4 < row.e3_e4_Mass < 120


    # The selectors are located here
    def triggers(self, row):
        return (row.doubleEPass == 1)


    def lepton_iso(self, row):
        # print "->", row.e1RelPFIsoRho ,  row.e2RelPFIsoRho ,  row.e3RelPFIsoRho ,  row.e4RelPFIsoRho
        return row.e1RelPFIsoRho < 0.4 and row.e2RelPFIsoRho < 0.4 and row.e3RelPFIsoRho < 0.4 and row.e4RelPFIsoRho < 0.4


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
        return row.Mass > 70

    def HZZ4l_phase_space(self, row):
        return row.Mass > 70 and row.e3_e4_Mass > 12
