"""
Generate datacards from HDF5 n-tuples for running hypothesis separation between
SM and JCP samples.

Author: D. Austin Belknap, UW-Madison
"""
import tables as tb
import numpy as np
from numpy import cos
import os
import sys
import logging as log

jcp_hyp = sys.argv[1]

sys.argv.append('-b-')
import ROOT as rt

NBINS = 8

NTUPLE_DIR = '../ntuples/'

CARD_DIR = './datacards/' + jcp_hyp + '/'

SM_FILE = 'SMHiggs-126.h5'

JP_FILES = {
        '0M':    'Higgs0M-126.h5',
        '0PH':   'Higgs0PH-126.h5',
        '2PM':   'Higgs2M-126.h5',
        '2PMqq': 'Higgs2Mqq-126.h5'}

QQZZ_FILES = ['ZZMMMM.h5', 'ZZEEEE.h5', 'ZZTTTT.h5',
              'ZZEEMM.h5', 'ZZEETT.h5', 'ZZMMTT.h5']

GGZZ_FILES = ['ggZZ2L2L.h5', 'ggZZ4L.h5']

DATA_FILES = ['data_2012A.h5', 'data_2012B.h5',
              'data_2012C.h5', 'data_2012D.h5']

CHANNELS = ['MMMM', 'EEEE', 'EEMM']

#CUTS = "(105.7 < mass) & (mass < 140.7)"
CUTS = "(116 < mass) & (mass < 136)"

EPSILON = 0.0000001


def P2(x):
    """Second-order legendre polynomial"""
    return 0.5*(3.0*x**2 - 1.0)


def mktemplate1D(file_name, channel, hist_name, lumi=19.712, nbins=8, isData=False):
    """Generate an unrolled 3D template

    Arguments:
    file_name -- name of the HDF5 ntuple file
    channel -- channel name (which HDF5 group?)
    hist_name -- name of the unrolled template

    Keyword arguments:
    lumi -- integrated luminosity (default 19.712)
    nbins -- number of bins to use per dimension (default 8)
    """
    log.info("Building " + file_name + " " + channel + " template")

    h5file = tb.open_file(file_name, 'r')

    if isData:
        scaling = 1
    else:
        XSEC = float(h5file.root._v_attrs.XSEC)
        NEVENTS = float(h5file.root._v_attrs.GENEVENTS)
        scaling = lumi*XSEC/NEVENTS

    table = getattr(h5file.root, channel).events

    template = rt.TH3F("template", "template",
                       nbins, -0.5, 1.0,  # P2(costheta1)
                       nbins, -0.5, 1.0,  # P2(costheta2)
                       nbins, -1.0, 1.0)  # cos(2Phi)

    event_set = set()

    for x in table.where(CUTS):
        # avoid duplicated data events
        if isData:
            if x['event'] in event_set:
                continue
            else:
                event_set.add(x['event'])

        template.Fill(P2(x['costheta1']),
                      P2(x['costheta2']),
                      cos(2.0*x['Phi']),
                      scaling)

    template_1d = rt.TH1F(hist_name, hist_name, nbins**3, 0, 1)

    for i in xrange(1, nbins+1):
        for j in xrange(1, nbins+1):
            for k in xrange(1, nbins+1):
                ind_3d = template.GetBin(k, j, i)
                ind_1d = template_1d.GetBin(k + (j-1)*nbins + (i-1)*nbins**2)
                template_1d.SetBinContent(ind_1d,
                                          EPSILON + template.GetBinContent(ind_3d))

    h5file.close()

    return (template_1d, template_1d.Integral())


def efficiency_string(process_names, chan):
    if chan == "MMMM":
        out = "CMS_eff_m lnN " + " ".join(['1.043' for x in process_names]) + '\n'
    elif chan == "EEMM":
        out =  "CMS_eff_m lnN " + " ".join(['1.015' for x in process_names]) + '\n'
        out += "CMS_eff_e lnN " + " ".join(['1.024' for x in process_names]) + '\n'
    elif chan == "EEEE":
        out = "CMS_eff_e lnN " + " ".join(['1.101' for x in process_names]) + '\n'

    return out


