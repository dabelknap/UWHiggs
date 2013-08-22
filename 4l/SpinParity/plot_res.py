import tables as tb
from pylab import *

h5file = tb.open_file('output.h5',mode='r')

table = h5file.root.MMMM.events

var1 = 'Phi1'
var2 = 'Phi1_gen'

cut = '(40 < z1mass) & (z1mass < 120) & (12 < z2mass) & (z2mass < 120) & (106 < mass) & (mass < 141) & (costheta1_gen > -10)'

values = [ x[var1]-x[var2] for x in table.where(cut) ]

font = {#'family' : 'arial',
       'size'   : 14}

matplotlib.rc('font', **font)

hist(values, 40, range=(-0.15,0.1), histtype='stepfilled', facecolor='lightgreen', linewidth=2, edgecolor='darkgreen', label=var1+'-'+var2)

legend(loc='upper left')
xlabel(var1 + '-' + var2)
savefig(var1 + '_res' + '.pdf')

h5file.close()
