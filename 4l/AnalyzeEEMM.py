'''
H to ZZ to 4l analyzer for the 2e2mu final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy
import tables as tb
from Event import Event4l
from mcWeighting import make_PUCorrector
from math import floor

Z_MASS = 91.188

class AnalyzeEEMM(MegaBase):
    tree = 'eemm/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree      = tree
        self.outfile   = outfile
        self.event_set = set()
        self.pucorrector = make_PUCorrector()

    def begin(self):
        self.h5file = tb.open_file('output.h5', mode='a')
        try:
            self.h5file.removeNode("/EEMM", recursive=True)
        except tb.NodeError:
            pass
        self.h5group = self.h5file.create_group(
                "/",
                'EEMM',
                'Higgs to ZZ to 2e2mu'
                )
        self.h5table = self.h5file.create_table(
                self.h5group,
                'events',
                Event4l,
                "Selected 2e2mu Events"
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
            #print row.evt, " ", row.Mass, " ", row.e1_e2_Mass, " ", row.m1_m2_Mass, " ", row.e1Pt, " ", row.e2Pt, " ", row.m1Pt, " ", row.m2Pt
            self.eventCounts += 1
            self.store_row(row)

            self.event_set.add(row.evt)

            if self.eventCounts % 1000 == 0:
                self.h5table.flush()


    def finish(self):
        print ""
        print self.eventCounts

        self.h5table.flush()
        self.h5file.close()


    def event_weight(self, row):
        # If data, don't weight
        if row.run > 2:
            return 1.0
        else:
            return self.pu_weights[str(int(floor(row.nTruePU)))]


    # The selectors are located here
    def triggers(self, row):
        return True


    def lepton_trigger(self, row):
        pts = [ row.e1Pt, row.e2Pt, row.m1Pt, row.m2Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20 and pts[1] > 10


    def lepton_iso(self, row):
        return row.e1RelPFIsoRho < 0.4 and row.e2RelPFIsoRho < 0.4 and row.m1RelPFIsoRho < 0.4 and row.m2RelPFIsoRho < 0.4


    def Z_mass(self, row):
        Z1, Z2 = self.identifyZ(row)
        return 40 < Z1 < 120 and 4 < Z2 < 120


    def identifyZ(self, row):
        Zee = row.e1_e2_MassFsr
        Zmm = row.m1_m2_MassFsr
        
        if ( abs(Z_MASS - Zee) < abs(Z_MASS - Zmm) ):
            return (Zee, Zmm)
        else:
            return (Zmm, Zee)


    def switchZ(self, row):
        Zee = row.e1_e2_MassFsr
        Zmm = row.m1_m2_MassFsr
        
        if ( abs(Z_MASS - Zee) < abs(Z_MASS - Zmm) ):
            return False
        else:
            return True



    def qcd_suppress(self, row):
        '''
        Return true if opposite-sign leptons have an invariant mass greater than 4 GeV.
        '''
        passed = True

        if row.e1_e2_SS == 0:
            passed = passed and row.e1_e2_MassFsr > 4

        if row.e1_m1_SS == 0:
            passed = passed and row.e1_m1_MassFsr > 4

        if row.e1_m2_SS == 0:
            passed = passed and row.e1_m2_MassFsr > 4

        if row.e2_m1_SS == 0:
            passed = passed and row.e2_m1_MassFsr > 4

        if row.e2_m2_SS == 0:
            passed = passed and row.e2_m2_MassFsr > 4

        if row.m1_m2_SS == 0:
            passed = passed and row.m1_m2_MassFsr > 4

        return passed


    def z4l_phase_space(self, row):
        return row.MassFsr > 70


    def HZZ4l_phase_space(self, row):
        Z1, Z2 = self.identifyZ(row)
        return row.MassFsr > 70 and Z2 > 12


    def store_row(self, rtRow):
        switch = self.switchZ(rtRow)

        self.h5row['channel']       = '2e2mu'
        self.h5row['event']         = rtRow.evt
        self.h5row['lumi']          = rtRow.lumi
        self.h5row['run']           = rtRow.run

        self.h5row["pu_weight"]     = self.event_weight(rtRow)

        self.h5row['mass']          = rtRow.MassFsr
        self.h5row['pt']            = rtRow.PtFsr

        if switch:
            self.h5row['z1mass']        = rtRow.m1_m2_MassFsr
            self.h5row['z1pt']          = rtRow.m1_m2_PtFsr

            self.h5row['z2mass']        = rtRow.e1_e2_MassFsr
            self.h5row['z2pt']          = rtRow.e1_e2_PtFsr

            self.h5row['l1ID']          = 13
            self.h5row['l2ID']          = 13
            self.h5row['l3ID']          = 11
            self.h5row['l4ID']          = 11

            self.h5row["l1pt"]          = rtRow.m1Pt
            self.h5row["l2pt"]          = rtRow.m2Pt
            self.h5row["l3pt"]          = rtRow.e1Pt
            self.h5row["l4pt"]          = rtRow.e2Pt

            self.h5row["l1eta"]         = rtRow.m1Eta
            self.h5row["l2eta"]         = rtRow.m2Eta
            self.h5row["l3eta"]         = rtRow.e1Eta
            self.h5row["l4eta"]         = rtRow.e2Eta

            self.h5row["l1phi"]         = rtRow.m1Phi
            self.h5row["l2phi"]         = rtRow.m2Phi
            self.h5row["l3phi"]         = rtRow.e1Phi
            self.h5row["l4phi"]         = rtRow.e2Phi

        else:
            self.h5row['z1mass']        = rtRow.e1_e2_MassFsr
            self.h5row['z1pt']          = rtRow.e1_e2_PtFsr

            self.h5row['z2mass']        = rtRow.m1_m2_MassFsr
            self.h5row['z2pt']          = rtRow.m1_m2_PtFsr

            self.h5row['l1ID']          = 11
            self.h5row['l2ID']          = 11
            self.h5row['l3ID']          = 13
            self.h5row['l4ID']          = 13

            self.h5row["l1pt"]          = rtRow.e1Pt
            self.h5row["l2pt"]          = rtRow.e2Pt
            self.h5row["l3pt"]          = rtRow.m1Pt
            self.h5row["l4pt"]          = rtRow.m2Pt

            self.h5row["l1eta"]         = rtRow.e1Eta
            self.h5row["l2eta"]         = rtRow.e2Eta
            self.h5row["l3eta"]         = rtRow.m1Eta
            self.h5row["l4eta"]         = rtRow.m2Eta

            self.h5row["l1phi"]         = rtRow.e1Phi
            self.h5row["l2phi"]         = rtRow.e2Phi
            self.h5row["l3phi"]         = rtRow.m1Phi
            self.h5row["l4phi"]         = rtRow.m2Phi

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
