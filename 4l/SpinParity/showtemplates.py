"""Plot unrolled 3D templates with bin ordering imposed
"""
import sys

sys.argv.append('-b-')
import ROOT as rt

infile = rt.TFile(sys.argv[1],'READ')

sig_hist = infile.Get("sig")
alt_hist = infile.Get("sig_ALT")

nbins = sig_hist.GetNbinsX()

bin_vals = []

for i in xrange(1,nbins+1):
    sig_val = sig_hist.GetBinContent(sig_hist.GetBin(i))
    alt_val = alt_hist.GetBinContent(alt_hist.GetBin(i))
    bin_vals.append((sig_val,alt_val,float(sig_val)/float(alt_val)))

bin_vals.sort(key=lambda x:x[2])

out_sig = sig_hist.Clone("sig_sorted")
out_alt = alt_hist.Clone("alg_sorted")

for i in xrange(1,nbins+1):
    out_sig.SetBinContent(out_sig.GetBin(i), bin_vals[i-1][0])
    out_alt.SetBinContent(out_alt.GetBin(i), bin_vals[i-1][1])

c1 = rt.TCanvas("c1","c1",600,600)
out_sig.Draw()
out_alt.Draw("SAME")
out_alt.SetLineColor(rt.kRed)
c1.SaveAs(sys.argv[2])

infile.Close()
