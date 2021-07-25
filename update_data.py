'''
Update the course information data used by the application, scraping it from various websites.
Run from the repository's **parent** directory with -h or --help to view the help message and arguments.
'''

import argparse
import json

from .scrapers.available_courses import get_available_courses_dict
from .scrapers.course_information import get_course_information_dict
from .scrapers.course_statistics import get_course_statistics_dict
from .scrapers.grade_distributions_and_teaching_team import get_grade_distributions_and_teaching_team_dicts
from .scrapers.professors_information import get_professor_information_dict

DATA_DIR_PATH = 'ubc_course_explorer_data'
AVAILABLE_COURSES_FN = 'available_courses.json'
COURSE_INFORMATION_FN = 'course_information.json'
COURSE_STATISTICS_FN = 'course_statistics.json'
GRADE_DISTRIBUTIONS_FN = 'grade_distributions.json'
PROFESSOR_INFORMATION_FN = 'professors_information.json'
TEACHING_TEAM_FN = 'teaching_team.json'


def dump_json(filename, object):
    '''Saves an object to a json file in the root directory.'''
    with open(f"{DATA_DIR_PATH}/{filename}", 'w') as json_file:
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
    parser.add_argument('-d', '--grade_distributions_and_teaching_team',
                        help=f"update {GRADE_DISTRIBUTIONS_FN} and {TEACHING_TEAM_FN}", action='store_true')
    parser.add_argument('-p', '--professor_information', help=f"update {PROFESSOR_INFORMATION_FN}", action='store_true')
    args = parser.parse_args()

    if args.available_courses:
        j = get_available_courses_dict()
        dump_json(AVAILABLE_COURSES_FN, j)
    if args.course_information:
        j = get_course_information_dict()
        dump_json(COURSE_INFORMATION_FN, j)
    if args.course_statistics:
        j = get_course_statistics_dict()
        dump_json(COURSE_STATISTICS_FN, j)
    if args.grade_distributions_and_teaching_team:
        j1, j2 = get_grade_distributions_and_teaching_team_dicts()
        dump_json(GRADE_DISTRIBUTIONS_FN, j1)
        dump_json(TEACHING_TEAM_FN, j2)
    if args.professor_information:
        j = get_professor_information_dict()
        dump_json(PROFESSOR_INFORMATION_FN, j)
