import requests

from scrapers.utilities import EX_API_URL, COURSE_INFORMATION_FN, dump_json


def update_course_information_dict():
    '''Saves a dictionary of the course information for all courses to a json file.
        - Keys are course names: i.e, 'MATH 210'
        - Values are dictionaries of information, identical to the example below without the 'dept', 'code', and 'link'
          entries
            - Will manually form link from course subject, number, and detail, as this API does not use detail
    '''
    print('updating course information')

    # list of dictionaries for each course, for example
    # {
    # "preq": [
    #     "MATH 101", ...
    # ],
    # "creq": [
    #     "MATH 215", ...
    # ],
    # "depn": [
    #     "CPSC 203", ...
    # ],
    # "_id": "5eb76d718ade8b27172d6363",
    # "dept": "MATH",
    # "code": "MATH 210",
    # "name": "Introduction to Mathematical Computing",
    # "cred": 3,
    # "desc": "Course Description",
    # "prer": "One of MATH 101, MATH 103, MATH 105, MATH 121, SCIE 001.",
    # "crer": "One of MATH 215, MATH 255, MATH 256, MATH 258 and one of MATH 152, MATH 221, MATH 223.",
    # "link": "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept=MATH&course=210"
    # }
    url = f"{EX_API_URL}/getAllCourses"
    courses_info_list = requests.get(url).json()

    courses_info_dict = {course_info_dict['code']: {k: v for k, v in course_info_dict.items()
                         if k not in ['dept', 'code', 'link']} for course_info_dict in courses_info_list}

    dump_json(COURSE_INFORMATION_FN, courses_info_dict)
