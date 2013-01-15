'''
H to ZZ to 4l analyzer for the 4mu final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

Z_MASS = 91.188

class AnalyzeMMMM(MegaBase):
    tree = 'mmmm/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree = tree
        self.outfile = outfile

    def begin(self):
        pass

    def process(self):
        self.eventCounts = 0
        for row in self.tree:
            if not self.triggers(row):
                continue
            if not self.loose_lepton(row):
                continue
            if not self.assign_Z_candidates(row):
                continue
            if not self.qcd_suppress(row):
                continue
            if not self.z4l_phase_space(row):
                continue
            if not self.HZZ4l_phase_space(row):
                continue
            self.eventCounts += 1


    def finish(self):
        print "Events Passed", self.eventCounts
        pass


    # The selectors are located here
    def triggers(self, row):
        return (row.doubleMuPass == 1)

    def loose_lepton(self, row):
        pt_pass  = row.m1Pt > 5 and row.m2Pt > 5 and row.m3Pt > 5 and row.m4Pt > 5
        eta_pass = row.m1AbsEta < 2.4 and row.m2AbsEta < 2.4 and row.m3AbsEta < 2.4 and row.m4AbsEta < 2.4
        dxy_pass = row.m1PVDXY < 0.5 and row.m2PVDXY < 0.5 and row.m3PVDXY < 0.5 and row.m4PVDXY < 0.5
        dz_pass  = row.m1PVDZ < 0.5 and row.m2PVDZ < 0.5 and row.m3PVDZ < 0.5 and row.m4PVDZ < 0.5
        muon_id  = (row.m1IsGlobal or row.m1IsTracker) and (row.m2IsGlobal or row.m2IsTracker) and  (row.m3IsGlobal or row.m3IsTracker) and  (row.m4IsGlobal or row.m4IsTracker)

        return pt_pass and eta_pass and dxy_pass and dz_pass and muon_id

    def assign_Z_candidates(self, row):
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

    def HZZ4l_phase_space(self, row):
        return row.Mass > 100 and row.m3_m4_Mass > 12
