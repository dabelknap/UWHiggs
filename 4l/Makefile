
#ROOTDIR=./rootFiles
#NTUPDIR=./ntuples_20feb14

ROOTDIR=./rootFiles_trig
NTUPDIR=./ntuples_02mar14

all : signal zz ggzz data

signal : $(NTUPDIR)/SMHiggs-126.h5 $(NTUPDIR)/Higgs0M-126.h5 $(NTUPDIR)/Higgs0PH-126.h5 $(NTUPDIR)/Higgs2PM-126.h5 $(NTUPDIR)/Higgs2PMqq-126.h5

zz : $(NTUPDIR)/ZZMMMM.h5 $(NTUPDIR)/ZZEEEE.h5 $(NTUPDIR)/ZZTTTT.h5 $(NTUPDIR)/ZZEEMM.h5 $(NTUPDIR)/ZZMMTT.h5 $(NTUPDIR)/ZZEETT.h5

ggzz : $(NTUPDIR)/ggZZ4L.h5 $(NTUPDIR)/ggZZ2L2L.h5

data : $(NTUPDIR)/data_2012A.h5 $(NTUPDIR)/data_2012B.h5 $(NTUPDIR)/data_2012C.h5 $(NTUPDIR)/data_2012D.h5


$(NTUPDIR)/SMHiggs-126.h5 : $(ROOTDIR)/SMHiggs-126.root
	$(eval XSEC=2.79317)
	$(eval EVTS=299979)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/Higgs0M-126.h5 : $(ROOTDIR)/Higgs0M-126.root
	$(eval XSEC=2.79317)
	$(eval EVTS=299972)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/Higgs0PH-126.h5 : $(ROOTDIR)/Higgs0PH-126.root
	$(eval XSEC=2.79317)
	$(eval EVTS=293973)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/Higgs2PM-126.h5 : $(ROOTDIR)/Graviton2PM-126.root
	$(eval XSEC=2.79317)
	$(eval EVTS=291881)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/Higgs2PMqq-126.h5 : $(ROOTDIR)/Graviton2PMqq-126.root
	$(eval XSEC=2.79317)
	$(eval EVTS=187977)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@



$(NTUPDIR)/ZZMMMM.h5 : $(ROOTDIR)/ZZTo4mu_8TeV-powheg-pythia6.root
	$(eval XSEC=76.91)
	$(eval EVTS=1499064)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/ZZEEEE.h5 : $(ROOTDIR)/ZZTo4e_8TeV-powheg-pythia6.root
	$(eval XSEC=76.91)
	$(eval EVTS=1476608)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/ZZTTTT.h5 : $(ROOTDIR)/ZZTo4tau_8TeV-powheg-pythia6.root
	$(eval XSEC=76.91)
	$(eval EVTS=824466)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@



$(NTUPDIR)/ZZEEMM.h5 : $(ROOTDIR)/ZZTo2e2mu_8TeV-powheg-pythia6.root
	$(eval XSEC=176.7)
	$(eval EVTS=1497445)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/ZZEETT.h5 : $(ROOTDIR)/ZZTo2e2tau_8TeV-powheg-pythia6.root
	$(eval XSEC=176.7)
	$(eval EVTS=823911)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/ZZMMTT.h5 : $(ROOTDIR)/ZZTo2mu2tau_8TeV-powheg-pythia6.root
	$(eval XSEC=176.7)
	$(eval EVTS=816729)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@



$(NTUPDIR)/ggZZ4L.h5 : $(ROOTDIR)/ggZZ4L.root
	$(eval XSEC=4.8)
	$(eval EVTS=460969)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/ggZZ2L2L.h5 : $(ROOTDIR)/ggZZ2L2L.root
	$(eval XSEC=12.03)
	$(eval EVTS=372175)
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	#python set_nevents.py output.h5 $(EVTS) $(XSEC)
	python set_nevents.py output.h5 $(patsubst %.root,%.json,$<) $(XSEC)
	mv output.h5 $@

$(NTUPDIR)/data_2012A.h5 : $(ROOTDIR)/data_2012A.root
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	mv output.h5 $@

$(NTUPDIR)/data_2012B.h5 : $(ROOTDIR)/data_2012B.root
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	mv output.h5 $@

$(NTUPDIR)/data_2012C.h5 : $(ROOTDIR)/data_2012C.root
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	mv output.h5 $@

$(NTUPDIR)/data_2012D.h5 : $(ROOTDIR)/data_2012D.root
	mega AnalyzeMMMM.py $< output.root
	mega AnalyzeEEEE.py $< output.root
	mega AnalyzeEEMM.py $< output.root
	mv output.h5 $@
