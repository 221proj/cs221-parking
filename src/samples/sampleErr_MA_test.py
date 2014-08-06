
import matplotlib.pyplot as plt 

MA_step = [1,2,3,4]

#202052 = [0.0650524, 0.0648429, 0.064760, 0.064596]
#671001 = [0.0414606, 0.0420560, 0.042339, 0.042425]
#330032 = [0.0010213, 0.0009448,  0.0009321, 0.00093029 ]


Y1 = [0.0650524, 0.0648429, 0.064760, 0.064596]
Y2 = [0.0414606, 0.0420560, 0.042339, 0.042425]
Y3 = [0.0010213, 0.0009448,  0.0009321, 0.00093029 ]


Y_tsLabels =['Lot-202052','Lot-671001', 'Lot-330032']


plt.figure()
data = [Y1,Y2]
#plt.plot(MA_step, Y1, 'r-', MA_step, Y2, 'g-', MA_step, Y3)
plt.boxplot(data)
#plt.ylim(0,0.2)
plt.xlabel('Moving Average Step')
plt.ylabel('Prediction Error Rate')
plt.title('Single Lot Prediction Error Rate vs MA steps')
plt.legend(Y_tsLabels)

plt.show()