import ROOT as rt
import DblHBaseSelections as selections
import MuMuMuMuTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase


class DblHAnalyzeMMMM(MegaBase):
    tree = 'mmmm/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(DblHAnalyzeMMMM, self).__init__(tree, outfile, **kwargs)
        self.tree = MuMuMuMuTree.MuMuMuMuTree(tree)
        self.out = outfile
        self.histograms = {}
        self.histo_locations = {}


    def book_histos(self, folder):
        self.book(folder, "m1Pt", "Muon Pt", 100, 0, 100)
        self.book(folder, "m2Pt", "Muon Pt", 100, 0, 100)
        self.book(folder, "m3Pt", "Muon Pt", 100, 0, 100)
        self.book(folder, "m4Pt", "Muon Pt", 100, 0, 100)


    def begin(self):
        folder = 'test'
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


    def process(self):
        for i, row in enumerate(self.tree):
            if not self.preselection(row):
                continue

            self.fill_histos(self.histograms, "test", row)


    def finish(self):
        self.write_histos()


    def preselection(self, row):
        for i in xrange(4):
            if not selections.muSelection(row, 'm' + str(i+1)):
                return False

        pts = sorted([row.m1Pt, row.m2Pt, row.m3Pt, row.m4Pt])
        if not (pts[-1] > 20.0 and pts[-2] > 10.0):
            return False

        return True
