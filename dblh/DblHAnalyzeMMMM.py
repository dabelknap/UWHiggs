import ROOT as rt
import DblHBaseSelections as selections
import MuMuMuMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

HPP_MASS = 110.0


class DblHAnalyzeMMMM(MegaBase):
    tree = 'mmmm/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(DblHAnalyzeMMMM, self).__init__(tree, outfile, **kwargs)
        self.tree = MuMuMuMuTree.MuMuMuMuTree(tree)
        self.out = outfile
        self.histograms = {}
        self.histo_locations = {}


    def book_histos(self, folder):
        self.book(folder, "MassPP", "H++ Mass", 100, 50, 150)
        self.book(folder, "MassMM", "H-- Mass", 100, 50, 150)


    def begin(self):
        folder = 'mmmm'
        self.book_histos(folder)

        for key in self.histograms:
            location, name = key.split('/')
            self.histo_locations.setdefault(location, []).append(name)


    def fill_histos(self, histos, folder_str, row, weight=None):
        for name in self.histo_locations[folder_str]:
            value = self.histograms[folder_str + '/' + name]
            if value.InheritsFrom('TH2'):
                pass
            else:
                if weight:
                    value.Fill(getattr(row, name), weight)
                else:
                    value.Fill(getattr(row, name))


    def fill_masses(self, row):
        for i in xrange(1, 4+1):
            for j in xrange(i+1, 4+1):
                pair_name = 'm' + str(i) + '_m' + str(j)
                first_name = 'm' + str(i)

                charge = getattr(row, first_name + 'Charge')
                SS = getattr(row, pair_name + '_SS')
                mass = getattr(row, pair_name + '_Mass')

                if charge > 0 and SS:
                    self.histograms['test/MassPP'].Fill(mass)
                elif charge < 0 and SS:
                    self.histograms['test/MassMM'].Fill(mass)
                else:
                    continue


    def process(self):
        for i, row in enumerate(self.tree):
            if not self.preselection(row):
                continue

            if not self.selection(row):
                continue

            self.fill_masses(row)


    def finish(self):
        self.write_histos()


    def qcdRejection(self, row):
        cut = 12.0
        for i in xrange(1, 4+1):
            for j in xrange(i+1, 4+1):
                if getattr(row, 'm' + str(i) + '_m' + str(j) + '_Mass') <= 12.0:
                    return False
        return True


    def lepIsolation(self, row):
        iso_type = 'RelPFIsoRho'
        isos = sorted([getattr(row, 'm' + str(i+1) + iso_type) for i in xrange(4)])
        iso_sum = isos[-1] + isos[-2]
        return (iso_sum < 0.35)


    def chargeRequirement(self, row):
        charges = []
        for i in xrange(4):
            charges.append(getattr(row, 'm' + str(i+1) + 'Charge'))
        return (sum(charges) == 0)


    def preselection(self, row):
        for i in xrange(4):
            if not selections.muSelection(row, 'm' + str(i+1)):
                return False

        pts = sorted([row.m1Pt, row.m2Pt, row.m3Pt, row.m4Pt])
        if not (pts[-1] > 20.0 and pts[-2] > 10.0):
            return False

        if not self.qcdRejection(row):
            return False

        if not self.lepIsolation(row):
            return False

        if not self.chargeRequirement(row):
            return False

        return True


    def zVeto(self, row):
        for i in xrange(1, 4+1):
            for j in xrange(i+1, 4+1):
                pair_name = 'm' + str(i) + '_m' + str(j)

                # OSSF leptons
                if not getattr(row, pair_name + '_SS'):
                    mass = getattr(row, pair_name + '_Mass')
                    if abs(mass - 91.2) <= 80.0:
                        return False
        return True


    def sTCut(self, row):
        pt_sum = sum([row.m1Pt, row.m2Pt, row.m3Pt, row.m4Pt])
        return (pt_sum > 0.6*HPP_MASS + 130)


    def selection(self, row):
        return self.sTCut(row)
