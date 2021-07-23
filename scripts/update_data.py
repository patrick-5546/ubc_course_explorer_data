'''
Update the course information data used by the application, scraping it from various websites.
Run from the repository's root directory with -h or --help to view the help message and arguments.

Notes:
    - The gr prefix is for ubcgrades.com
    - The ex prefix is for ubcexplorer.io
    - The rmp prefix is for ratemyprofessors.com
'''

import argparse
from collections import defaultdict
import json
import os
import requests

# File paths
DATA_DIR_PATH = '.'  # files are located in the repository's root directory
AVAILABLE_COURSES_FN = 'available_courses.json'
COURSE_INFORMATION_FN = 'course_information.json'
COURSE_STATISTICS_FN = 'course_statistics.json'
GRADE_DISTRIBUTIONS_FN = 'grade_distributions.json'

# ubcgrades
GR_API_URL = 'https://ubcgrades.com/api/v2'
GR_CAMPUS = 'UBCV'

# ubcexplorer
EX_API_URL = 'https://ubcexplorer.io'


def update_available_courses_dict():
    '''Save a dictionary of the available courses to a json file at AVAILABLE_COURSES_PATH.
        - Keys are subjects: i.e., 'APSC'
        - Values are a list of their course labels: i.e., ['100', '101', '150', ...]
    '''
    print('updating available courses')

    avail_courses_dict = dict()
    for subject in _get_subjects_list():
        avail_courses_dict[subject] = _get_course_labels_list(subject)

    _dump_json(AVAILABLE_COURSES_FN, avail_courses_dict)


def _get_subjects_list():
    '''Returns a list of all distinct subjects across all terms.'''
    # list of dictionaries for each subject, for example
    # {
    #     "subject": "MATH",
    #     "subject_title": "Mathematics"
    # }
    url = f"{GR_API_URL}/subjects/{GR_CAMPUS}"
    subjects_list = requests.get(url).json()

    return [subject_dict['subject'] for subject_dict in subjects_list]


def _get_course_labels_list(subject):
    '''Returns a list of all distinct course labels in a subject.'''
    print(f"Getting the course labels list for {subject}")

    # list of dictionaries for each course in a subject, for example with subject == 'APSC'
    # {
    #     "course": "496",
    #     "course_title": "Interdisciplinary Engineering Design Project",
    #     "detail": "D"
    # }
    url = f"{GR_API_URL}/courses/{GR_CAMPUS}/{subject}"
    courses_list = requests.get(url).json()

    # Set comprehension was used because there are some entries with the same 'course' and 'detail' values, but
    # different 'course_title' values, as they could change across the years
    return sorted(list({f"{course_dict['course']}{course_dict['detail']}" for course_dict in courses_list}))


