from collections import defaultdict
import requests

from scrapers.utilities import GR_API_URL, GR_CAMPUS, GRADE_DISTRIBUTIONS_FN, dump_json


def update_grade_distributions_dict():
    '''Saves a dictionary of the grade distributions for all courses to a json file.
        - Keys are course names: i.e, 'ENGL 100'
        - Values are lists of dictionaries, where the dictionaries are identical to the example below without the
          'campus', 'course', 'detail', 'section', and 'subject' entries
            - Only the overall distributions are saved for each term the course is offered, not individual sections
            - Most recent sections are first
    '''
    print('updating grade distributions')

    grade_distrs_dict = defaultdict(list)  # dictionary where the default value of new keys is an empty list
    for term in _get_available_terms_list():
        print(f"\tGetting the overall grade distributions for the courses in {term}")

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

    dump_json(GRADE_DISTRIBUTIONS_FN, grade_distrs_dict)


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
