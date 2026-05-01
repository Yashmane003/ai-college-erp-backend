import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

data = {
    'attendance': [90, 85, 70, 60, 95, 80, 75, 50],
    'assignment_score': [88, 78, 65, 55, 92, 74, 70, 40],
    'midterm_score': [85, 75, 60, 50, 95, 72, 68, 35],
    'final_score': [90, 80, 65, 55, 95, 78, 72, 42]
}

df = pd.DataFrame(data)

X = df[['attendance', 'assignment_score', 'midterm_score']]
y = df['final_score']

model = LinearRegression()
model.fit(X, y)

with open('student_model.pkl', 'wb') as file:
    pickle.dump(model, file)

