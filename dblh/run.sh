#!/bin/bash

set -o nounset
set -o errexit

#export jobid=hpphmm-110-ntuple-21-jan-14
export jobid=ntuple_hpp4l-110_27jan14
export PU=false
rake test
