

import tables as tb
import numpy as np
from numpy import cos
import sys

jcp_hyp = sys.argv[1]

sys.argv.append('-b-')
import ROOT as rt


NTUPLE_DIR = '../ntuples/'

CARD_DIR = './datacards/'

SM_FILE = 'SMHiggs-126.h5'
JP_FILES = {'0M' : 'Higgs0M-126.h5'}

QQZZ_FILES = ['ZZMMMM.h5', 'ZZEEEE.h5', 'ZZTTTT.h5',
              'ZZEEMM.h5', 'ZZEETT.h5', 'ZZMMTT.h5']

GGZZ_FILES = ['ggZZ2L2L.h5', 'ggZZ4L.h5']

CHANNELS = ['MMMM', 'EEEE', 'EEMM']

CUTS = "(105.7 < mass) & (mass < 140.7)"


def P2(x):
    return 0.5*(3.0*x**2 - 1.0)


def mktemplate1D(file_name, channel, hist_name, lumi=19.712, nbins=8):
    """Generate an unrolled 3D template

    Arguments:
    file_name -- name of the HDF5 ntuple file
    channel -- channel name (which HDF5 group?)
    hist_name -- name of the unrolled template

    Keyword arguments:
    lumi -- integrated luminosity (default 19.712)
    nbins -- number of bins to use per dimension (default 8)
    """

    h5file = tb.open_file(file_name, 'r')

    XSEC = float(h5file.root._v_attrs.XSEC)
    NEVENTS = float(h5file.root._v_attrs.GENEVENTS)

    table = getattr(h5file.root, channel).events

    template = rt.TH3F("template", "template",
                       nbins, -0.5, 1.0,  # P2(costheta1)
                       nbins, -0.5, 1.0,  # P2(costheta2)
                       nbins, -1.0, 1.0)  # cos(2Phi)

    for x in table.where(CUTS):
        template.Fill(P2(x['costheta1']),
                      P2(x['costheta2']),
                      cos(2.0*x['Phi']),
                      lumi*XSEC/NEVENTS)

    template_1d = rt.TH1F(hist_name, hist_name, nbins**3, 0, 1)

    for i in xrange(1, nbins+1):
        for j in xrange(1, nbins+1):
            for k in xrange(1, nbins+1):
                ind_3d = template.GetBin(k, j, i)
                ind_1d = template_1d.GetBin(k + (j-1)*nbins + (i-1)*nbins**2)
                template_1d.SetBinContent(ind_1d,
                                          template.GetBinContent(ind_3d))

    h5file.close()

    return (template_1d, template_1d.Integral())


def mkdatacard(process_names, yields, shape_filename):
    if len(process_names) != len(yields):
        raise RuntimeError('process_names and yeilds not same length!')

    n_proc = len(process_names)

    out = "imax 1\n"
    out += "jmax %d\n" % (n_proc-1)
    out += "kmax *\n"
    out += "------------\n"
    out += "shapes * * " + shape_filename + " $PROCESS $PROCESS_$SYSTEMATIC\n"
    out += "------------\n"
    out += "bin a1\n"
    out += "observation 0\n"
    out += "------------\n"
    out += "## mass window [105.7,140.7]\n"
    out += "bin" + "".join([" a1" for x in process_names]) + "\n"
    out += "process" + "".join([" %s" % name for name in process_names]) + "\n"
    out += "process" + "".join([" %d" % (x-1) for x in xrange(n_proc)]) + "\n"
    out += "rate" + "".join([" %.4f" % x for x in yields]) + "\n"
    out += "------------\n"
    out += "lumi_8TeV lnN" + "".join([" 1.044" for x in xrange(n_proc)]) + "\n"
    out += "QCDscale_ggH lnN" + "".join([" 1.0750" if x in ["sig","sig_ALT"]
                                         else " -"
                                         for x in process_names]) + "\n"
    out += "BRhiggs_hzz4l lnN" + "".join([" 1.02" if x in ["sig","sig_ALT"]
                                          else " -" for x in process_names]) + "\n"

    return out


if __name__ == "__main__":

    JP_FILE = JP_FILES[jcp_hyp]

    for chan in CHANNELS:
        ROOT_name = "template_8TeV_" + chan + ".root"
        out_ROOT = rt.TFile(CARD_DIR + ROOT_name, "RECREATE")
        
        sm_template = mktemplate1D(NTUPLE_DIR + SM_FILE, chan, "sig")

        jp_template = mktemplate1D(NTUPLE_DIR + JP_FILE, chan, "sig_ALT")

        qqzz_template = [rt.TH1F("qqzz_bkg", "qqzz_bkg", 8**3, 0, 1), 0]
        for QQZZ_FILE in QQZZ_FILES:
            tmp = mktemplate1D(NTUPLE_DIR + QQZZ_FILE, chan, QQZZ_FILE)
            qqzz_template[0].Add(tmp[0])
            qqzz_template[1] += tmp[1]

        ggzz_template = [rt.TH1F("ggzz_bkg", "ggzz_bkg", 8**3, 0, 1), 0]
        for GGZZ_FILE in GGZZ_FILES:
            tmp = mktemplate1D(NTUPLE_DIR + GGZZ_FILE, chan, GGZZ_FILE)
            ggzz_template[0].Add(tmp[0])
            ggzz_template[1] += tmp[1]
        
        out_card = open(CARD_DIR + 'datacard_8TeV_' + chan + '.txt', 'w')

        process_names = ["sig", "sig_ALT", "qqzz_bkg", "ggzz_bkg"]
        yields = [sm_template[1], jp_template[1], qqzz_template[1], ggzz_template[1]]

        card_string = mkdatacard(process_names, yields, ROOT_name)

        out_card.write(card_string)
        out_card.close()

        data = rt.TH1F("data_obs", "data_obs", 8**3, 0, 1)

        sm_template[0].Write()
        jp_template[0].Write()
        qqzz_template[0].Write()
        ggzz_template[0].Write()
        data.Write()

        out_ROOT.Close()
