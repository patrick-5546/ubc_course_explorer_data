from collections import defaultdict
import requests

from .constants import GR_API_URL, GR_CAMPUS


def get_grade_distributions_and_teaching_team_dicts():
    '''Returns a dictionary of the grade distributions for all courses to a json file.
        - Keys are course names: i.e, 'ENGL 100'
        - Values are lists of dictionaries, where the dictionaries are identical to the example below without the
          'campus', 'course', 'detail', 'educators', 'section', and 'subject' entries
            - Only the overall distributions are saved for each term the course is offered, not individual sections
            - Most recent sections are first

    Returns a dictionary of the teaching teams for all sections of all courses to a json file.
        - Keys are the course names: i.e., 'ENGL 100'
        - Values are dictionaries of lists
            - Keys are the sections number: i.e., '001'
            - Values are a list of professors that have taught that section, sorted by recency then alphabetically
    '''
    print('updating grade distributions and teaching team')

    grade_distrs_dict = defaultdict(list)  # default value of new keys is an empty list
    teaching_team_dict = defaultdict(lambda: defaultdict(list))  # default value of the new keys is defaultdict(list)
    for term in _get_available_terms_list():
        print(f"\tGetting the overall grade distributions for the courses in {term}")

        # list of dictionaries for each course section in a term, for example with term == '2020W'
        # {
        #     "average": 89.0,
        #     "campus": "UBCV",
        #     "course": "504",
        #     "course_title": "Research Methodology in Applied Animal Biology",
        #     "detail": "",
        #     "educators": "Daniel Weary;John Smith",
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
            course_name = (f"{term_grade_distr_dict['subject']} {term_grade_distr_dict['course']}"
                           f"{term_grade_distr_dict['detail']}")
            section = term_grade_distr_dict['section']

            # Use the 'OVERALL' section to get the grade distribution for a course
            if section == 'OVERALL':
                grade_distrs_dict[course_name].append({k: v for k, v in term_grade_distr_dict.items()
                                                       if k not in ['campus', 'course', 'detail', 'educators',
                                                                    'section', 'subject']})

            # Use the other sections to get the section teaching teams for a course
            else:
                # gets the new professors, filtering out empty strings
                new_profs_list = sorted(list(set([p for p in term_grade_distr_dict['educators'].split(';') if p])
                                             - set(teaching_team_dict[course_name][section])))
                teaching_team_dict[course_name][section].extend(new_profs_list)

    return grade_distrs_dict, teaching_team_dict


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
