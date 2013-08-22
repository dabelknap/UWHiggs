import tables as tb
from pylab import *

h5file = tb.open_file('output.h5',mode='r')

table = h5file.root.MMMM.events

var = 'costheta1_gen'
cut = '(40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & (106 < mass) & (mass < 141) & (costheta1_gen > -10)'

values = [x[var] for x in table.where(cut)]

font = {#'family' : 'arial',
       'size'   : 14}

matplotlib.rc('font', **font)

hist(values, 40, histtype='stepfilled', facecolor='lightgreen', edgecolor='darkgreen', label=var)
legend(loc='upper left')
savefig(var + '.pdf')

h5file.close()
