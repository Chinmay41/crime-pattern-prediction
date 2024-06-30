from flask import Flask, render_template, request
import pickle
import numpy as np

model = pickle.load(open('MLP.pkl', 'rb'))

app = Flask(__name__)



@app.route('/')
def man():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def home():
    hour = request.form['a']
    day = request.form['b']
    month = request.form['c']
    year = request.form['d']
    street = request.form['e']
    

    hour = int(hour)
    day = int(day)
    month = int(month)
    year = int(year)
    street = int(street)
   

    def hourzone(hour):
        if ((hour >=2) and (hour < 8)):
            return 0
        elif hour >= 8 and hour < 12:
            return 1
        elif hour >= 12 and hour < 18:
            return 2
        elif hour >= 18 and hour < 22:
            return 3
        elif hour < 2 or hour >= 22:
            return 4

    def pd_dist(street):
        if street==1 or street==3:
            return 5
        if street==6 or street==7 or street==16 or street==18 or street==0:
            return 0
        if street==9:
            return 2
        if street==15 or street==4:
            return 8
        if street==19 or street==5:
            return 7
        if street==2:
            return 1
        if street==14:
            return 3
        if street==10 or street==17:
            return 4
        if street==8 or street==11:
            return 6
        if street==12 or street==13:
            return 9

    def resol(pd_dist1):
        return pd_dist(pd_dist1)+1

    def xx(street):
        match street:
            case 0:
                return  0.527595
            case 1:
                return -0.440796
            case 2:
                return -1.018001
            case 3:
                return 0.527807
            case 4:
                return  0.834224
            case 5:
                return -1.561166
            case 6:
                return -2.714558
            case 7:
                return -3.186468
            case 8:
                return 2.265083
            case 9:
                return 0.270347
            case 10:
                return 0.584743
            case 11:
                return 0.372691
            case 12:
                return 0.098308
            case 13:
                return 0.335841
            case 14:
                return 1.726117
            case 15:
                return -2.437608
            case 16:
                return -0.190084
            case 17:
                return -1.920058
            case 18:
                return -1.694927
            case 19:
                return -0.3638116

    def yy(street):
        match street:
            case 0:
                return 0.578001
            case 1:
                return 0.482829
            case 2:
                return -0.235725
            case 3:
                return -0.868788
            case 4:
                return -1.060086
            case 5:
                return -0.775427
            case 6:
                return  0.792554
            case 7:
                return -0.090579
            case 8:
                return 1.752882
            case 9:
                return -1.35869
            case 10:
                return -0.501800
            case 11:
                return 0.941348
            case 12:
                return 0.170593
            case 13:
                return 0.514207
            case 14:
                return -1.431083
            case 15:
                return 0.752409
            case 16:
                return -0.359402
            case 17:
                return -2.224840
            case 18:
                return -1.218655
            case 19:
                return -2.316848

    def business(hour):
        if 8<= hour <=18:
            return 1
        else:
            return 0

    def holi(date):
        from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
        cal = calendar()
        holidays = cal.holidays(date)
        holiday = date["d"].dt.date.astype('datetime64[ns]').isin(holidays)
        print(type(eval(holiday)))
        if holiday==True:
            return 1
        else:
            return 0

    def cat(op):
        d=dict()
        d = {16:"LARCENY/THEFT", 21:"OTHER OFFENSES", 20:"NON-CRIMINAL", 1:"ASSAULT", 7:"DRUG/NARCOTI", 36:"VEHICLE THEFT", 35:"VANDALISM", 37:"WARRANTS", 4:"BURGLARY", 32:"SUSPICIOUS OCC", 19:"MISSING PERSON", 25:"ROBBERY", 13:"FRAUD", 12:"FORGERY/COUNTERFEITING", 27:"SECONDARY CODES", 38:"WEAPON LAWS", 23:"PROSTITUTION", 34:"TRESPASS", 30:"STOLEN PROPERTY", 28:"SEX OFFENSES FORCIBLE",5:"DISORDERLY CONDUCT", 8:"DRUNKENNESS", 24:"RECOVERED VEHICLE", 15:"KIDNAPPING", 6:"DRIVING UNDER THE INFLUENCE", 26:"RUNAWAY", 17:"LIQUOR LAWS", 0:"ARSON", 18:"LOITERING", 9:"EMBEZZLEMENT", 31:"SUICIDE", 11:"FAMILY OFFENSES", 2:"BAD CHECKS", 3:"BRIBERY", 10:"EXTORTION", 29:"SEX OFFENSES NON FORCIBLE", 14:"GAMBLING", 22:"PORNOGRAPHY/OBSCENE MAT", 33:"TREA"}
        for i in range(0,37):
            if i==op:
                print(d[op])

    def pred(hour, day, month, year, street):
        # Hour Zone 0 - Pass midnight, 1 - morning, 2 - afternoon, 3 - dinner / sun set, 4 - night
        pd_district = pd_dist(street)
        resolution = resol(pd_district)
        x = xx(street)
        y = yy(street)

        hour_zone = hourzone(hour)
        day_of_week = day%7
        business_hour = business(hour)
        weekend = 0
        holiday = 0
        op = model.predict([[day_of_week, pd_district, resolution, x, y, day, month, year,hour, hour_zone, holiday, business_hour, weekend, street]])
        return op

    #arr1 = np.array([[day_of_week, pd_district, resolution, x, y, day, month, year,hour, hour_zone, holiday, business_hour, weekend, street]])




    #arr = np.array([[hour, day, month, year, street]])



    

    pred1 = pred(hour, day, month, year, street)
   #return render_template('after.html', data=pred1)
    if pred1 is not None:
        return render_template('after.html', data=pred1)
    else:
        # Handle the case where pred1 is None, e.g., by displaying an error message
        return render_template('error.html')



if __name__ == "__main__":
    app.run(debug=True)