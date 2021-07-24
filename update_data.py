'''
Update the course information data used by the application, scraping it from various websites.
Run from the repository's root directory with -h or --help to view the help message and arguments.
'''

import argparse

from scrapers.available_courses import update_available_courses_dict
from scrapers.course_information import update_course_information_dict
from scrapers.course_statistics import update_course_statistics_dict
from scrapers.grade_distributions import update_grade_distributions_dict
from scrapers.professors_information import update_professor_information_dict
from scrapers.utilities import (
    AVAILABLE_COURSES_FN,
    COURSE_INFORMATION_FN,
    COURSE_STATISTICS_FN,
    GRADE_DISTRIBUTIONS_FN,
    PROFESSOR_INFORMATION_FN
)


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
        update_available_courses_dict(AVAILABLE_COURSES_FN)
    if args.course_information:
        update_course_information_dict(COURSE_INFORMATION_FN)
    if args.course_statistics:
        update_course_statistics_dict(COURSE_STATISTICS_FN)
    if args.grade_distributions:
        update_grade_distributions_dict(GRADE_DISTRIBUTIONS_FN)
    if args.professor_information:
        update_professor_information_dict(PROFESSOR_INFORMATION_FN)
