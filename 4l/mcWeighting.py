import FinalStateAnalysis.TagAndProbe.PileupWeight as PileupWeight

def make_PUCorrector():
    datasets = ["$CMSSW_BASE/src/UWHiggs/4l/PU/2012/data_pu.root"]
            #"$CMSSW_BASE/src/UWHiggs/4l/PU/2012/puProfile_Data_8TeV.root",
            #"$CMSSW_BASE/src/UWHiggs/4l/PU/2012/puProfile_Summer12_53X.root"]
            
    mctag ='S10'

    return PileupWeight.PileupWeight(mctag, *datasets)
