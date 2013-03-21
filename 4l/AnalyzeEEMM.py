'''
H to ZZ to 4l analyzer for the 2e2mu final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy

Z_MASS = 91.188

class AnalyzeEEMM(MegaBase):
    tree = 'eemm/final/Ntuple'
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
            print row.evt, " ", row.Mass, " ", row.e1_e2_Mass, " ", row.m1_m2_Mass, " ", row.e1Pt, " ", row.e2Pt, " ", row.m1Pt, " ", row.m2Pt
            self.eventCounts += 1
            self.event_set.add( row.evt )


    def finish(self):
        print ""
        print self.eventCounts
        print self.event_set
        pass


    def lepton_trigger(self, row):
        pts = [ row.e1Pt, row.e2Pt, row.m1Pt, row.m2Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20 and pts[1] > 10


    def Z_mass(self, row):
        Z1, Z2 = self.identifyZ(row)
        return 40 < Z1 < 120 and 4 < Z2 < 120


    def identifyZ(self, row):
        Zee = row.e1_e2_Mass
        Zmm = row.m1_m2_Mass
        
        if ( abs(Z_MASS - Zee) < abs(Z_MASS - Zmm) ):
            return (Zee, Zmm)
        else:
            return (Zmm, Zee)



    # The selectors are located here
    def triggers(self, row):
        return True


    def lepton_iso(self, row):
        # print "->", row.e1RelPFIsoRho ,  row.e2RelPFIsoRho ,  row.m1RelPFIsoRho ,  row.m2RelPFIsoRho
        return row.e1RelPFIsoRho < 0.4 and row.e2RelPFIsoRho < 0.4 and row.m1RelPFIsoRho < 0.4 and row.m2RelPFIsoRho < 0.4


    def qcd_suppress(self, row):
        '''
        Return true if opposite-sign leptons have an invariant mass greater than 4 GeV.
        '''
        passed = True

        if row.e1_e2_SS == 0:
            passed = passed and row.e1_e2_Mass > 4

        if row.e1_m1_SS == 0:
            passed = passed and row.e1_m1_Mass > 4

        if row.e1_m2_SS == 0:
            passed = passed and row.e1_m2_Mass > 4

        if row.e2_m1_SS == 0:
            passed = passed and row.e2_m1_Mass > 4

        if row.e2_m2_SS == 0:
            passed = passed and row.e2_m2_Mass > 4

        if row.m1_m2_SS == 0:
            passed = passed and row.m1_m2_Mass > 4

        return passed

    def z4l_phase_space(self, row):
        return row.Mass > 70

    def HZZ4l_phase_space(self, row):
        Z1, Z2 = self.identifyZ(row)
        return row.Mass > 70 and Z2 > 12
