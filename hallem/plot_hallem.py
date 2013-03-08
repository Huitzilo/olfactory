#!/usr/bin/env python
# encoding: utf-8
"""

Just plotting the hallem rows (Odorants) as a boxplot to get a look and
feel which odorant might carry the most/the least information

"""
import pylab as pl
import numpy as np
from hallem.data import Hallem

hallem = Hallem()
fig = pl.figure(figsize=(30, 15))
fig.autofmt_xdate()
t = []
for i in hallem.odorant_list:
    t.append(i.decode("utf8"))

pl.boxplot(np.transpose(hallem.get_activation_matrix()), bootstrap=10000, vert=True)
pl.xticks(np.arange(1, len(hallem.odorant_list) + 1), t, rotation="vertical")
pl.savefig("figures/odorant_boxplot.png")

pl.figure()
pl.plot(range(23), hallem.get_activation_matrix()[15])
pl.savefig("figures/glycerol_activation.png")

pl.figure()
pl.plot(range(23), hallem.get_activation_matrix()[43])
pl.savefig("figures/isobutylacetat_activation.png")

print hallem.odorant_list[[15, 43]]
print np.std(hallem.get_activation_matrix(), axis=1)[[15, 43]]

# matrix = np.transpose(hallem.get_activation_matrix())
# matrix = hallem.get_activation_matrix()
# print matrix.shape
# means_odorants = np.mean(matrix, axis=1)
# means_glomeruli = np.mean(matrix, axis=0)

# stds_odorants = np.std(matrix, axis=1)
# stds_glomeruli = np.std(matrix, axis=0)



# print means

#sorted_odorants = np.argsort(x)
#sorted_glomeruli = np.argsort(y)

#pl.plot(range(len(means_odorants)), )
#pl.plot(range(len(stds_odorants)), stds_odorants)
#pl.plot(range(len(stds_glomeruli)), stds_glomeruli)
#print y[18:23]


#index = 21
#print matrix[:, index], means_glomeruli[index], stds_glomeruli[index]
#pl.plot(range(len(means_glomeruli)), means_glomeruli[sorted_glomeruli])
#pl.plot(range(len(stds_glomeruli)), stds_glomeruli[sorted_glomeruli])

#pl.show()

#print np.cov(matrix, rowvar=1)[0]

# M = [[2.5, 2.4],
#      [0.5, 0.7],
#      [2.2, 2.9],
#      [1.9, 2.2],
#      [3.1, 3.0],
#      [2.3, 2.7],
#      [2, 1.6],
#      [1, 1.1],
#      [1.5, 1.6],
#      [1.1, 0.9]]




# x = PCA()
# x.fit(matrix)
# print x.explained_variance_ratio_

# corr = []
# strong_corr = []
# for i, rowA in enumerate(matrix):
#     for j, rowB in enumerate(matrix):
#         if j > i:
#             c = sp.stats.pearsonr(rowA, rowB)[0]
#             if c > 0.65:
#                 print "strong correlation:", i, j, c
#                 strong_corr.append((i, j, c))
#             corr.append(c)
#
# pl.title("Correlation between glomeruli")
# pl.xlabel("Pearson Correlation")
# pl.ylabel("Count")
# pl.hist(corr, bins=20)
# pl.savefig("figures/pearson_glomeruli.png")
#
# for i in strong_corr:
#     o1 = i[0]
#     o2 = i[1]
#     o1_name = hallem.or_list[o1]
#     o2_name = hallem.or_list[o2]
#     pl.figure()
#     pl.title(o1_name + " against " + o2_name + "| correlation=" + str(i[2]))
#     pl.plot(matrix[o1], matrix[o2], '.')
#     pl.xlabel(o1_name)
#     pl.ylabel(o2_name)
#     pl.savefig("figures/correlation/" + o1_name + "_" + o2_name + ".png")
# s = 0
# for i in x.explained_variance_ratio_:
#     s += i;
#     print s, i



#print np.dot(x.components_ ,np.transpose(M))


#for i in x.components_[0:7]:
#    pl.plot(range(len(i)), i)

#pl.legend(range(0,24))
#pl.show()
#19, 20 glom
#23, 82 odorant