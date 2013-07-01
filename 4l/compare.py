"""
"""

import json
import sys

if len(sys.argv) < 4:
    print "Usage: python compare.py [file1].json [file2].json [compare_op]"
    sys.exit(1)

file1 = open(sys.argv[1],'r')
file2 = open(sys.argv[2],'r')
comp  = sys.argv[3]

ntuple1 = json.load( file1 )
ntuple2 = json.load( file2 )

event_set1 = set( ntuple1.keys() )
event_set2 = set( ntuple2.keys() )
diff_set = set()



def print_comparision( event, ntuple1, ntuple2 ):
    vars = ["event","mass","z1mass","z2mass","z1l1pt","z1l2pt",
            "z2l1pt","z2l2pt","channel"]

    lengths = [5,7,7,7,7,12,7,12,7,12,7,12]

    row_format = ""
    top_format = ""
    for i in range(len(vars)):
        row_format += "{" + str(i) + ":<" + str(15) + "} "

    print row_format.format("", *vars)

    row1 = ntuple1[event]
    row2 = ntuple2[event]

    list1 = []
    list2 = []

    for var in vars:
        list1.append( row1[var] )
        list2.append( row2[var] )

    print row_format.format("", *list1 )
    print row_format.format("", *list2 )
    print ""



if comp == "subtract":
    diff_set = event_set1 - event_set2
    print len(diff_set)
elif comp == "intersect":
    diff_set = event_set1.intersection( event_set2 )
    print len(diff_set)

    for event in diff_set:
        print_comparision( event, ntuple1, ntuple2 )
