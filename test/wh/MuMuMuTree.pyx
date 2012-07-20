

# Load relevant ROOT C++ headers
cdef extern from "TObject.h":
    cdef cppclass TObject:
        pass

cdef extern from "TBranch.h":
    cdef cppclass TBranch:
        int GetEntry(long, int)
        void SetAddress(void*)

cdef extern from "TTree.h":
    cdef cppclass TTree:
        TTree()
        int GetEntry(long, int)
        long LoadTree(long)
        long GetEntries()
        TTree* GetTree()
        int GetTreeNumber()
        TBranch* GetBranch(char*)

cdef extern from "TFile.h":
    cdef cppclass TFile:
        TFile(char*, char*, char*, int)
        TObject* Get(char*)

# Used for filtering with a string
cdef extern from "TTreeFormula.h":
    cdef cppclass TTreeFormula:
        TTreeFormula(char*, char*, TTree*)
        double EvalInstance(int, char**)
        void UpdateFormulaLeaves()
        void SetTree(TTree*)

from cpython cimport PyCObject_AsVoidPtr

cdef class MuMuMuTree:
    # Pointers to tree (may be a chain), current active tree, and current entry
    # localentry is the entry in the current tree of the chain
    cdef TTree* tree
    cdef TTree* currentTree
    cdef int currentTreeNumber
    cdef long ientry
    cdef long localentry

    # Branches and address for all

    cdef TBranch* LT_branch
    cdef float LT_value

    cdef TBranch* Mass_branch
    cdef float Mass_value

    cdef TBranch* Pt_branch
    cdef float Pt_value

    cdef TBranch* bjetCSVVeto_branch
    cdef float bjetCSVVeto_value

    cdef TBranch* bjetVeto_branch
    cdef float bjetVeto_value

    cdef TBranch* charge_branch
    cdef float charge_value

    cdef TBranch* doubleEExtraGroup_branch
    cdef float doubleEExtraGroup_value

    cdef TBranch* doubleEExtraPass_branch
    cdef float doubleEExtraPass_value

    cdef TBranch* doubleEExtraPrescale_branch
    cdef float doubleEExtraPrescale_value

    cdef TBranch* doubleEGroup_branch
    cdef float doubleEGroup_value

    cdef TBranch* doubleEPass_branch
    cdef float doubleEPass_value

    cdef TBranch* doubleEPrescale_branch
    cdef float doubleEPrescale_value

    cdef TBranch* doubleMuGroup_branch
    cdef float doubleMuGroup_value

    cdef TBranch* doubleMuPass_branch
    cdef float doubleMuPass_value

    cdef TBranch* doubleMuPrescale_branch
    cdef float doubleMuPrescale_value

    cdef TBranch* doubleMuTrkGroup_branch
    cdef float doubleMuTrkGroup_value

    cdef TBranch* doubleMuTrkPass_branch
    cdef float doubleMuTrkPass_value

    cdef TBranch* doubleMuTrkPrescale_branch
    cdef float doubleMuTrkPrescale_value

    cdef TBranch* eVetoCicTightIso_branch
    cdef float eVetoCicTightIso_value

    cdef TBranch* eVetoMVAIso_branch
    cdef float eVetoMVAIso_value

    cdef TBranch* evt_branch
    cdef int evt_value

    cdef TBranch* isdata_branch
    cdef int isdata_value

    cdef TBranch* isoMuGroup_branch
    cdef float isoMuGroup_value

    cdef TBranch* isoMuPass_branch
    cdef float isoMuPass_value

    cdef TBranch* isoMuPrescale_branch
    cdef float isoMuPrescale_value

    cdef TBranch* jetVeto20_branch
    cdef float jetVeto20_value

    cdef TBranch* jetVeto40_branch
    cdef float jetVeto40_value

    cdef TBranch* lumi_branch
    cdef int lumi_value

    cdef TBranch* m1AbsEta_branch
    cdef float m1AbsEta_value

    cdef TBranch* m1Charge_branch
    cdef float m1Charge_value

    cdef TBranch* m1D0_branch
    cdef float m1D0_value

    cdef TBranch* m1DZ_branch
    cdef float m1DZ_value

    cdef TBranch* m1Eta_branch
    cdef float m1Eta_value

    cdef TBranch* m1GlbTrkHits_branch
    cdef float m1GlbTrkHits_value

    cdef TBranch* m1IP3DS_branch
    cdef float m1IP3DS_value

    cdef TBranch* m1IsGlobal_branch
    cdef float m1IsGlobal_value

    cdef TBranch* m1IsTracker_branch
    cdef float m1IsTracker_value

    cdef TBranch* m1JetBtag_branch
    cdef float m1JetBtag_value

    cdef TBranch* m1JetCSVBtag_branch
    cdef float m1JetCSVBtag_value

    cdef TBranch* m1JetPt_branch
    cdef float m1JetPt_value

    cdef TBranch* m1Mass_branch
    cdef float m1Mass_value

    cdef TBranch* m1MtToMET_branch
    cdef float m1MtToMET_value

    cdef TBranch* m1NormTrkChi2_branch
    cdef float m1NormTrkChi2_value

    cdef TBranch* m1PFIDTight_branch
    cdef float m1PFIDTight_value

    cdef TBranch* m1Phi_branch
    cdef float m1Phi_value

    cdef TBranch* m1PixHits_branch
    cdef float m1PixHits_value

    cdef TBranch* m1Pt_branch
    cdef float m1Pt_value

    cdef TBranch* m1PtUncorr_branch
    cdef float m1PtUncorr_value

    cdef TBranch* m1RelPFIsoDB_branch
    cdef float m1RelPFIsoDB_value

    cdef TBranch* m1VBTFID_branch
    cdef float m1VBTFID_value

    cdef TBranch* m1VZ_branch
    cdef float m1VZ_value

    cdef TBranch* m1WWID_branch
    cdef float m1WWID_value

    cdef TBranch* m1_m2_DPhi_branch
    cdef float m1_m2_DPhi_value

    cdef TBranch* m1_m2_DR_branch
    cdef float m1_m2_DR_value

    cdef TBranch* m1_m2_Mass_branch
    cdef float m1_m2_Mass_value

    cdef TBranch* m1_m2_PZeta_branch
    cdef float m1_m2_PZeta_value

    cdef TBranch* m1_m2_PZetaVis_branch
    cdef float m1_m2_PZetaVis_value

    cdef TBranch* m1_m2_Pt_branch
    cdef float m1_m2_Pt_value

    cdef TBranch* m1_m2_SS_branch
    cdef float m1_m2_SS_value

    cdef TBranch* m1_m2_Zcompat_branch
    cdef float m1_m2_Zcompat_value

    cdef TBranch* m1_m3_DPhi_branch
    cdef float m1_m3_DPhi_value

    cdef TBranch* m1_m3_DR_branch
    cdef float m1_m3_DR_value

    cdef TBranch* m1_m3_Mass_branch
    cdef float m1_m3_Mass_value

    cdef TBranch* m1_m3_PZeta_branch
    cdef float m1_m3_PZeta_value

    cdef TBranch* m1_m3_PZetaVis_branch
    cdef float m1_m3_PZetaVis_value

    cdef TBranch* m1_m3_Pt_branch
    cdef float m1_m3_Pt_value

    cdef TBranch* m1_m3_SS_branch
    cdef float m1_m3_SS_value

    cdef TBranch* m1_m3_Zcompat_branch
    cdef float m1_m3_Zcompat_value

    cdef TBranch* m2AbsEta_branch
    cdef float m2AbsEta_value

    cdef TBranch* m2Charge_branch
    cdef float m2Charge_value

    cdef TBranch* m2D0_branch
    cdef float m2D0_value

    cdef TBranch* m2DZ_branch
    cdef float m2DZ_value

    cdef TBranch* m2Eta_branch
    cdef float m2Eta_value

    cdef TBranch* m2GlbTrkHits_branch
    cdef float m2GlbTrkHits_value

    cdef TBranch* m2IP3DS_branch
    cdef float m2IP3DS_value

    cdef TBranch* m2IsGlobal_branch
    cdef float m2IsGlobal_value

    cdef TBranch* m2IsTracker_branch
    cdef float m2IsTracker_value

    cdef TBranch* m2JetBtag_branch
    cdef float m2JetBtag_value

    cdef TBranch* m2JetCSVBtag_branch
    cdef float m2JetCSVBtag_value

    cdef TBranch* m2JetPt_branch
    cdef float m2JetPt_value

    cdef TBranch* m2Mass_branch
    cdef float m2Mass_value

    cdef TBranch* m2MtToMET_branch
    cdef float m2MtToMET_value

    cdef TBranch* m2NormTrkChi2_branch
    cdef float m2NormTrkChi2_value

    cdef TBranch* m2PFIDTight_branch
    cdef float m2PFIDTight_value

    cdef TBranch* m2Phi_branch
    cdef float m2Phi_value

    cdef TBranch* m2PixHits_branch
    cdef float m2PixHits_value

    cdef TBranch* m2Pt_branch
    cdef float m2Pt_value

    cdef TBranch* m2PtUncorr_branch
    cdef float m2PtUncorr_value

    cdef TBranch* m2RelPFIsoDB_branch
    cdef float m2RelPFIsoDB_value

    cdef TBranch* m2VBTFID_branch
    cdef float m2VBTFID_value

    cdef TBranch* m2VZ_branch
    cdef float m2VZ_value

    cdef TBranch* m2WWID_branch
    cdef float m2WWID_value

    cdef TBranch* m2_m3_DPhi_branch
    cdef float m2_m3_DPhi_value

    cdef TBranch* m2_m3_DR_branch
    cdef float m2_m3_DR_value

    cdef TBranch* m2_m3_Mass_branch
    cdef float m2_m3_Mass_value

    cdef TBranch* m2_m3_PZeta_branch
    cdef float m2_m3_PZeta_value

    cdef TBranch* m2_m3_PZetaVis_branch
    cdef float m2_m3_PZetaVis_value

    cdef TBranch* m2_m3_Pt_branch
    cdef float m2_m3_Pt_value

    cdef TBranch* m2_m3_SS_branch
    cdef float m2_m3_SS_value

    cdef TBranch* m2_m3_Zcompat_branch
    cdef float m2_m3_Zcompat_value

    cdef TBranch* m3AbsEta_branch
    cdef float m3AbsEta_value

    cdef TBranch* m3Charge_branch
    cdef float m3Charge_value

    cdef TBranch* m3D0_branch
    cdef float m3D0_value

    cdef TBranch* m3DZ_branch
    cdef float m3DZ_value

    cdef TBranch* m3Eta_branch
    cdef float m3Eta_value

    cdef TBranch* m3GlbTrkHits_branch
    cdef float m3GlbTrkHits_value

    cdef TBranch* m3IP3DS_branch
    cdef float m3IP3DS_value

    cdef TBranch* m3IsGlobal_branch
    cdef float m3IsGlobal_value

    cdef TBranch* m3IsTracker_branch
    cdef float m3IsTracker_value

    cdef TBranch* m3JetBtag_branch
    cdef float m3JetBtag_value

    cdef TBranch* m3JetCSVBtag_branch
    cdef float m3JetCSVBtag_value

    cdef TBranch* m3JetPt_branch
    cdef float m3JetPt_value

    cdef TBranch* m3Mass_branch
    cdef float m3Mass_value

    cdef TBranch* m3MtToMET_branch
    cdef float m3MtToMET_value

    cdef TBranch* m3NormTrkChi2_branch
    cdef float m3NormTrkChi2_value

    cdef TBranch* m3PFIDTight_branch
    cdef float m3PFIDTight_value

    cdef TBranch* m3Phi_branch
    cdef float m3Phi_value

    cdef TBranch* m3PixHits_branch
    cdef float m3PixHits_value

    cdef TBranch* m3Pt_branch
    cdef float m3Pt_value

    cdef TBranch* m3PtUncorr_branch
    cdef float m3PtUncorr_value

    cdef TBranch* m3RelPFIsoDB_branch
    cdef float m3RelPFIsoDB_value

    cdef TBranch* m3VBTFID_branch
    cdef float m3VBTFID_value

    cdef TBranch* m3VZ_branch
    cdef float m3VZ_value

    cdef TBranch* m3WWID_branch
    cdef float m3WWID_value

    cdef TBranch* metEt_branch
    cdef float metEt_value

    cdef TBranch* metPhi_branch
    cdef float metPhi_value

    cdef TBranch* metSignificance_branch
    cdef float metSignificance_value

    cdef TBranch* mu17ele8Group_branch
    cdef float mu17ele8Group_value

    cdef TBranch* mu17ele8Pass_branch
    cdef float mu17ele8Pass_value

    cdef TBranch* mu17ele8Prescale_branch
    cdef float mu17ele8Prescale_value

    cdef TBranch* mu8ele17Group_branch
    cdef float mu8ele17Group_value

    cdef TBranch* mu8ele17Pass_branch
    cdef float mu8ele17Pass_value

    cdef TBranch* mu8ele17Prescale_branch
    cdef float mu8ele17Prescale_value

    cdef TBranch* muGlbIsoVetoPt10_branch
    cdef float muGlbIsoVetoPt10_value

    cdef TBranch* muVetoPt5_branch
    cdef float muVetoPt5_value

    cdef TBranch* nTruePU_branch
    cdef float nTruePU_value

    cdef TBranch* nvtx_branch
    cdef float nvtx_value

    cdef TBranch* processID_branch
    cdef float processID_value

    cdef TBranch* puWeightData2011AB_branch
    cdef float puWeightData2011AB_value

    cdef TBranch* puWeightData2012A_branch
    cdef float puWeightData2012A_value

    cdef TBranch* puWeightData2012AB_branch
    cdef float puWeightData2012AB_value

    cdef TBranch* rho_branch
    cdef float rho_value

    cdef TBranch* run_branch
    cdef int run_value

    cdef TBranch* singleMuGroup_branch
    cdef float singleMuGroup_value

    cdef TBranch* singleMuPass_branch
    cdef float singleMuPass_value

    cdef TBranch* singleMuPrescale_branch
    cdef float singleMuPrescale_value

    cdef TBranch* tauVetoPt20_branch
    cdef float tauVetoPt20_value

    cdef TBranch* idx_branch
    cdef int idx_value


    def __cinit__(self, ttree):
        #print "cinit"
        # Constructor from a ROOT.TTree
        from ROOT import AsCObject
        self.tree = <TTree*>PyCObject_AsVoidPtr(AsCObject(ttree))
        self.ientry = 0
        self.currentTreeNumber = -1
        #print self.tree.GetEntries()
        #self.load_entry(0)

    cdef load_entry(self, long i):
        #print "load", i
        # Load the correct tree and setup the branches
        self.localentry = self.tree.LoadTree(i)
        #print "local", self.localentry
        new_tree = self.tree.GetTree()
        #print "tree", <long>(new_tree)
        treenum = self.tree.GetTreeNumber()
        #print "num", treenum
        if treenum != self.currentTreeNumber or new_tree != self.currentTree:
            #print "New tree!"
            self.currentTree = new_tree
            self.currentTreeNumber = treenum
            self.setup_branches(new_tree)

    cdef setup_branches(self, TTree* the_tree):
        #print "setup"

        #print "making LT"
        self.LT_branch = the_tree.GetBranch("LT")
        self.LT_branch.SetAddress(<void*>&self.LT_value)

        #print "making Mass"
        self.Mass_branch = the_tree.GetBranch("Mass")
        self.Mass_branch.SetAddress(<void*>&self.Mass_value)

        #print "making Pt"
        self.Pt_branch = the_tree.GetBranch("Pt")
        self.Pt_branch.SetAddress(<void*>&self.Pt_value)

        #print "making bjetCSVVeto"
        self.bjetCSVVeto_branch = the_tree.GetBranch("bjetCSVVeto")
        self.bjetCSVVeto_branch.SetAddress(<void*>&self.bjetCSVVeto_value)

        #print "making bjetVeto"
        self.bjetVeto_branch = the_tree.GetBranch("bjetVeto")
        self.bjetVeto_branch.SetAddress(<void*>&self.bjetVeto_value)

        #print "making charge"
        self.charge_branch = the_tree.GetBranch("charge")
        self.charge_branch.SetAddress(<void*>&self.charge_value)

        #print "making doubleEExtraGroup"
        self.doubleEExtraGroup_branch = the_tree.GetBranch("doubleEExtraGroup")
        self.doubleEExtraGroup_branch.SetAddress(<void*>&self.doubleEExtraGroup_value)

        #print "making doubleEExtraPass"
        self.doubleEExtraPass_branch = the_tree.GetBranch("doubleEExtraPass")
        self.doubleEExtraPass_branch.SetAddress(<void*>&self.doubleEExtraPass_value)

        #print "making doubleEExtraPrescale"
        self.doubleEExtraPrescale_branch = the_tree.GetBranch("doubleEExtraPrescale")
        self.doubleEExtraPrescale_branch.SetAddress(<void*>&self.doubleEExtraPrescale_value)

        #print "making doubleEGroup"
        self.doubleEGroup_branch = the_tree.GetBranch("doubleEGroup")
        self.doubleEGroup_branch.SetAddress(<void*>&self.doubleEGroup_value)

        #print "making doubleEPass"
        self.doubleEPass_branch = the_tree.GetBranch("doubleEPass")
        self.doubleEPass_branch.SetAddress(<void*>&self.doubleEPass_value)

        #print "making doubleEPrescale"
        self.doubleEPrescale_branch = the_tree.GetBranch("doubleEPrescale")
        self.doubleEPrescale_branch.SetAddress(<void*>&self.doubleEPrescale_value)

        #print "making doubleMuGroup"
        self.doubleMuGroup_branch = the_tree.GetBranch("doubleMuGroup")
        self.doubleMuGroup_branch.SetAddress(<void*>&self.doubleMuGroup_value)

        #print "making doubleMuPass"
        self.doubleMuPass_branch = the_tree.GetBranch("doubleMuPass")
        self.doubleMuPass_branch.SetAddress(<void*>&self.doubleMuPass_value)

        #print "making doubleMuPrescale"
        self.doubleMuPrescale_branch = the_tree.GetBranch("doubleMuPrescale")
        self.doubleMuPrescale_branch.SetAddress(<void*>&self.doubleMuPrescale_value)

        #print "making doubleMuTrkGroup"
        self.doubleMuTrkGroup_branch = the_tree.GetBranch("doubleMuTrkGroup")
        self.doubleMuTrkGroup_branch.SetAddress(<void*>&self.doubleMuTrkGroup_value)

        #print "making doubleMuTrkPass"
        self.doubleMuTrkPass_branch = the_tree.GetBranch("doubleMuTrkPass")
        self.doubleMuTrkPass_branch.SetAddress(<void*>&self.doubleMuTrkPass_value)

        #print "making doubleMuTrkPrescale"
        self.doubleMuTrkPrescale_branch = the_tree.GetBranch("doubleMuTrkPrescale")
        self.doubleMuTrkPrescale_branch.SetAddress(<void*>&self.doubleMuTrkPrescale_value)

        #print "making eVetoCicTightIso"
        self.eVetoCicTightIso_branch = the_tree.GetBranch("eVetoCicTightIso")
        self.eVetoCicTightIso_branch.SetAddress(<void*>&self.eVetoCicTightIso_value)

        #print "making eVetoMVAIso"
        self.eVetoMVAIso_branch = the_tree.GetBranch("eVetoMVAIso")
        self.eVetoMVAIso_branch.SetAddress(<void*>&self.eVetoMVAIso_value)

        #print "making evt"
        self.evt_branch = the_tree.GetBranch("evt")
        self.evt_branch.SetAddress(<void*>&self.evt_value)

        #print "making isdata"
        self.isdata_branch = the_tree.GetBranch("isdata")
        self.isdata_branch.SetAddress(<void*>&self.isdata_value)

        #print "making isoMuGroup"
        self.isoMuGroup_branch = the_tree.GetBranch("isoMuGroup")
        self.isoMuGroup_branch.SetAddress(<void*>&self.isoMuGroup_value)

        #print "making isoMuPass"
        self.isoMuPass_branch = the_tree.GetBranch("isoMuPass")
        self.isoMuPass_branch.SetAddress(<void*>&self.isoMuPass_value)

        #print "making isoMuPrescale"
        self.isoMuPrescale_branch = the_tree.GetBranch("isoMuPrescale")
        self.isoMuPrescale_branch.SetAddress(<void*>&self.isoMuPrescale_value)

        #print "making jetVeto20"
        self.jetVeto20_branch = the_tree.GetBranch("jetVeto20")
        self.jetVeto20_branch.SetAddress(<void*>&self.jetVeto20_value)

        #print "making jetVeto40"
        self.jetVeto40_branch = the_tree.GetBranch("jetVeto40")
        self.jetVeto40_branch.SetAddress(<void*>&self.jetVeto40_value)

        #print "making lumi"
        self.lumi_branch = the_tree.GetBranch("lumi")
        self.lumi_branch.SetAddress(<void*>&self.lumi_value)

        #print "making m1AbsEta"
        self.m1AbsEta_branch = the_tree.GetBranch("m1AbsEta")
        self.m1AbsEta_branch.SetAddress(<void*>&self.m1AbsEta_value)

        #print "making m1Charge"
        self.m1Charge_branch = the_tree.GetBranch("m1Charge")
        self.m1Charge_branch.SetAddress(<void*>&self.m1Charge_value)

        #print "making m1D0"
        self.m1D0_branch = the_tree.GetBranch("m1D0")
        self.m1D0_branch.SetAddress(<void*>&self.m1D0_value)

        #print "making m1DZ"
        self.m1DZ_branch = the_tree.GetBranch("m1DZ")
        self.m1DZ_branch.SetAddress(<void*>&self.m1DZ_value)

        #print "making m1Eta"
        self.m1Eta_branch = the_tree.GetBranch("m1Eta")
        self.m1Eta_branch.SetAddress(<void*>&self.m1Eta_value)

        #print "making m1GlbTrkHits"
        self.m1GlbTrkHits_branch = the_tree.GetBranch("m1GlbTrkHits")
        self.m1GlbTrkHits_branch.SetAddress(<void*>&self.m1GlbTrkHits_value)

        #print "making m1IP3DS"
        self.m1IP3DS_branch = the_tree.GetBranch("m1IP3DS")
        self.m1IP3DS_branch.SetAddress(<void*>&self.m1IP3DS_value)

        #print "making m1IsGlobal"
        self.m1IsGlobal_branch = the_tree.GetBranch("m1IsGlobal")
        self.m1IsGlobal_branch.SetAddress(<void*>&self.m1IsGlobal_value)

        #print "making m1IsTracker"
        self.m1IsTracker_branch = the_tree.GetBranch("m1IsTracker")
        self.m1IsTracker_branch.SetAddress(<void*>&self.m1IsTracker_value)

        #print "making m1JetBtag"
        self.m1JetBtag_branch = the_tree.GetBranch("m1JetBtag")
        self.m1JetBtag_branch.SetAddress(<void*>&self.m1JetBtag_value)

        #print "making m1JetCSVBtag"
        self.m1JetCSVBtag_branch = the_tree.GetBranch("m1JetCSVBtag")
        self.m1JetCSVBtag_branch.SetAddress(<void*>&self.m1JetCSVBtag_value)

        #print "making m1JetPt"
        self.m1JetPt_branch = the_tree.GetBranch("m1JetPt")
        self.m1JetPt_branch.SetAddress(<void*>&self.m1JetPt_value)

        #print "making m1Mass"
        self.m1Mass_branch = the_tree.GetBranch("m1Mass")
        self.m1Mass_branch.SetAddress(<void*>&self.m1Mass_value)

        #print "making m1MtToMET"
        self.m1MtToMET_branch = the_tree.GetBranch("m1MtToMET")
        self.m1MtToMET_branch.SetAddress(<void*>&self.m1MtToMET_value)

        #print "making m1NormTrkChi2"
        self.m1NormTrkChi2_branch = the_tree.GetBranch("m1NormTrkChi2")
        self.m1NormTrkChi2_branch.SetAddress(<void*>&self.m1NormTrkChi2_value)

        #print "making m1PFIDTight"
        self.m1PFIDTight_branch = the_tree.GetBranch("m1PFIDTight")
        self.m1PFIDTight_branch.SetAddress(<void*>&self.m1PFIDTight_value)

        #print "making m1Phi"
        self.m1Phi_branch = the_tree.GetBranch("m1Phi")
        self.m1Phi_branch.SetAddress(<void*>&self.m1Phi_value)

        #print "making m1PixHits"
        self.m1PixHits_branch = the_tree.GetBranch("m1PixHits")
        self.m1PixHits_branch.SetAddress(<void*>&self.m1PixHits_value)

        #print "making m1Pt"
        self.m1Pt_branch = the_tree.GetBranch("m1Pt")
        self.m1Pt_branch.SetAddress(<void*>&self.m1Pt_value)

        #print "making m1PtUncorr"
        self.m1PtUncorr_branch = the_tree.GetBranch("m1PtUncorr")
        self.m1PtUncorr_branch.SetAddress(<void*>&self.m1PtUncorr_value)

        #print "making m1RelPFIsoDB"
        self.m1RelPFIsoDB_branch = the_tree.GetBranch("m1RelPFIsoDB")
        self.m1RelPFIsoDB_branch.SetAddress(<void*>&self.m1RelPFIsoDB_value)

        #print "making m1VBTFID"
        self.m1VBTFID_branch = the_tree.GetBranch("m1VBTFID")
        self.m1VBTFID_branch.SetAddress(<void*>&self.m1VBTFID_value)

        #print "making m1VZ"
        self.m1VZ_branch = the_tree.GetBranch("m1VZ")
        self.m1VZ_branch.SetAddress(<void*>&self.m1VZ_value)

        #print "making m1WWID"
        self.m1WWID_branch = the_tree.GetBranch("m1WWID")
        self.m1WWID_branch.SetAddress(<void*>&self.m1WWID_value)

        #print "making m1_m2_DPhi"
        self.m1_m2_DPhi_branch = the_tree.GetBranch("m1_m2_DPhi")
        self.m1_m2_DPhi_branch.SetAddress(<void*>&self.m1_m2_DPhi_value)

        #print "making m1_m2_DR"
        self.m1_m2_DR_branch = the_tree.GetBranch("m1_m2_DR")
        self.m1_m2_DR_branch.SetAddress(<void*>&self.m1_m2_DR_value)

        #print "making m1_m2_Mass"
        self.m1_m2_Mass_branch = the_tree.GetBranch("m1_m2_Mass")
        self.m1_m2_Mass_branch.SetAddress(<void*>&self.m1_m2_Mass_value)

        #print "making m1_m2_PZeta"
        self.m1_m2_PZeta_branch = the_tree.GetBranch("m1_m2_PZeta")
        self.m1_m2_PZeta_branch.SetAddress(<void*>&self.m1_m2_PZeta_value)

        #print "making m1_m2_PZetaVis"
        self.m1_m2_PZetaVis_branch = the_tree.GetBranch("m1_m2_PZetaVis")
        self.m1_m2_PZetaVis_branch.SetAddress(<void*>&self.m1_m2_PZetaVis_value)

        #print "making m1_m2_Pt"
        self.m1_m2_Pt_branch = the_tree.GetBranch("m1_m2_Pt")
        self.m1_m2_Pt_branch.SetAddress(<void*>&self.m1_m2_Pt_value)

        #print "making m1_m2_SS"
        self.m1_m2_SS_branch = the_tree.GetBranch("m1_m2_SS")
        self.m1_m2_SS_branch.SetAddress(<void*>&self.m1_m2_SS_value)

        #print "making m1_m2_Zcompat"
        self.m1_m2_Zcompat_branch = the_tree.GetBranch("m1_m2_Zcompat")
        self.m1_m2_Zcompat_branch.SetAddress(<void*>&self.m1_m2_Zcompat_value)

        #print "making m1_m3_DPhi"
        self.m1_m3_DPhi_branch = the_tree.GetBranch("m1_m3_DPhi")
        self.m1_m3_DPhi_branch.SetAddress(<void*>&self.m1_m3_DPhi_value)

        #print "making m1_m3_DR"
        self.m1_m3_DR_branch = the_tree.GetBranch("m1_m3_DR")
        self.m1_m3_DR_branch.SetAddress(<void*>&self.m1_m3_DR_value)

        #print "making m1_m3_Mass"
        self.m1_m3_Mass_branch = the_tree.GetBranch("m1_m3_Mass")
        self.m1_m3_Mass_branch.SetAddress(<void*>&self.m1_m3_Mass_value)

        #print "making m1_m3_PZeta"
        self.m1_m3_PZeta_branch = the_tree.GetBranch("m1_m3_PZeta")
        self.m1_m3_PZeta_branch.SetAddress(<void*>&self.m1_m3_PZeta_value)

        #print "making m1_m3_PZetaVis"
        self.m1_m3_PZetaVis_branch = the_tree.GetBranch("m1_m3_PZetaVis")
        self.m1_m3_PZetaVis_branch.SetAddress(<void*>&self.m1_m3_PZetaVis_value)

        #print "making m1_m3_Pt"
        self.m1_m3_Pt_branch = the_tree.GetBranch("m1_m3_Pt")
        self.m1_m3_Pt_branch.SetAddress(<void*>&self.m1_m3_Pt_value)

        #print "making m1_m3_SS"
        self.m1_m3_SS_branch = the_tree.GetBranch("m1_m3_SS")
        self.m1_m3_SS_branch.SetAddress(<void*>&self.m1_m3_SS_value)

        #print "making m1_m3_Zcompat"
        self.m1_m3_Zcompat_branch = the_tree.GetBranch("m1_m3_Zcompat")
        self.m1_m3_Zcompat_branch.SetAddress(<void*>&self.m1_m3_Zcompat_value)

        #print "making m2AbsEta"
        self.m2AbsEta_branch = the_tree.GetBranch("m2AbsEta")
        self.m2AbsEta_branch.SetAddress(<void*>&self.m2AbsEta_value)

        #print "making m2Charge"
        self.m2Charge_branch = the_tree.GetBranch("m2Charge")
        self.m2Charge_branch.SetAddress(<void*>&self.m2Charge_value)

        #print "making m2D0"
        self.m2D0_branch = the_tree.GetBranch("m2D0")
        self.m2D0_branch.SetAddress(<void*>&self.m2D0_value)

        #print "making m2DZ"
        self.m2DZ_branch = the_tree.GetBranch("m2DZ")
        self.m2DZ_branch.SetAddress(<void*>&self.m2DZ_value)

        #print "making m2Eta"
        self.m2Eta_branch = the_tree.GetBranch("m2Eta")
        self.m2Eta_branch.SetAddress(<void*>&self.m2Eta_value)

        #print "making m2GlbTrkHits"
        self.m2GlbTrkHits_branch = the_tree.GetBranch("m2GlbTrkHits")
        self.m2GlbTrkHits_branch.SetAddress(<void*>&self.m2GlbTrkHits_value)

        #print "making m2IP3DS"
        self.m2IP3DS_branch = the_tree.GetBranch("m2IP3DS")
        self.m2IP3DS_branch.SetAddress(<void*>&self.m2IP3DS_value)

        #print "making m2IsGlobal"
        self.m2IsGlobal_branch = the_tree.GetBranch("m2IsGlobal")
        self.m2IsGlobal_branch.SetAddress(<void*>&self.m2IsGlobal_value)

        #print "making m2IsTracker"
        self.m2IsTracker_branch = the_tree.GetBranch("m2IsTracker")
        self.m2IsTracker_branch.SetAddress(<void*>&self.m2IsTracker_value)

        #print "making m2JetBtag"
        self.m2JetBtag_branch = the_tree.GetBranch("m2JetBtag")
        self.m2JetBtag_branch.SetAddress(<void*>&self.m2JetBtag_value)

        #print "making m2JetCSVBtag"
        self.m2JetCSVBtag_branch = the_tree.GetBranch("m2JetCSVBtag")
        self.m2JetCSVBtag_branch.SetAddress(<void*>&self.m2JetCSVBtag_value)

        #print "making m2JetPt"
        self.m2JetPt_branch = the_tree.GetBranch("m2JetPt")
        self.m2JetPt_branch.SetAddress(<void*>&self.m2JetPt_value)

        #print "making m2Mass"
        self.m2Mass_branch = the_tree.GetBranch("m2Mass")
        self.m2Mass_branch.SetAddress(<void*>&self.m2Mass_value)

        #print "making m2MtToMET"
        self.m2MtToMET_branch = the_tree.GetBranch("m2MtToMET")
        self.m2MtToMET_branch.SetAddress(<void*>&self.m2MtToMET_value)

        #print "making m2NormTrkChi2"
        self.m2NormTrkChi2_branch = the_tree.GetBranch("m2NormTrkChi2")
        self.m2NormTrkChi2_branch.SetAddress(<void*>&self.m2NormTrkChi2_value)

        #print "making m2PFIDTight"
        self.m2PFIDTight_branch = the_tree.GetBranch("m2PFIDTight")
        self.m2PFIDTight_branch.SetAddress(<void*>&self.m2PFIDTight_value)

        #print "making m2Phi"
        self.m2Phi_branch = the_tree.GetBranch("m2Phi")
        self.m2Phi_branch.SetAddress(<void*>&self.m2Phi_value)

        #print "making m2PixHits"
        self.m2PixHits_branch = the_tree.GetBranch("m2PixHits")
        self.m2PixHits_branch.SetAddress(<void*>&self.m2PixHits_value)

        #print "making m2Pt"
        self.m2Pt_branch = the_tree.GetBranch("m2Pt")
        self.m2Pt_branch.SetAddress(<void*>&self.m2Pt_value)

        #print "making m2PtUncorr"
        self.m2PtUncorr_branch = the_tree.GetBranch("m2PtUncorr")
        self.m2PtUncorr_branch.SetAddress(<void*>&self.m2PtUncorr_value)

        #print "making m2RelPFIsoDB"
        self.m2RelPFIsoDB_branch = the_tree.GetBranch("m2RelPFIsoDB")
        self.m2RelPFIsoDB_branch.SetAddress(<void*>&self.m2RelPFIsoDB_value)

        #print "making m2VBTFID"
        self.m2VBTFID_branch = the_tree.GetBranch("m2VBTFID")
        self.m2VBTFID_branch.SetAddress(<void*>&self.m2VBTFID_value)

        #print "making m2VZ"
        self.m2VZ_branch = the_tree.GetBranch("m2VZ")
        self.m2VZ_branch.SetAddress(<void*>&self.m2VZ_value)

        #print "making m2WWID"
        self.m2WWID_branch = the_tree.GetBranch("m2WWID")
        self.m2WWID_branch.SetAddress(<void*>&self.m2WWID_value)

        #print "making m2_m3_DPhi"
        self.m2_m3_DPhi_branch = the_tree.GetBranch("m2_m3_DPhi")
        self.m2_m3_DPhi_branch.SetAddress(<void*>&self.m2_m3_DPhi_value)

        #print "making m2_m3_DR"
        self.m2_m3_DR_branch = the_tree.GetBranch("m2_m3_DR")
        self.m2_m3_DR_branch.SetAddress(<void*>&self.m2_m3_DR_value)

        #print "making m2_m3_Mass"
        self.m2_m3_Mass_branch = the_tree.GetBranch("m2_m3_Mass")
        self.m2_m3_Mass_branch.SetAddress(<void*>&self.m2_m3_Mass_value)

        #print "making m2_m3_PZeta"
        self.m2_m3_PZeta_branch = the_tree.GetBranch("m2_m3_PZeta")
        self.m2_m3_PZeta_branch.SetAddress(<void*>&self.m2_m3_PZeta_value)

        #print "making m2_m3_PZetaVis"
        self.m2_m3_PZetaVis_branch = the_tree.GetBranch("m2_m3_PZetaVis")
        self.m2_m3_PZetaVis_branch.SetAddress(<void*>&self.m2_m3_PZetaVis_value)

        #print "making m2_m3_Pt"
        self.m2_m3_Pt_branch = the_tree.GetBranch("m2_m3_Pt")
        self.m2_m3_Pt_branch.SetAddress(<void*>&self.m2_m3_Pt_value)

        #print "making m2_m3_SS"
        self.m2_m3_SS_branch = the_tree.GetBranch("m2_m3_SS")
        self.m2_m3_SS_branch.SetAddress(<void*>&self.m2_m3_SS_value)

        #print "making m2_m3_Zcompat"
        self.m2_m3_Zcompat_branch = the_tree.GetBranch("m2_m3_Zcompat")
        self.m2_m3_Zcompat_branch.SetAddress(<void*>&self.m2_m3_Zcompat_value)

        #print "making m3AbsEta"
        self.m3AbsEta_branch = the_tree.GetBranch("m3AbsEta")
        self.m3AbsEta_branch.SetAddress(<void*>&self.m3AbsEta_value)

        #print "making m3Charge"
        self.m3Charge_branch = the_tree.GetBranch("m3Charge")
        self.m3Charge_branch.SetAddress(<void*>&self.m3Charge_value)

        #print "making m3D0"
        self.m3D0_branch = the_tree.GetBranch("m3D0")
        self.m3D0_branch.SetAddress(<void*>&self.m3D0_value)

        #print "making m3DZ"
        self.m3DZ_branch = the_tree.GetBranch("m3DZ")
        self.m3DZ_branch.SetAddress(<void*>&self.m3DZ_value)

        #print "making m3Eta"
        self.m3Eta_branch = the_tree.GetBranch("m3Eta")
        self.m3Eta_branch.SetAddress(<void*>&self.m3Eta_value)

        #print "making m3GlbTrkHits"
        self.m3GlbTrkHits_branch = the_tree.GetBranch("m3GlbTrkHits")
        self.m3GlbTrkHits_branch.SetAddress(<void*>&self.m3GlbTrkHits_value)

        #print "making m3IP3DS"
        self.m3IP3DS_branch = the_tree.GetBranch("m3IP3DS")
        self.m3IP3DS_branch.SetAddress(<void*>&self.m3IP3DS_value)

        #print "making m3IsGlobal"
        self.m3IsGlobal_branch = the_tree.GetBranch("m3IsGlobal")
        self.m3IsGlobal_branch.SetAddress(<void*>&self.m3IsGlobal_value)

        #print "making m3IsTracker"
        self.m3IsTracker_branch = the_tree.GetBranch("m3IsTracker")
        self.m3IsTracker_branch.SetAddress(<void*>&self.m3IsTracker_value)

        #print "making m3JetBtag"
        self.m3JetBtag_branch = the_tree.GetBranch("m3JetBtag")
        self.m3JetBtag_branch.SetAddress(<void*>&self.m3JetBtag_value)

        #print "making m3JetCSVBtag"
        self.m3JetCSVBtag_branch = the_tree.GetBranch("m3JetCSVBtag")
        self.m3JetCSVBtag_branch.SetAddress(<void*>&self.m3JetCSVBtag_value)

        #print "making m3JetPt"
        self.m3JetPt_branch = the_tree.GetBranch("m3JetPt")
        self.m3JetPt_branch.SetAddress(<void*>&self.m3JetPt_value)

        #print "making m3Mass"
        self.m3Mass_branch = the_tree.GetBranch("m3Mass")
        self.m3Mass_branch.SetAddress(<void*>&self.m3Mass_value)

        #print "making m3MtToMET"
        self.m3MtToMET_branch = the_tree.GetBranch("m3MtToMET")
        self.m3MtToMET_branch.SetAddress(<void*>&self.m3MtToMET_value)

        #print "making m3NormTrkChi2"
        self.m3NormTrkChi2_branch = the_tree.GetBranch("m3NormTrkChi2")
        self.m3NormTrkChi2_branch.SetAddress(<void*>&self.m3NormTrkChi2_value)

        #print "making m3PFIDTight"
        self.m3PFIDTight_branch = the_tree.GetBranch("m3PFIDTight")
        self.m3PFIDTight_branch.SetAddress(<void*>&self.m3PFIDTight_value)

        #print "making m3Phi"
        self.m3Phi_branch = the_tree.GetBranch("m3Phi")
        self.m3Phi_branch.SetAddress(<void*>&self.m3Phi_value)

        #print "making m3PixHits"
        self.m3PixHits_branch = the_tree.GetBranch("m3PixHits")
        self.m3PixHits_branch.SetAddress(<void*>&self.m3PixHits_value)

        #print "making m3Pt"
        self.m3Pt_branch = the_tree.GetBranch("m3Pt")
        self.m3Pt_branch.SetAddress(<void*>&self.m3Pt_value)

        #print "making m3PtUncorr"
        self.m3PtUncorr_branch = the_tree.GetBranch("m3PtUncorr")
        self.m3PtUncorr_branch.SetAddress(<void*>&self.m3PtUncorr_value)

        #print "making m3RelPFIsoDB"
        self.m3RelPFIsoDB_branch = the_tree.GetBranch("m3RelPFIsoDB")
        self.m3RelPFIsoDB_branch.SetAddress(<void*>&self.m3RelPFIsoDB_value)

        #print "making m3VBTFID"
        self.m3VBTFID_branch = the_tree.GetBranch("m3VBTFID")
        self.m3VBTFID_branch.SetAddress(<void*>&self.m3VBTFID_value)

        #print "making m3VZ"
        self.m3VZ_branch = the_tree.GetBranch("m3VZ")
        self.m3VZ_branch.SetAddress(<void*>&self.m3VZ_value)

        #print "making m3WWID"
        self.m3WWID_branch = the_tree.GetBranch("m3WWID")
        self.m3WWID_branch.SetAddress(<void*>&self.m3WWID_value)

        #print "making metEt"
        self.metEt_branch = the_tree.GetBranch("metEt")
        self.metEt_branch.SetAddress(<void*>&self.metEt_value)

        #print "making metPhi"
        self.metPhi_branch = the_tree.GetBranch("metPhi")
        self.metPhi_branch.SetAddress(<void*>&self.metPhi_value)

        #print "making metSignificance"
        self.metSignificance_branch = the_tree.GetBranch("metSignificance")
        self.metSignificance_branch.SetAddress(<void*>&self.metSignificance_value)

        #print "making mu17ele8Group"
        self.mu17ele8Group_branch = the_tree.GetBranch("mu17ele8Group")
        self.mu17ele8Group_branch.SetAddress(<void*>&self.mu17ele8Group_value)

        #print "making mu17ele8Pass"
        self.mu17ele8Pass_branch = the_tree.GetBranch("mu17ele8Pass")
        self.mu17ele8Pass_branch.SetAddress(<void*>&self.mu17ele8Pass_value)

        #print "making mu17ele8Prescale"
        self.mu17ele8Prescale_branch = the_tree.GetBranch("mu17ele8Prescale")
        self.mu17ele8Prescale_branch.SetAddress(<void*>&self.mu17ele8Prescale_value)

        #print "making mu8ele17Group"
        self.mu8ele17Group_branch = the_tree.GetBranch("mu8ele17Group")
        self.mu8ele17Group_branch.SetAddress(<void*>&self.mu8ele17Group_value)

        #print "making mu8ele17Pass"
        self.mu8ele17Pass_branch = the_tree.GetBranch("mu8ele17Pass")
        self.mu8ele17Pass_branch.SetAddress(<void*>&self.mu8ele17Pass_value)

        #print "making mu8ele17Prescale"
        self.mu8ele17Prescale_branch = the_tree.GetBranch("mu8ele17Prescale")
        self.mu8ele17Prescale_branch.SetAddress(<void*>&self.mu8ele17Prescale_value)

        #print "making muGlbIsoVetoPt10"
        self.muGlbIsoVetoPt10_branch = the_tree.GetBranch("muGlbIsoVetoPt10")
        self.muGlbIsoVetoPt10_branch.SetAddress(<void*>&self.muGlbIsoVetoPt10_value)

        #print "making muVetoPt5"
        self.muVetoPt5_branch = the_tree.GetBranch("muVetoPt5")
        self.muVetoPt5_branch.SetAddress(<void*>&self.muVetoPt5_value)

        #print "making nTruePU"
        self.nTruePU_branch = the_tree.GetBranch("nTruePU")
        self.nTruePU_branch.SetAddress(<void*>&self.nTruePU_value)

        #print "making nvtx"
        self.nvtx_branch = the_tree.GetBranch("nvtx")
        self.nvtx_branch.SetAddress(<void*>&self.nvtx_value)

        #print "making processID"
        self.processID_branch = the_tree.GetBranch("processID")
        self.processID_branch.SetAddress(<void*>&self.processID_value)

        #print "making puWeightData2011AB"
        self.puWeightData2011AB_branch = the_tree.GetBranch("puWeightData2011AB")
        self.puWeightData2011AB_branch.SetAddress(<void*>&self.puWeightData2011AB_value)

        #print "making puWeightData2012A"
        self.puWeightData2012A_branch = the_tree.GetBranch("puWeightData2012A")
        self.puWeightData2012A_branch.SetAddress(<void*>&self.puWeightData2012A_value)

        #print "making puWeightData2012AB"
        self.puWeightData2012AB_branch = the_tree.GetBranch("puWeightData2012AB")
        self.puWeightData2012AB_branch.SetAddress(<void*>&self.puWeightData2012AB_value)

        #print "making rho"
        self.rho_branch = the_tree.GetBranch("rho")
        self.rho_branch.SetAddress(<void*>&self.rho_value)

        #print "making run"
        self.run_branch = the_tree.GetBranch("run")
        self.run_branch.SetAddress(<void*>&self.run_value)

        #print "making singleMuGroup"
        self.singleMuGroup_branch = the_tree.GetBranch("singleMuGroup")
        self.singleMuGroup_branch.SetAddress(<void*>&self.singleMuGroup_value)

        #print "making singleMuPass"
        self.singleMuPass_branch = the_tree.GetBranch("singleMuPass")
        self.singleMuPass_branch.SetAddress(<void*>&self.singleMuPass_value)

        #print "making singleMuPrescale"
        self.singleMuPrescale_branch = the_tree.GetBranch("singleMuPrescale")
        self.singleMuPrescale_branch.SetAddress(<void*>&self.singleMuPrescale_value)

        #print "making tauVetoPt20"
        self.tauVetoPt20_branch = the_tree.GetBranch("tauVetoPt20")
        self.tauVetoPt20_branch.SetAddress(<void*>&self.tauVetoPt20_value)

        #print "making idx"
        self.idx_branch = the_tree.GetBranch("idx")
        self.idx_branch.SetAddress(<void*>&self.idx_value)


    # Iterating over the tree
    def __iter__(self):
        self.ientry = 0
        while self.ientry < self.tree.GetEntries():
            self.load_entry(self.ientry)
            yield self
            self.ientry += 1

    # Iterate over rows which pass the filter
    def where(self, filter):
        print "where"
        cdef TTreeFormula* formula = new TTreeFormula(
            "cyiter", filter, self.tree)
        self.ientry = 0
        cdef TTree* currentTree = self.tree.GetTree()
        while self.ientry < self.tree.GetEntries():
            self.tree.LoadTree(self.ientry)
            if currentTree != self.tree.GetTree():
                currentTree = self.tree.GetTree()
                formula.SetTree(currentTree)
                formula.UpdateFormulaLeaves()
            if formula.EvalInstance(0, NULL):
                yield self
            self.ientry += 1
        del formula

    # Getting/setting the Tree entry number
    property entry:
        def __get__(self):
            return self.ientry
        def __set__(self, int i):
            print i
            self.ientry = i
            self.load_entry(i)

    # Access to the current branch values

    property LT:
        def __get__(self):
            self.LT_branch.GetEntry(self.localentry, 0)
            return self.LT_value

    property Mass:
        def __get__(self):
            self.Mass_branch.GetEntry(self.localentry, 0)
            return self.Mass_value

    property Pt:
        def __get__(self):
            self.Pt_branch.GetEntry(self.localentry, 0)
            return self.Pt_value

    property bjetCSVVeto:
        def __get__(self):
            self.bjetCSVVeto_branch.GetEntry(self.localentry, 0)
            return self.bjetCSVVeto_value

    property bjetVeto:
        def __get__(self):
            self.bjetVeto_branch.GetEntry(self.localentry, 0)
            return self.bjetVeto_value

    property charge:
        def __get__(self):
            self.charge_branch.GetEntry(self.localentry, 0)
            return self.charge_value

    property doubleEExtraGroup:
        def __get__(self):
            self.doubleEExtraGroup_branch.GetEntry(self.localentry, 0)
            return self.doubleEExtraGroup_value

    property doubleEExtraPass:
        def __get__(self):
            self.doubleEExtraPass_branch.GetEntry(self.localentry, 0)
            return self.doubleEExtraPass_value

    property doubleEExtraPrescale:
        def __get__(self):
            self.doubleEExtraPrescale_branch.GetEntry(self.localentry, 0)
            return self.doubleEExtraPrescale_value

    property doubleEGroup:
        def __get__(self):
            self.doubleEGroup_branch.GetEntry(self.localentry, 0)
            return self.doubleEGroup_value

    property doubleEPass:
        def __get__(self):
            self.doubleEPass_branch.GetEntry(self.localentry, 0)
            return self.doubleEPass_value

    property doubleEPrescale:
        def __get__(self):
            self.doubleEPrescale_branch.GetEntry(self.localentry, 0)
            return self.doubleEPrescale_value

    property doubleMuGroup:
        def __get__(self):
            self.doubleMuGroup_branch.GetEntry(self.localentry, 0)
            return self.doubleMuGroup_value

    property doubleMuPass:
        def __get__(self):
            self.doubleMuPass_branch.GetEntry(self.localentry, 0)
            return self.doubleMuPass_value

    property doubleMuPrescale:
        def __get__(self):
            self.doubleMuPrescale_branch.GetEntry(self.localentry, 0)
            return self.doubleMuPrescale_value

    property doubleMuTrkGroup:
        def __get__(self):
            self.doubleMuTrkGroup_branch.GetEntry(self.localentry, 0)
            return self.doubleMuTrkGroup_value

    property doubleMuTrkPass:
        def __get__(self):
            self.doubleMuTrkPass_branch.GetEntry(self.localentry, 0)
            return self.doubleMuTrkPass_value

    property doubleMuTrkPrescale:
        def __get__(self):
            self.doubleMuTrkPrescale_branch.GetEntry(self.localentry, 0)
            return self.doubleMuTrkPrescale_value

    property eVetoCicTightIso:
        def __get__(self):
            self.eVetoCicTightIso_branch.GetEntry(self.localentry, 0)
            return self.eVetoCicTightIso_value

    property eVetoMVAIso:
        def __get__(self):
            self.eVetoMVAIso_branch.GetEntry(self.localentry, 0)
            return self.eVetoMVAIso_value

    property evt:
        def __get__(self):
            self.evt_branch.GetEntry(self.localentry, 0)
            return self.evt_value

    property isdata:
        def __get__(self):
            self.isdata_branch.GetEntry(self.localentry, 0)
            return self.isdata_value

    property isoMuGroup:
        def __get__(self):
            self.isoMuGroup_branch.GetEntry(self.localentry, 0)
            return self.isoMuGroup_value

    property isoMuPass:
        def __get__(self):
            self.isoMuPass_branch.GetEntry(self.localentry, 0)
            return self.isoMuPass_value

    property isoMuPrescale:
        def __get__(self):
            self.isoMuPrescale_branch.GetEntry(self.localentry, 0)
            return self.isoMuPrescale_value

    property jetVeto20:
        def __get__(self):
            self.jetVeto20_branch.GetEntry(self.localentry, 0)
            return self.jetVeto20_value

    property jetVeto40:
        def __get__(self):
            self.jetVeto40_branch.GetEntry(self.localentry, 0)
            return self.jetVeto40_value

    property lumi:
        def __get__(self):
            self.lumi_branch.GetEntry(self.localentry, 0)
            return self.lumi_value

    property m1AbsEta:
        def __get__(self):
            self.m1AbsEta_branch.GetEntry(self.localentry, 0)
            return self.m1AbsEta_value

    property m1Charge:
        def __get__(self):
            self.m1Charge_branch.GetEntry(self.localentry, 0)
            return self.m1Charge_value

    property m1D0:
        def __get__(self):
            self.m1D0_branch.GetEntry(self.localentry, 0)
            return self.m1D0_value

    property m1DZ:
        def __get__(self):
            self.m1DZ_branch.GetEntry(self.localentry, 0)
            return self.m1DZ_value

    property m1Eta:
        def __get__(self):
            self.m1Eta_branch.GetEntry(self.localentry, 0)
            return self.m1Eta_value

    property m1GlbTrkHits:
        def __get__(self):
            self.m1GlbTrkHits_branch.GetEntry(self.localentry, 0)
            return self.m1GlbTrkHits_value

    property m1IP3DS:
        def __get__(self):
            self.m1IP3DS_branch.GetEntry(self.localentry, 0)
            return self.m1IP3DS_value

    property m1IsGlobal:
        def __get__(self):
            self.m1IsGlobal_branch.GetEntry(self.localentry, 0)
            return self.m1IsGlobal_value

    property m1IsTracker:
        def __get__(self):
            self.m1IsTracker_branch.GetEntry(self.localentry, 0)
            return self.m1IsTracker_value

    property m1JetBtag:
        def __get__(self):
            self.m1JetBtag_branch.GetEntry(self.localentry, 0)
            return self.m1JetBtag_value

    property m1JetCSVBtag:
        def __get__(self):
            self.m1JetCSVBtag_branch.GetEntry(self.localentry, 0)
            return self.m1JetCSVBtag_value

    property m1JetPt:
        def __get__(self):
            self.m1JetPt_branch.GetEntry(self.localentry, 0)
            return self.m1JetPt_value

    property m1Mass:
        def __get__(self):
            self.m1Mass_branch.GetEntry(self.localentry, 0)
            return self.m1Mass_value

    property m1MtToMET:
        def __get__(self):
            self.m1MtToMET_branch.GetEntry(self.localentry, 0)
            return self.m1MtToMET_value

    property m1NormTrkChi2:
        def __get__(self):
            self.m1NormTrkChi2_branch.GetEntry(self.localentry, 0)
            return self.m1NormTrkChi2_value

    property m1PFIDTight:
        def __get__(self):
            self.m1PFIDTight_branch.GetEntry(self.localentry, 0)
            return self.m1PFIDTight_value

    property m1Phi:
        def __get__(self):
            self.m1Phi_branch.GetEntry(self.localentry, 0)
            return self.m1Phi_value

    property m1PixHits:
        def __get__(self):
            self.m1PixHits_branch.GetEntry(self.localentry, 0)
            return self.m1PixHits_value

    property m1Pt:
        def __get__(self):
            self.m1Pt_branch.GetEntry(self.localentry, 0)
            return self.m1Pt_value

    property m1PtUncorr:
        def __get__(self):
            self.m1PtUncorr_branch.GetEntry(self.localentry, 0)
            return self.m1PtUncorr_value

    property m1RelPFIsoDB:
        def __get__(self):
            self.m1RelPFIsoDB_branch.GetEntry(self.localentry, 0)
            return self.m1RelPFIsoDB_value

    property m1VBTFID:
        def __get__(self):
            self.m1VBTFID_branch.GetEntry(self.localentry, 0)
            return self.m1VBTFID_value

    property m1VZ:
        def __get__(self):
            self.m1VZ_branch.GetEntry(self.localentry, 0)
            return self.m1VZ_value

    property m1WWID:
        def __get__(self):
            self.m1WWID_branch.GetEntry(self.localentry, 0)
            return self.m1WWID_value

    property m1_m2_DPhi:
        def __get__(self):
            self.m1_m2_DPhi_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_DPhi_value

    property m1_m2_DR:
        def __get__(self):
            self.m1_m2_DR_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_DR_value

    property m1_m2_Mass:
        def __get__(self):
            self.m1_m2_Mass_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_Mass_value

    property m1_m2_PZeta:
        def __get__(self):
            self.m1_m2_PZeta_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_PZeta_value

    property m1_m2_PZetaVis:
        def __get__(self):
            self.m1_m2_PZetaVis_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_PZetaVis_value

    property m1_m2_Pt:
        def __get__(self):
            self.m1_m2_Pt_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_Pt_value

    property m1_m2_SS:
        def __get__(self):
            self.m1_m2_SS_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_SS_value

    property m1_m2_Zcompat:
        def __get__(self):
            self.m1_m2_Zcompat_branch.GetEntry(self.localentry, 0)
            return self.m1_m2_Zcompat_value

    property m1_m3_DPhi:
        def __get__(self):
            self.m1_m3_DPhi_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_DPhi_value

    property m1_m3_DR:
        def __get__(self):
            self.m1_m3_DR_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_DR_value

    property m1_m3_Mass:
        def __get__(self):
            self.m1_m3_Mass_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_Mass_value

    property m1_m3_PZeta:
        def __get__(self):
            self.m1_m3_PZeta_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_PZeta_value

    property m1_m3_PZetaVis:
        def __get__(self):
            self.m1_m3_PZetaVis_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_PZetaVis_value

    property m1_m3_Pt:
        def __get__(self):
            self.m1_m3_Pt_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_Pt_value

    property m1_m3_SS:
        def __get__(self):
            self.m1_m3_SS_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_SS_value

    property m1_m3_Zcompat:
        def __get__(self):
            self.m1_m3_Zcompat_branch.GetEntry(self.localentry, 0)
            return self.m1_m3_Zcompat_value

    property m2AbsEta:
        def __get__(self):
            self.m2AbsEta_branch.GetEntry(self.localentry, 0)
            return self.m2AbsEta_value

    property m2Charge:
        def __get__(self):
            self.m2Charge_branch.GetEntry(self.localentry, 0)
            return self.m2Charge_value

    property m2D0:
        def __get__(self):
            self.m2D0_branch.GetEntry(self.localentry, 0)
            return self.m2D0_value

    property m2DZ:
        def __get__(self):
            self.m2DZ_branch.GetEntry(self.localentry, 0)
            return self.m2DZ_value

    property m2Eta:
        def __get__(self):
            self.m2Eta_branch.GetEntry(self.localentry, 0)
            return self.m2Eta_value

    property m2GlbTrkHits:
        def __get__(self):
            self.m2GlbTrkHits_branch.GetEntry(self.localentry, 0)
            return self.m2GlbTrkHits_value

    property m2IP3DS:
        def __get__(self):
            self.m2IP3DS_branch.GetEntry(self.localentry, 0)
            return self.m2IP3DS_value

    property m2IsGlobal:
        def __get__(self):
            self.m2IsGlobal_branch.GetEntry(self.localentry, 0)
            return self.m2IsGlobal_value

    property m2IsTracker:
        def __get__(self):
            self.m2IsTracker_branch.GetEntry(self.localentry, 0)
            return self.m2IsTracker_value

    property m2JetBtag:
        def __get__(self):
            self.m2JetBtag_branch.GetEntry(self.localentry, 0)
            return self.m2JetBtag_value

    property m2JetCSVBtag:
        def __get__(self):
            self.m2JetCSVBtag_branch.GetEntry(self.localentry, 0)
            return self.m2JetCSVBtag_value

    property m2JetPt:
        def __get__(self):
            self.m2JetPt_branch.GetEntry(self.localentry, 0)
            return self.m2JetPt_value

    property m2Mass:
        def __get__(self):
            self.m2Mass_branch.GetEntry(self.localentry, 0)
            return self.m2Mass_value

    property m2MtToMET:
        def __get__(self):
            self.m2MtToMET_branch.GetEntry(self.localentry, 0)
            return self.m2MtToMET_value

    property m2NormTrkChi2:
        def __get__(self):
            self.m2NormTrkChi2_branch.GetEntry(self.localentry, 0)
            return self.m2NormTrkChi2_value

    property m2PFIDTight:
        def __get__(self):
            self.m2PFIDTight_branch.GetEntry(self.localentry, 0)
            return self.m2PFIDTight_value

    property m2Phi:
        def __get__(self):
            self.m2Phi_branch.GetEntry(self.localentry, 0)
            return self.m2Phi_value

    property m2PixHits:
        def __get__(self):
            self.m2PixHits_branch.GetEntry(self.localentry, 0)
            return self.m2PixHits_value

    property m2Pt:
        def __get__(self):
            self.m2Pt_branch.GetEntry(self.localentry, 0)
            return self.m2Pt_value

    property m2PtUncorr:
        def __get__(self):
            self.m2PtUncorr_branch.GetEntry(self.localentry, 0)
            return self.m2PtUncorr_value

    property m2RelPFIsoDB:
        def __get__(self):
            self.m2RelPFIsoDB_branch.GetEntry(self.localentry, 0)
            return self.m2RelPFIsoDB_value

    property m2VBTFID:
        def __get__(self):
            self.m2VBTFID_branch.GetEntry(self.localentry, 0)
            return self.m2VBTFID_value

    property m2VZ:
        def __get__(self):
            self.m2VZ_branch.GetEntry(self.localentry, 0)
            return self.m2VZ_value

    property m2WWID:
        def __get__(self):
            self.m2WWID_branch.GetEntry(self.localentry, 0)
            return self.m2WWID_value

    property m2_m3_DPhi:
        def __get__(self):
            self.m2_m3_DPhi_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_DPhi_value

    property m2_m3_DR:
        def __get__(self):
            self.m2_m3_DR_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_DR_value

    property m2_m3_Mass:
        def __get__(self):
            self.m2_m3_Mass_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_Mass_value

    property m2_m3_PZeta:
        def __get__(self):
            self.m2_m3_PZeta_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_PZeta_value

    property m2_m3_PZetaVis:
        def __get__(self):
            self.m2_m3_PZetaVis_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_PZetaVis_value

    property m2_m3_Pt:
        def __get__(self):
            self.m2_m3_Pt_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_Pt_value

    property m2_m3_SS:
        def __get__(self):
            self.m2_m3_SS_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_SS_value

    property m2_m3_Zcompat:
        def __get__(self):
            self.m2_m3_Zcompat_branch.GetEntry(self.localentry, 0)
            return self.m2_m3_Zcompat_value

    property m3AbsEta:
        def __get__(self):
            self.m3AbsEta_branch.GetEntry(self.localentry, 0)
            return self.m3AbsEta_value

    property m3Charge:
        def __get__(self):
            self.m3Charge_branch.GetEntry(self.localentry, 0)
            return self.m3Charge_value

    property m3D0:
        def __get__(self):
            self.m3D0_branch.GetEntry(self.localentry, 0)
            return self.m3D0_value

    property m3DZ:
        def __get__(self):
            self.m3DZ_branch.GetEntry(self.localentry, 0)
            return self.m3DZ_value

    property m3Eta:
        def __get__(self):
            self.m3Eta_branch.GetEntry(self.localentry, 0)
            return self.m3Eta_value

    property m3GlbTrkHits:
        def __get__(self):
            self.m3GlbTrkHits_branch.GetEntry(self.localentry, 0)
            return self.m3GlbTrkHits_value

    property m3IP3DS:
        def __get__(self):
            self.m3IP3DS_branch.GetEntry(self.localentry, 0)
            return self.m3IP3DS_value

    property m3IsGlobal:
        def __get__(self):
            self.m3IsGlobal_branch.GetEntry(self.localentry, 0)
            return self.m3IsGlobal_value

    property m3IsTracker:
        def __get__(self):
            self.m3IsTracker_branch.GetEntry(self.localentry, 0)
            return self.m3IsTracker_value

    property m3JetBtag:
        def __get__(self):
            self.m3JetBtag_branch.GetEntry(self.localentry, 0)
            return self.m3JetBtag_value

    property m3JetCSVBtag:
        def __get__(self):
            self.m3JetCSVBtag_branch.GetEntry(self.localentry, 0)
            return self.m3JetCSVBtag_value

    property m3JetPt:
        def __get__(self):
            self.m3JetPt_branch.GetEntry(self.localentry, 0)
            return self.m3JetPt_value

    property m3Mass:
        def __get__(self):
            self.m3Mass_branch.GetEntry(self.localentry, 0)
            return self.m3Mass_value

    property m3MtToMET:
        def __get__(self):
            self.m3MtToMET_branch.GetEntry(self.localentry, 0)
            return self.m3MtToMET_value

    property m3NormTrkChi2:
        def __get__(self):
            self.m3NormTrkChi2_branch.GetEntry(self.localentry, 0)
            return self.m3NormTrkChi2_value

    property m3PFIDTight:
        def __get__(self):
            self.m3PFIDTight_branch.GetEntry(self.localentry, 0)
            return self.m3PFIDTight_value

    property m3Phi:
        def __get__(self):
            self.m3Phi_branch.GetEntry(self.localentry, 0)
            return self.m3Phi_value

    property m3PixHits:
        def __get__(self):
            self.m3PixHits_branch.GetEntry(self.localentry, 0)
            return self.m3PixHits_value

    property m3Pt:
        def __get__(self):
            self.m3Pt_branch.GetEntry(self.localentry, 0)
            return self.m3Pt_value

    property m3PtUncorr:
        def __get__(self):
            self.m3PtUncorr_branch.GetEntry(self.localentry, 0)
            return self.m3PtUncorr_value

    property m3RelPFIsoDB:
        def __get__(self):
            self.m3RelPFIsoDB_branch.GetEntry(self.localentry, 0)
            return self.m3RelPFIsoDB_value

    property m3VBTFID:
        def __get__(self):
            self.m3VBTFID_branch.GetEntry(self.localentry, 0)
            return self.m3VBTFID_value

    property m3VZ:
        def __get__(self):
            self.m3VZ_branch.GetEntry(self.localentry, 0)
            return self.m3VZ_value

    property m3WWID:
        def __get__(self):
            self.m3WWID_branch.GetEntry(self.localentry, 0)
            return self.m3WWID_value

    property metEt:
        def __get__(self):
            self.metEt_branch.GetEntry(self.localentry, 0)
            return self.metEt_value

    property metPhi:
        def __get__(self):
            self.metPhi_branch.GetEntry(self.localentry, 0)
            return self.metPhi_value

    property metSignificance:
        def __get__(self):
            self.metSignificance_branch.GetEntry(self.localentry, 0)
            return self.metSignificance_value

    property mu17ele8Group:
        def __get__(self):
            self.mu17ele8Group_branch.GetEntry(self.localentry, 0)
            return self.mu17ele8Group_value

    property mu17ele8Pass:
        def __get__(self):
            self.mu17ele8Pass_branch.GetEntry(self.localentry, 0)
            return self.mu17ele8Pass_value

    property mu17ele8Prescale:
        def __get__(self):
            self.mu17ele8Prescale_branch.GetEntry(self.localentry, 0)
            return self.mu17ele8Prescale_value

    property mu8ele17Group:
        def __get__(self):
            self.mu8ele17Group_branch.GetEntry(self.localentry, 0)
            return self.mu8ele17Group_value

    property mu8ele17Pass:
        def __get__(self):
            self.mu8ele17Pass_branch.GetEntry(self.localentry, 0)
            return self.mu8ele17Pass_value

    property mu8ele17Prescale:
        def __get__(self):
            self.mu8ele17Prescale_branch.GetEntry(self.localentry, 0)
            return self.mu8ele17Prescale_value

    property muGlbIsoVetoPt10:
        def __get__(self):
            self.muGlbIsoVetoPt10_branch.GetEntry(self.localentry, 0)
            return self.muGlbIsoVetoPt10_value

    property muVetoPt5:
        def __get__(self):
            self.muVetoPt5_branch.GetEntry(self.localentry, 0)
            return self.muVetoPt5_value

    property nTruePU:
        def __get__(self):
            self.nTruePU_branch.GetEntry(self.localentry, 0)
            return self.nTruePU_value

    property nvtx:
        def __get__(self):
            self.nvtx_branch.GetEntry(self.localentry, 0)
            return self.nvtx_value

    property processID:
        def __get__(self):
            self.processID_branch.GetEntry(self.localentry, 0)
            return self.processID_value

    property puWeightData2011AB:
        def __get__(self):
            self.puWeightData2011AB_branch.GetEntry(self.localentry, 0)
            return self.puWeightData2011AB_value

    property puWeightData2012A:
        def __get__(self):
            self.puWeightData2012A_branch.GetEntry(self.localentry, 0)
            return self.puWeightData2012A_value

    property puWeightData2012AB:
        def __get__(self):
            self.puWeightData2012AB_branch.GetEntry(self.localentry, 0)
            return self.puWeightData2012AB_value

    property rho:
        def __get__(self):
            self.rho_branch.GetEntry(self.localentry, 0)
            return self.rho_value

    property run:
        def __get__(self):
            self.run_branch.GetEntry(self.localentry, 0)
            return self.run_value

    property singleMuGroup:
        def __get__(self):
            self.singleMuGroup_branch.GetEntry(self.localentry, 0)
            return self.singleMuGroup_value

    property singleMuPass:
        def __get__(self):
            self.singleMuPass_branch.GetEntry(self.localentry, 0)
            return self.singleMuPass_value

    property singleMuPrescale:
        def __get__(self):
            self.singleMuPrescale_branch.GetEntry(self.localentry, 0)
            return self.singleMuPrescale_value

    property tauVetoPt20:
        def __get__(self):
            self.tauVetoPt20_branch.GetEntry(self.localentry, 0)
            return self.tauVetoPt20_value

    property idx:
        def __get__(self):
            self.idx_branch.GetEntry(self.localentry, 0)
            return self.idx_value


