#!python

import tables as tb
import numpy as np
from numpy import cos
import sys

sys.argv.append( '-b-' )
import ROOT as rt

NTUPLE = "../ntuples/ggH125.h5"

CHAN = "MMMM"

CUTS = "(105.7 < mass) & (mass < 140.7)"

NBINS = 8


def P2(x):
    return 0.5*(3.0*x**2 - 1.0)


if __name__ == "__main__":

    h5file = tb.open_file(NTUPLE, 'r')

    outfile = rt.TFile(CHAN + "_template.root", "RECREATE");

    table = getattr(h5file.root, CHAN).events

    template = rt.TH3F("template", "template",
            NBINS, -0.5, 1.0,  # P2(costheta1)
            NBINS, -0.5, 1.0,  # P2(costheta2)
            NBINS, -1.0, 1.0)  # cos(2Phi)

    for x in table.where(CUTS):
        template.Fill(P2(x['costheta1']), P2(x['costheta2']), cos(2.0*x['Phi']))

    template_1d = rt.TH1F("template_1d","template_1d", NBINS**3, 0, 1)

    for i in xrange(1, NBINS+1):
        for j in xrange(1, NBINS+1):
            for k in xrange(1, NBINS+1):
                ind_3d = template.GetBin(k, j, i)
                ind_1d = template_1d.GetBin(k + (j-1)*NBINS + (i-1)*NBINS**2)
                template_1d.SetBinContent(
                        ind_1d,
                        template.GetBinContent(ind_3d))

    template_1d.Write()

    outfile.Close()
    h5file.close()
