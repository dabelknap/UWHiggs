'''
H to ZZ to 4l analyzer for the 4mu final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy

Z_MASS = 91.188

class AnalyzeMMMM( MegaBase ):
    tree = 'mmmm/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree      = tree
        self.outfile   = outfile
        self.event_set = set()

    def begin(self):
        # self.mytree = self.book('path/to/', 'ntupleName', 'ntupleTitle', type=ROOT.TTree)
        # self.mytree.CopyAddresses( self.tree )
        pass

    def process(self):
        prev_evt = 0
        self.eventCounts = 0
        for row in self.tree:
            if not self.triggers(row):
                continue
            if not self.loose_lepton(row):
                continue
            if not self.Z_mass(row):
                continue
            if not self.lepton_iso2(row):
                continue
            if not self.lepton_trigger(row):
                continue
            if not self.qcd_suppress(row):
                continue
            if not self.HZZ4l_phase_space(row):
                continue
            print row.evt, " ", row.Mass, " ", row.m1_m2_Mass, " ", row.m3_m4_Mass, " ", row.m1Pt, " ", row.m2Pt, " ", row.m3Pt, " ", row.m4Pt
            self.eventCounts += 1
            self.event_set.add( row.evt )
            # self.mytree.Fill()


    def finish(self):
        print ""
        print self.eventCounts
        print self.event_set
        pass


    # The selectors are located here
    def triggers(self, row):
        return (row.doubleMuPass == 1)


    def loose_lepton(self, row):
        pt_pass  = row.m1Pt > 5 and row.m2Pt > 5 and row.m3Pt > 5 and row.m4Pt > 5
        eta_pass = row.m1AbsEta < 2.4 and row.m2AbsEta < 2.4 and row.m3AbsEta < 2.4 and row.m4AbsEta < 2.4
        dxy_pass = row.m1PVDXY < 0.5 and row.m2PVDXY < 0.5 and row.m3PVDXY < 0.5 and row.m4PVDXY < 0.5
        dz_pass  = row.m1PVDZ < 1 and row.m2PVDZ < 1 and row.m3PVDZ < 1 and row.m4PVDZ < 1
        muon_id  = (row.m1IsGlobal or row.m1IsTracker) and (row.m2IsGlobal or row.m2IsTracker) and  (row.m3IsGlobal or row.m3IsTracker) and  (row.m4IsGlobal or row.m4IsTracker)

        return pt_pass and eta_pass and dxy_pass and dz_pass and muon_id


    def pfRelIso(self, pt, chrg, neuHad, phot, rho, EA):
        iso = ( chrg + max(0.0, neuHad + phot - rho*EA) )/pt
        return iso


    def lepton_iso(self, row):
        l1_iso = self.pfRelIso( row.m1Pt, row.m1PFChargedIso, row.m1PFNeutralIso, row.m1PFPhotonIso, row.rho, row.m1EffectiveArea2012 )
        l2_iso = self.pfRelIso( row.m2Pt, row.m2PFChargedIso, row.m2PFNeutralIso, row.m2PFPhotonIso, row.rho, row.m2EffectiveArea2012 )
        l3_iso = self.pfRelIso( row.m3Pt, row.m3PFChargedIso, row.m3PFNeutralIso, row.m3PFPhotonIso, row.rho, row.m3EffectiveArea2012 )
        l4_iso = self.pfRelIso( row.m4Pt, row.m4PFChargedIso, row.m4PFNeutralIso, row.m4PFPhotonIso, row.rho, row.m4EffectiveArea2012 )

        print "->", l1_iso, l2_iso, l3_iso, l4_iso

        return l1_iso < 0.4 and l2_iso < 0.4 and l3_iso < 0.4 and l4_iso < 0.4


    def lepton_iso2(self, row):
        print "->", row.m1RelPFIsoRho ,  row.m2RelPFIsoRho ,  row.m3RelPFIsoRho ,  row.m4RelPFIsoRho
        return row.m1RelPFIsoRho < 0.4 and row.m2RelPFIsoRho < 0.4 and row.m3RelPFIsoRho < 0.4 and row.m4RelPFIsoRho < 0.4


    def lepton_trigger(self, row):
        pts = [ row.m1Pt, row.m2Pt, row.m3Pt, row.m4Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20 and pts[1] > 10


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
            passed = passed and row.m1_m2_Mass > 4

        if row.m1_m3_SS == 0:
            passed = passed and row.m1_m3_Mass > 4

        if row.m1_m4_SS == 0:
            passed = passed and row.m1_m4_Mass > 4

        if row.m2_m3_SS == 0:
            passed = passed and row.m2_m3_Mass > 4

        if row.m2_m4_SS == 0:
            passed = passed and row.m2_m4_Mass > 4

        if row.m3_m4_SS == 0:
            passed = passed and row.m3_m4_Mass > 4

        return passed

    def z4l_phase_space(self, row):
        return row.Mass > 70

    def Z_mass(self, row):
        return 40 < row.m1_m2_Mass < 120 and 4 < row.m3_m4_Mass < 120

    def HZZ4l_phase_space(self, row):
        return row.Mass > 70 and row.m3_m4_Mass > 12
