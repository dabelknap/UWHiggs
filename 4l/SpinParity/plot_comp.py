import tables as tb
from pylab import *

h5file = tb.open_file('output.h5',mode='r')

table = h5file.root.MMMM.events

var1 = 'Phi1'
var2 = 'Phi1_gen'

cut = '(40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & (106 < mass) & (mass < 141) & (costheta1_gen > -10)'

val1 = []
val2 = []

for x in table.where(cut):
    val1.append( x[var1] )
    val2.append( x[var2] )

font = {#'family' : 'arial',
       'size'   : 14}

matplotlib.rc('font', **font)

hist(val1, 40, histtype='stepfilled', fill=False, linewidth=2, edgecolor='green', label=var1)
hist(val2, 40, histtype='stepfilled', fill=False, linewidth=2, edgecolor='blue', label=var2)

legend(loc='upper left')
savefig(var1 + '_comp' + '.pdf')

h5file.close()
