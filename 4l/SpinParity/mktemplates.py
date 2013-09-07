#!python

import tables as tb
import numpy as np
from numpy import cos
import sys

sys.argv.append( '-b-' )
import ROOT as rt

NTUPLE = "../ntuples/ggH125.h5"

CUTS = "(105.7 < mass) & (mass < 140.7)"


def P2(x):
    return 0.5*(3.0*x**2 - 1.0)


if __name__ == "__main__":

    h5file = tb.open_file(NTUPLE, 'r')

    outfile = rt.TFile("templates.root", "RECREATE");

    MMMM_table = h5file.root.MMMM.events
    EEEE_table = h5file.root.EEEE.events
    EEMM_table = h5file.root.EEMM.events

    MMMM_template = rt.TH3F("4m_template", "4m_template",
            8, -0.5, 1.0,  # P2(costheta1)
            8, -0.5, 1.0,  # P2(costheta2)
            8, -1.0, 1.0)  # cos(2Phi)

    EEEE_template = rt.TH3F(MMMM_template)
    EEEE_template.SetNameTitle("4e_template", "4e_template")
    EEMM_template = rt.TH3F(MMMM_template)
    EEMM_template.SetNameTitle("2e2m_template", "2e2m_template")

    for x in MMMM_table.where(CUTS):
        MMMM_template.Fill(
                P2(x['costheta1']),
                P2(x['costheta2']),
                cos(2.0*x['Phi']))

    for x in EEEE_table.where(CUTS):
        EEEE_template.Fill(
                P2(x['costheta1']),
                P2(x['costheta2']),
                cos(2.0*x['Phi']))

    for x in EEMM_table.where(CUTS):
        EEMM_template.Fill(
                P2(x['costheta1']),
                P2(x['costheta2']),
                cos(2.0*x['Phi']))

    EEEE_template.Write()
    MMMM_template.Write()
    EEMM_template.Write()

    outfile.Close()
    h5file.close()
