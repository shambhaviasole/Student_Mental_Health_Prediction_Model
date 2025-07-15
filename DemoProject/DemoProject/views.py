import joblib
import numpy as np
import pandas as pd
import pymysql
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


# Homepage View
def home(request):
    return render(request, "index.html")


# Registration View
def registration(request):
    msg = ""
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('emailID')
        password = request.POST.get('password')

        try:
            con = pymysql.connect(
                host='mysql-shambhavi-shambhaviasole9-python.h.aivencloud.com',
                port=10850,
                user='shambhavi',
                password='AVNS_HmvZ_bGZzAhYDISIpxY',
                database='shambhavidb',
                ssl={'ssl': {}}
            )
            with con.cursor() as curs:
                # Check if email already exists
                curs.execute("SELECT * FROM StudentRegistration WHERE emailID = %s", (email,))
                if curs.fetchone():
                    msg = "Email already registered."
                else:
                    insert_query = """
                        INSERT INTO StudentRegistration (fullname, emailID, password) 
                        VALUES (%s, %s, %s)
                    """
                    curs.execute(insert_query, (fullname, email, password))
                    con.commit()
                    msg = "Registration successful!"
        except Exception as e:
            msg = f"Error during registration: {e}"
        finally:
            con.close()

    return render(request, 'registration.html', {'message': msg})


# Login View

def login(request):
    if request.method == "POST":
        email = request.POST.get('emailID').strip()
        psw = request.POST.get('password').strip()
        print(f"DEBUG: Email={email}, Password={psw}")

        try:
            con = pymysql.connect(
                host='mysql-shambhavi-shambhaviasole9-python.h.aivencloud.com',
                port=10850,
                user='shambhavi',
                password='AVNS_HmvZ_bGZzAhYDISIpxY',
                database='shambhavidb',
                ssl={'ssl': {}}
            )
            curs = con.cursor()
            query = "SELECT studID FROM StudentRegistration WHERE emailID = %s AND password = %s"
            curs.execute(query, (email, psw))
            result = curs.fetchone()
            print("DEBUG: Login result =", result)

            if result:
                request.session['studID'] = result[0]
                return redirect('stdDashboard')
            else:
                return render(request, 'loginfailed.html', {'message': 'Invalid credentials'})

        except Exception as e:
            return render(request, 'stdDashboard.html', {'error': str(e)})
        finally:
            con.close()

    return render(request, 'login.html')



# Dashboard View
def stdDashboard(request):
    if 'studID' not in request.session:
        return redirect('login')
    return render(request, 'stdDashboard.html')


# Logout View
def logout(request):
    request.session.flush()  # clear session
    request.session.clear_expired()
    return render(request, "logout.html")


# Mental Health Prediction View
def mental_health_prediction(request):
    if request.method == 'POST':
        try:
            data = {
                'Gender': [int(request.POST.get('Gender'))],
                'Age': [int(request.POST.get('Age'))],
                'Education': [int(request.POST.get('Education'))],
                'ScreenTime': [float(request.POST.get('ScreenTime'))],
                'Sleep': [float(request.POST.get('Sleep'))],
                'Physical': [int(request.POST.get('Physical'))],
                'Stress': [int(request.POST.get('Stress'))],
                'Anxious': [int(request.POST.get('Anxious'))],
                'AcademicPerf': [int(request.POST.get('AcademicPerf'))]
            }

            df = pd.DataFrame(data)
            model = joblib.load('processed_student_mental_health.joblib')
            pred = model.predict(df)
            prediction = "Mentally Unfit" if pred[0] == 1 else "Mentally Fit"

            # Save result in session and redirect
            request.session['prediction_result'] = prediction
            return redirect('mental_health_result')

        except Exception as e:
            request.session['prediction_result'] = f"Error during prediction: {str(e)}"
            return redirect('mental_health_result')

    return render(request, "mental_health_form.html")


def mental_health_result(request):
    prediction = request.session.get('prediction_result', None)
    return render(request, "mental_health_result.html", {'prediction': prediction})


# Login Failed View (optional)
def loginfailed(request):
    return render(request, "loginfailed.html")
