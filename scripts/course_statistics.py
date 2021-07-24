import requests

from available_courses import get_subjects_list
from utilities import GR_API_URL, GR_CAMPUS, COURSE_STATISTICS_FN, dump_json


def update_course_statistics_dict():
    '''Saves a dictionary of the course statistics for all courses to a json file.
        - Keys are course names: i.e, 'ENGL 100'
        - Values are dictionaries of information, identical to the example below without the 'campus', 'course',
          'detail', and 'subject' entries
    '''
    print('updating course statistics')

    course_stats_dict = dict()
    for subject in get_subjects_list():
        print(f"\tGetting the course statistics for the courses in {subject}")

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

    dump_json(COURSE_STATISTICS_FN, course_stats_dict)
