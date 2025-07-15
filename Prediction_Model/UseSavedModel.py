import joblib
import pandas

model=joblib.load('processed_student_mental_health.joblib')

newdata=pandas.DataFrame({'Gender':[0],'Age':[20],'Education':[9],'ScreenTime':[11.2],'Sleep':[6.5],'Physical':[1],'Stress':[2],'Anxious':[2],'AcademicPerf':[1]})
prediction=model.predict(newdata)
print('Mental Health Fitness level prediction :',prediction)