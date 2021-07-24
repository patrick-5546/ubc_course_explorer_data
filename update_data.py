'''
Update the course information data used by the application, scraping it from various websites.
Run from the repository's root directory with -h or --help to view the help message and arguments.
'''

import argparse
import json

from scrapers.available_courses import get_available_courses_dict
from scrapers.course_information import get_course_information_dict
from scrapers.course_statistics import get_course_statistics_dict
from scrapers.grade_distributions import get_grade_distributions_dict
from scrapers.professors_information import get_professor_information_dict
from scrapers.constants import (
    AVAILABLE_COURSES_FN,
    COURSE_INFORMATION_FN,
    COURSE_STATISTICS_FN,
    GRADE_DISTRIBUTIONS_FN,
    PROFESSOR_INFORMATION_FN
)

def dump_json(filename, object):
    '''Saves an object to a json file in the root directory.'''
    with open(filename, 'w') as json_file:
        json.dump(object, json_file)
    print(f"Saved object to {filename}")


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Update the files containing the course information data used by '
                                                 'the application, scraping it from various websites. Select which '
                                                 'files to update using the arguments below.')
    parser.add_argument('-c', '--available_courses', help=f"update {AVAILABLE_COURSES_FN}", action='store_true')
    parser.add_argument('-i', '--course_information', help=f"update {COURSE_INFORMATION_FN}", action='store_true')
    parser.add_argument('-s', '--course_statistics', help=f"update {COURSE_STATISTICS_FN}", action='store_true')
    parser.add_argument('-d', '--grade_distributions', help=f"update {GRADE_DISTRIBUTIONS_FN}", action='store_true')
    parser.add_argument('-p', '--professor_information', help=f"update {PROFESSOR_INFORMATION_FN}", action='store_true')
    args = parser.parse_args()

    if args.available_courses:
        dump_json(AVAILABLE_COURSES_FN, get_available_courses_dict())
    if args.course_information:
        dump_json(COURSE_INFORMATION_FN, get_course_information_dict())
    if args.course_statistics:
        dump_json(COURSE_STATISTICS_FN, get_course_statistics_dict())
    if args.grade_distributions:
        dump_json(GRADE_DISTRIBUTIONS_FN, get_grade_distributions_dict())
    if args.professor_information:
        dump_json(PROFESSOR_INFORMATION_FN, get_professor_information_dict())
