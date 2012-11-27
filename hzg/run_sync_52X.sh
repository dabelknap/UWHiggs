#!/bin/bash

# A script to get a sync revision and run the ntuplization locally

srmPrefix="srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN"
remoteDataDir="/hdfs/store/user/lgray/HZG_sync/"
localDataDir="/scratch/$USER/data/HZG_sync/"
syncPostfix=${1}

if [ -z "$syncPostfix" ]
then
    echo "Please specify a postfix representing the sync revision!"
    pstfxs=`lcg-ls ${srmPrefix}=${remoteDataDir}`
    echo "Available postfixes: " 
    for fix in $pstfxs
    do
      echo " ${fix##*/}"
    done    
    exit
fi

mcSignalEle=`lcg-ls -b -Dsrmv2 ${srmPrefix}=${remoteDataDir}${syncPostfix}/52X/ | grep MCSignalEle | sed 's/\/hdfs\/store/root\:\/\/cmsxrootd\.hep\.wisc\.edu\/\/store/' | tr '\n' '\,' | head -c -1`
mcBkgEle=`lcg-ls -b -Dsrmv2 ${srmPrefix}=${remoteDataDir}${syncPostfix}/52X/ | grep MCBkgEle | sed 's/\/hdfs\/store/root\:\/\/cmsxrootd\.hep\.wisc\.edu\/\/store/' | tr '\n' '\,' | head -c -1`
dataElectron=`lcg-ls -b -Dsrmv2 ${srmPrefix}=${remoteDataDir}${syncPostfix}/52X/ | grep DataElectron | sed 's/\/hdfs\/store/root\:\/\/cmsxrootd\.hep\.wisc\.edu\/\/store/' | tr '\n' '\,' | head -c -1`
dataMuon=`lcg-ls -b -Dsrmv2 ${srmPrefix}=${remoteDataDir}${syncPostfix}/52X/ | grep DataMuon | sed 's/\/hdfs\/store/root\:\/\/cmsxrootd\.hep\.wisc\.edu\/\/store/' | tr '\n' '\,' | head -c -1`

theCfg=$CMSSW_BASE/src/FinalStateAnalysis/NtupleTools/test/make_ntuples_cfg.py

sync_52X=()
sync_52X+=("DataMuon;${dataMuon}")
sync_52X+=("DataElectron;${dataElectron}")
sync_52X+=("MCSignalEle;${mcSignalEle}")
sync_52X+=("MCBkgEle;${mcBkgEle}")

for sync_test in ${sync_52X[@]}
do
  parts=(`echo $sync_test | tr ';' ' '`)
  echo
  echo ${parts[0]} ${parts[1]}

  jobName=hZg_sync_52X_ntuples.${syncPostfix}.${parts[0]}
  fajOpts="--infer-cmssw-path --express-queue --job-generates-output-name --output-dir=${hdfsOutDir} --input-dir=${parts[1]%/*##*,}/ --input-file-list=${jobName}.input.txt"
  patTupleOpts="makeHZG=1 makeDiObject=1 passThru=1 eventView=1 reportEvery=100 maxEvents=-1 outputFile=${jobName}.root passThru=1"

  rm -rf ${jobName}.input.txt
  for file in `echo ${parts[1]} | tr ',' '\n'`
  do
    echo ${file##*/} | tr ',' '\n' >> ${jobName}.input.txt
  done

  echo farmoutAnalysisJobs $fajOpts $jobName $theCfg inputFiles='$inputFileNames' $patTupleOpts $dataOpts 
done