def mkdatacard(process_names, yields, shape_filename, channel, obs):
    log.info("Building " + channel + " datacard")
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
    out += "observation %i\n" % obs
    out += "------------\n"
    out += "## mass window [116,136]\n"
    out += "bin" + "".join([" a1" for x in process_names]) + "\n"
    out += "process" + "".join([" %s" % name for name in process_names]) + "\n"
    out += "process" + "".join([" %d" % (x-1) for x in xrange(n_proc)]) + "\n"
    out += "rate" + "".join([" %.4f" % x for x in yields]) + "\n"
    out += "------------\n"
    out += "lumi_8TeV lnN" + "".join([" 1.044" for x in xrange(n_proc)]) + "\n"

    out += "pdf_gg lnN " + " ".join(['1.0720' if x in ["sig","sig_ALT"]
                                else '1.0710' if x is "ggzz_bkg"
                                else '-' for x in process_names]) + "\n"

    out += "pdf_qqbar lnN " + " ".join(['1.0342' if x is 'qqzz_bkg'
                                   else '-' for x in process_names]) + "\n"

    out += "pdf_hz4l_accept lnN " + " ".join(['1.02' if x in ['sig','sig_ALT']
                                         else '-' for x in process_names]) + "\n"

    out += "QCDscale_ggH lnN" + "".join([" 1.0750" if x in ["sig","sig_ALT"]
                                         else " -"
                                         for x in process_names]) + "\n"

    out += "QCDscale_ggVV lnN " + " ".join(['1.2435' if x is 'ggzz_bkg'
                                           else '-' for x in process_names]) + '\n'

    out += "QCDscale_VV lnN " + " ".join(['1.0285' if x is 'qqzz_bkg'
                                         else '-' for x in process_names]) + '\n'

    out += "BRhiggs_hzz4l lnN" + "".join([" 1.02" if x in ["sig","sig_ALT"]
                                          else " -" for x in process_names]) + "\n"

    out += efficiency_string(process_names, channel)

    return out


def main():
    JP_FILE = JP_FILES[jcp_hyp]

    os.system("mkdir -p " + CARD_DIR)

    for chan in CHANNELS:
        ROOT_name = "template_8TeV_" + chan + ".root"

        sm_template = mktemplate1D(NTUPLE_DIR + SM_FILE, chan, "sig", nbins=NBINS)

        jp_template = mktemplate1D(NTUPLE_DIR + JP_FILE, chan, "sig_ALT", nbins=NBINS)

        qqzz_template = [rt.TH1F("qqzz_bkg", "qqzz_bkg", NBINS**3, 0, 1), 0]
        for QQZZ_FILE in QQZZ_FILES:
            tmp = mktemplate1D(NTUPLE_DIR + QQZZ_FILE, chan, QQZZ_FILE, nbins=NBINS)
            qqzz_template[0].Add(tmp[0])
            qqzz_template[1] += tmp[1]

        ggzz_template = [rt.TH1F("ggzz_bkg", "ggzz_bkg", NBINS**3, 0, 1), 0]
        for GGZZ_FILE in GGZZ_FILES:
            tmp = mktemplate1D(NTUPLE_DIR + GGZZ_FILE, chan, GGZZ_FILE, nbins=NBINS)
            ggzz_template[0].Add(tmp[0])
            ggzz_template[1] += tmp[1]
        
        process_names = ["sig", "sig_ALT", "qqzz_bkg", "ggzz_bkg"]
        yields = [sm_template[1], jp_template[1], qqzz_template[1], ggzz_template[1]]

        data_shape = [rt.TH1F("data_obs", "data_obs", NBINS**3, 0, 1), 0]
        for DATA_FILE in DATA_FILES:
            tmp = mktemplate1D(NTUPLE_DIR + DATA_FILE, chan, DATA_FILE, nbins=NBINS, isData=True)
            data_shape[0].Add(tmp[0])
            data_shape[1] += tmp[1]

        card_string = mkdatacard(process_names, yields, ROOT_name, chan, data_shape[1])

        with open(CARD_DIR + 'datacard_8TeV_' + chan + '.txt', 'w') as out_card:
            out_card.write(card_string)

        out_ROOT = rt.TFile(CARD_DIR + ROOT_name, "RECREATE")
        sm_template[0].Write()
        jp_template[0].Write()
        qqzz_template[0].Write()
        ggzz_template[0].Write()
        data_shape[0].Write()
        out_ROOT.Close()


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    main()
    sys.exit(0)