def update_course_information_dict():
    '''Saves a dictionary of the course information for all courses to a json file at COURSE_INFORMATION_PATH.
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

    _dump_json(COURSE_INFORMATION_FN, courses_info_dict)


def update_course_statistics_dict():
    '''Saves a dictionary of the course statistics for all courses to a json file at COURSE_STATISTICS_PATH.
        - Keys are course names: i.e, 'ENGL 100'
        - Values are dictionaries of information, identical to the example below without the 'campus', 'course',
          'detail', and 'subject' entries
    '''
    print('updating course statistics')

    course_stats_dict = dict()
    for subject in _get_subjects_list():
        print(f"Getting the course statistics for the courses in {subject}")

        # list of dictionaries for each course in a subject, for example with subject == 'ENGL'
        # {
        #     "average": 73.05126893958308,
        #     "average_past_5_yrs": 72.64875058959879,
        #     "campus": "UBCV",
        #     "course": "100",
        #     "course_title": "Reading and Writing about Literature",
        #     "detail": "",
        #     "faculty_title": "Faculty of Arts",
        #     "max_course_avg": 82.95652174,
        #     "min_course_avg": 64,
        #     "stdev": 11.995445807600767,
        #     "subject": "ENGL",
        #     "subject_title": "English"
        # }
        url = f"{GR_API_URL}/course-statistics/{GR_CAMPUS}/{subject}"
        sub_courses_stats_list = requests.get(url).json()

        course_stats_dict.update(
            {f"{sub_course_stats_dict['subject']} {sub_course_stats_dict['course']}{sub_course_stats_dict['detail']}":
             {k: v for k, v in sub_course_stats_dict.items() if k not in ['campus', 'course', 'detail', 'subject']}
             for sub_course_stats_dict in sub_courses_stats_list}
        )

    _dump_json(COURSE_STATISTICS_FN, course_stats_dict)


def update_grade_distributions_dict():
    '''Saves a dictionary of the grade distributions for all courses to a json file at GRADE_DISTRIBUTIONS_PATH.
        - Keys are course names: i.e, 'ENGL 100'
        - Values are lists of dictionaries, where the dictionaries are identical to the example below without the
          'campus', 'course', 'detail', 'section', and 'subject' entries
            - Only the overall distributions are saved for each term the course is offered, not individual sections
            - Most recent sections are first
    '''
    print('updating grade distributions')

    grade_distrs_dict = defaultdict(list)
    for term in _get_available_terms_list():
        print(f"Getting the overall grade distributions for the courses in {term}")

        # list of dictionaries for each course section in a term, for example with term == '2020W'
        # {
        #     "average": 89.0,
        #     "campus": "UBCV",
        #     "course": "504",
        #     "course_title": "Research Methodology in Applied Animal Biology",
        #     "detail": "",
        #     "educators": "Daniel Weary",
        #     "enrolled": 9,
        #     "faculty_title": "Faculty of Land and Food Systems",
        #     "grades": {
        #     "50-54%": 0, "55-59%": 0, ...
        #     },
        #     "high": 98,
        #     "low": 81,
        #     "section": "002",
        #     "session": "W",
        #     "stdev": 5.0,
        #     "subject": "AANB",
        #     "subject_title": "Applied Animal Biology",
        #     "year": "2020"
        # }
        url = f"{GR_API_URL}/grades/{GR_CAMPUS}/{term}"
        term_grade_distrs_list = requests.get(url).json()

        for term_grade_distr_dict in term_grade_distrs_list:
            if term_grade_distr_dict['section'] == 'OVERALL':
                course_name = (f"{term_grade_distr_dict['subject']} {term_grade_distr_dict['course']}"
                               f"{term_grade_distr_dict['detail']}")
                grade_distrs_dict[course_name].append({k: v for k, v in term_grade_distr_dict.items()
                                                       if k not in ['campus', 'course', 'detail',
                                                                    'section', 'subject']})

    _dump_json(GRADE_DISTRIBUTIONS_FN, grade_distrs_dict)


def _get_available_terms_list():
    '''Returns a list of all available terms from most to least recent.'''
    # list of terms, currently equal to
    # [
    # "2014S", "2014W", "2015S", "2015W", "2016S", "2016W", "2017S",
    # "2017W", "2018S", "2018W", "2019S", "2019W", "2020S", "2020W"
    # ]
    url = f"{GR_API_URL}/yearsessions/{GR_CAMPUS}"
    available_terms_list = requests.get(url).json()

    available_terms_list.reverse()
    return available_terms_list


def _dump_json(filename, object):
    path = os.path.join(DATA_DIR_PATH, filename)
    with open(path, 'w') as json_file:
        json.dump(object, json_file)
    print(f"Saved object to {path}\n")


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Update the files containing the course information data used by '
                                                 'the application, scraping it from various websites. Select which '
                                                 'files to update using the arguments below.')
    parser.add_argument('-c', '--available_courses', help=f"update {AVAILABLE_COURSES_FN}", action='store_true')
    parser.add_argument('-i', '--course_information', help=f"update {COURSE_INFORMATION_FN}", action='store_true')
    parser.add_argument('-s', '--course_statistics', help=f"update {COURSE_STATISTICS_FN}", action='store_true')
    parser.add_argument('-d', '--grade_distributions', help=f"update {GRADE_DISTRIBUTIONS_FN}", action='store_true')
    args = parser.parse_args()

    if args.available_courses:
        update_available_courses_dict()
    if args.course_information:
        update_course_information_dict()
    if args.course_statistics:
        update_course_statistics_dict()
    if args.grade_distributions:
        update_grade_distributions_dict()
