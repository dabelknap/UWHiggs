
import tables as tb
import sys
import json

if len(sys.argv) != 4:
    sys.stderr.write("Usage: set_nevents.py [hdf5 file] [N gen events] [xsec]\n")
    sys.exit(1)

with tb.open_file(sys.argv[1],'r+') as h5file:
    #nevents = int(sys.argv[2])
    with open(sys.argv[2], 'r') as jfile:
        nevents = float(json.load(jfile)["n_evts"])

    xsec = float(sys.argv[3])
    
    h5file.root._v_attrs.ISMC = 1
    h5file.root._v_attrs.XSEC = xsec
    h5file.root._v_attrs.GENEVENTS = nevents