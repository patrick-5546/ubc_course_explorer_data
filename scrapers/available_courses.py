import requests

from scrapers.utilities import GR_API_URL, GR_CAMPUS, AVAILABLE_COURSES_FN, dump_json


def update_available_courses_dict():
    '''Save a dictionary of the available courses to a json file.
        - Keys are subjects: i.e., 'APSC'
        - Values are a list of their course labels: i.e., ['100', '101', '150', ...]
    '''
    print('updating available courses')

    avail_courses_dict = dict()
    for subject in get_subjects_list():
        avail_courses_dict[subject] = _get_course_labels_list(subject)

    dump_json(AVAILABLE_COURSES_FN, avail_courses_dict)


def get_subjects_list():
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
    print(f"\tGetting the course labels list for {subject}")

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
