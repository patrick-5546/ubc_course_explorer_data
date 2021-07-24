import json
import os

# CONSTANTS

# data files
DATA_DIR_PATH = '.'  # files are located in the repository's root directory
AVAILABLE_COURSES_FN = 'available_courses.json'
COURSE_INFORMATION_FN = 'course_information.json'
COURSE_STATISTICS_FN = 'course_statistics.json'
GRADE_DISTRIBUTIONS_FN = 'grade_distributions.json'
PROFESSOR_INFORMATION_FN = 'professors_information.json'

# ubcgrades
GR_API_URL = 'https://ubcgrades.com/api/v2'
GR_CAMPUS = 'UBCV'

# ubcexplorer
EX_API_URL = 'https://ubcexplorer.io'

# rmp
RMP_API_URL = 'http://www.ratemyprofessors.com/filter/professor'
RMP_CAMPUS_ID = 1413


def dump_json(filename, object):
    '''Saves an object to a json file.'''
    path = os.path.join(DATA_DIR_PATH, filename)
    with open(path, 'w') as json_file:
        json.dump(object, json_file)
    print(f"Saved object to {path}\n")
