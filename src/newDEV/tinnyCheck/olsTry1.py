# model ols categorical data
import numpy as np 
import statsmodels.api as sm 
from statsmodels.sandbox.regression.predstd import wls_prediction_std


# nsample = 50 

# sig = 0.5
# x = np.linspace(0,20,nsample)

# X = np.c_[x, np.sin(x), (x-5)**2, np.ones(nsample)]
# beta = [0.5, 0.5, -0.02, 5 ]

# y_true = np.dot(X, beta)

# y = y_true + sig * np.random.normal(size=nsample)

# ###############
# model = sm.OLS(y,X)
# result = model.fit() 
# print y, X
# print y.shape, X.shape
import matplotlib.pyplot as plt

# plt.figure()
# plt.plot(x,y,'o', x, y_true ,'b-')
# plt.plot(x, result.fittedvalues, 'r--.')
# plt.show()

nsample = 50
groups = np.zeros(nsample, int)

groups[20:40] = 1
groups[40:] = 2
print groups
dummy = (groups[:, None] == np.unique(groups)).astype(float)
print dummy
x = np.linspace(0, 20, nsample)

X = np.c_[x, dummy[:, 1:], np.ones(nsample)]

beta = [1., 3, -3, 10]

y_true = np.dot(X, beta)

e = np.random.normal(size=nsample)

y = y_true +e 


print y, X 

print y.shape, X.shape 

plt.figure()
plt.plot(x,y,'o', x, y_true ,'b-')
plt.show()
