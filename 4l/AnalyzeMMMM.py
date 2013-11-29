'''
H to ZZ to 4l analyzer for the 4mu final state.

@author D. Austin Belknap
'''

from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import ROOT as rt
import numpy as npy
import json
import tables as tb
from Event import Event4l
from mcWeighting import make_PUCorrector
from math import floor

Z_MASS = 91.188

class AnalyzeMMMM( MegaBase ):
    tree = 'mmmm/final/Ntuple'
    global Z_MASS

    def __init__(self, tree, outfile, **kwargs):
        self.tree        = tree
        self.outfile     = outfile
        self.event_set   = set()
        self.pucorrector = make_PUCorrector()

    def begin(self):
        # Open HDF5 File
        self.h5file = tb.open_file('output.h5', mode='a')
        try:
            self.h5file.removeNode("/MMMM", recursive=True)
        except tb.NodeError:
            pass
        self.h5group = self.h5file.create_group(
                "/",
                'MMMM',
                'Higgs to ZZ to 4mu'
                )
        self.h5table = self.h5file.create_table(
                self.h5group,
                'events',
                Event4l,
                "Selected 4mu Events"
                )
        self.h5row = self.h5table.row

        with open("./PU/2012/pu_2012.json", 'r') as pu_file:
            self.pu_weights = json.load(pu_file)


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

            self.store_row(row)
            self.eventCounts += 1

            # flush the table every 1000 events to free memory
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
        return (row.doubleMuPass == 1)


    def lepton_trigger(self, row):
        pts = [ row.m1Pt, row.m2Pt, row.m3Pt, row.m4Pt ]
        pts.sort()
        pts.reverse()

        return pts[0] > 20.0 and pts[1] > 10.0


    def lepton_iso(self, row):
        return row.m1RelPFIsoRhoFSR < 0.4 and row.m2RelPFIsoRhoFSR < 0.4 and row.m3RelPFIsoRhoFSR < 0.4 and row.m4RelPFIsoRhoFSR < 0.4


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


    def store_row(self, rtRow):
        self.h5row['channel']       = '4mu'
        self.h5row['event']         = rtRow.evt
        self.h5row['lumi']          = rtRow.lumi
        self.h5row['run']           = rtRow.run

        self.h5row["pu_weight"]     = self.event_weight(rtRow)

        self.h5row['mass']          = rtRow.MassFsr
        self.h5row['pt']            = rtRow.PtFsr

        self.h5row['z1mass']        = rtRow.m1_m2_MassFsr
        self.h5row['z1pt']          = rtRow.m1_m2_PtFsr

        self.h5row['z2mass']        = rtRow.m3_m4_MassFsr
        self.h5row['z2pt']          = rtRow.m3_m4_PtFsr

        self.h5row['l1ID']          = 13
        self.h5row['l2ID']          = 13
        self.h5row['l3ID']          = 13
        self.h5row['l4ID']          = 13

        self.h5row["l1pt"]          = rtRow.m1Pt
        self.h5row["l2pt"]          = rtRow.m2Pt
        self.h5row["l3pt"]          = rtRow.m3Pt
        self.h5row["l4pt"]          = rtRow.m4Pt

        self.h5row["l1eta"]         = rtRow.m1Eta
        self.h5row["l2eta"]         = rtRow.m2Eta
        self.h5row["l3eta"]         = rtRow.m3Eta
        self.h5row["l4eta"]         = rtRow.m4Eta

        self.h5row["l1phi"]         = rtRow.m1Phi
        self.h5row["l2phi"]         = rtRow.m2Phi
        self.h5row["l3phi"]         = rtRow.m3Phi
        self.h5row["l4phi"]         = rtRow.m4Phi

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

        row["channel"] = "4mu"

        self.ntuple[rtRow.evt] = row
