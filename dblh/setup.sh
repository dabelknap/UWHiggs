#!/bin/bash

#Get the data
export datasrc=/nfs_scratch/belknap/data
#export datasrc=/hdfs/store/user/belknap

#export jobid=hpphmm-110-ntuple-21-jan-14
export jobid=ntuple_hpp4l-110_27jan14
export jobid8TeV=$jobid
export afile=`find $datasrc/$jobid | grep root | head -n 1`

rake "make_wrapper[$afile, mmmm/final/Ntuple, MuMuMuMuTree]"

ls *pyx | sed "s|pyx|so|" | xargs rake

rake "meta:getinputs[$jobid, $datasrc, mmmm/metaInfo]"
rake "meta:getmeta[inputs/$jobid, mmmm/metaInfo, 8]"
