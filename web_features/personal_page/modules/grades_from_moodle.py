from requests import post


class MoodleAPI:
    '''
    gets grades for assigments from moodle for each course
    '''
    TOKEN_URL = "https://moodle2.cs.huji.ac.il/nu21/login/token.php?service=moodle_mobile_app"
    MOODLE_API_URL = "https://moodle2.cs.huji.ac.il/nu21//webservice/rest/server.php?moodlewsrestformat=json"
    MOODLE_API_GRADES = ""
    RELEVANT_ASSIGNMENT_FIELDS = [
        'name',
        'course',
        'id',
        'cmid',
        'duedate',
        'timeclose'
    ]

    def __init__(self, username=None, public_token=None, private_token=None, userid=None):
        """
        Initialise the MoodleAPI object with default parameters, option to enter them manually
        @param public_token:
        @param private_token:
        @param userid:
        """
        self.public_token = public_token
        self.private_token = private_token
        self.userid = userid
        self.username = username

    def initialise(self, usr, pwd):
        """
        Initialise the MoodleAPI object with username and password
        @param usr:
        @param pwd:
        @return:
        """
        self.getToken(usr, pwd)
        self.get_userid()

    def getToken(self, usr, pwd):
        """
        Gets the public and private tokens based on username and password
        @param usr:
        @param pwd:
        @return:
        """
        cred = {"username": usr, "password": pwd}
        r = post(self.TOKEN_URL, data=cred)
        self.public_token, self.private_token = r.json()['token'], r.json()['privatetoken']

    def get_userid(self):
        """
        Gets the user-id based on token
        @return:
        """
        data = {"wstoken": self.public_token, "wsfunction": "core_webservice_get_site_info"}
        r = post(self.MOODLE_API_URL, data=data)
        self.userid = r.json()['userid']

    def get_grades(self, courses):
        '''
        gets the grades of assigments for each course
        :param courses list
        :return: courses: dict of {number course: {assigment name: grade}}
        '''
        final = {}
        for course in courses:
            data = {"wstoken": self.public_token,"userid": self.userid,"courseid" : course["id"],  "wsfunction": "gradereport_user_get_grade_items"}
            r = post(self.MOODLE_API_URL, data=data)
            data_course = r.json()
            for dict in data_course["usergrades"][0]["gradeitems"]:
                ex_name = dict["itemname"]
                grade = dict['graderaw']
                if grade != None: #if was graded already
                    if course["id"] in final:
                        final[course["id"]][ex_name] = grade
                    else:
                        final[course["id"]] = {ex_name: grade}

        return final

    def get_courses(self):
        """
        Gets a list of courses for these credentials
        @return: A dict of lists of dicts of... just print it if you ever need to use it
        """
        data = {"wstoken": self.public_token, "userid": self.userid, "wsfunction": "core_enrol_get_users_courses"}
        r = post(self.MOODLE_API_URL, data=data)
        return r.json()


