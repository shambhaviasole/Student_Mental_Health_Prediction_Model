import pandas
from sklearn.tree import DecisionTreeClassifier
import joblib

url="processed_student_mental_health.csv"
df=pandas.read_csv(url)
#print(df)

features=df[['Gender','Age','Education','ScreenTime','Sleep','Physical','Stress','Anxious','AcademicPerf']]
#print(features)
labels=df['Label']
#print(labels)

model=DecisionTreeClassifier()
model.fit(features,labels)

joblib.dump(model,'processed_student_mental_health.joblib')
print('Trained model saved for future use')
