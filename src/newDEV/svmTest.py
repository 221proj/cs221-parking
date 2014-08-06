### this script utilize the svm ###
# 
# 
# 
from sklearn.svm import SVR 
import numpy as np 

n_samples, n_features = 10, 5
np.random.seed(0)

x = np.sort(5 * np.random.rand(40, 1), axis=0)
y = np.sin(x).ravel()

###############################################################################
# Add noise to targets
y[::5] += 3 * (0.5 - np.random.rand(8))


# y = np.random.randn(n_samples)
# x = np.random.randn(n_samples, n_features)
# classifier 

clf = SVR(C=1.0, epsilon=0.2)
svr_rbf = clf.fit(x,y)

y_rbf = svr_rbf.predict(x)
print y_rbf
print "\n***\n"
print y 
 
import matplotlib.pyplot as plt 
plt.figure()
plt.scatter(x, y)
plt.plot(x, y_rbf, 'r-')
plt.show()


