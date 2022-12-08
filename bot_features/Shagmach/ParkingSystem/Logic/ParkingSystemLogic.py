import requests as req
import datetime

### Setup ###
login_url = 'https://park.cs.huji.ac.il/login'
request_url = 'https://park.cs.huji.ac.il/reqform'
username = 'talpiot1'
my_headers = {'Referer': 'https://park.cs.huji.ac.il/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


class ParkingSystemLogic:
    @staticmethod
    def issue_permit(
            plate_num,
            date: datetime.datetime = datetime.datetime.now(),
            first_name='Talpiot',
            last_name='User',
            phone='0502758710',
            _email='madar.talpiot@gmail.com'):

        sess = req.Session()
        sess.headers.update(my_headers)

        ### Gets login page (and sets park cookie)
        res_login_page = sess.get(login_url)

        ### Fill the form and login (set auth tkts) ###
        form_data = {'came_from': '/',
                     'name': username,
                     'password': 'EDF123',
                     'form.submitted': 'Log In'}

        res_main_menu = sess.post(login_url, form_data)
        if 'Parking form' not in res_main_menu.text:
            return 'שגיאה בהתחברות למערכת. בדוק מילת קסם'

        ### Fill out the parking form and we're done ###
        sess.headers['Referer'] = 'https://park.cs.huji.ac.il/reqform'  # Make it look like we're a regular user
        form_data = dict(lp=plate_num, fname=first_name, lname=last_name, cell=phone, email=_email, co='', gates='1',
                         cal=date.strftime('%Y-%m-%d'))
        form_data['OK.x'] = '24'
        form_data['OK.y'] = '15'

        res_reqform = sess.post(request_url, form_data)

        if "Permit number is" in res_reqform.text:
            result = "אישור רכב הונפק בהצלחה ✅"
        elif "duplicate permit" in res_reqform.text:
            result = "לרכב כבר יש אישור כניסה לתאריך הרצוי ❕"
        else:
            result = "משהו השתבש. נסה ידנית ❌"

        return result
