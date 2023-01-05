import joblib
import sklearn

#Loading algorithm
loaded_rf = joblib.load("my_random_forest.joblib")
#Data to test
one= [[0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7]]
#Prediction
predict_2=loaded_rf.predict(one)
#Printed Prediction
for data in predict_2:
            if(data==0):
                print('Beningn')
            if(data==1):
                print('Web Attack Brute Force')
            if(data==2):
                print('Web Attack XSS')
            if(data==3):
                print('Web Attack SQL injection')

print('finished')