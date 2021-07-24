from collections import defaultdict
import json
import math
import requests

from .constants import RMP_API_URL, RMP_CAMPUS_ID


def get_professor_information_dict():
    '''Returns a dictionary of professor information for all professors to a json file.
    Adapted from https://github.com/Rodantny/Rate-My-Professor-Scraper-and-Search.
        - Keys are the professor first and last names: i.e., 'Robert Gateman'
        - Values are lists of dictionaries of information, identical to the example below without the 'tSid',
          'instituion_name', 'tFname', and 'tLname' entries
            - The middle name is often missing
            - There may be more than one element in the list (same first and last name), and there is not a way to tell
              if the elements represent the same person, or to match that name with the other sources
                - Thus, print the department beside the name if there are multiple entries: i.e., John Smith (Biology)
    '''
    print('updating professor information')

    profs_info_list = _get_professor_list()
    profs_info_dict = defaultdict(list)  # default value of new keys is an empty list
    for prof_info_dict in profs_info_list:
        prof_name = f"{prof_info_dict['tFname']} {prof_info_dict['tLname']}"
        profs_info_dict[prof_name].append({k: v for k, v in prof_info_dict.items()
                                           if k not in ['tSid', 'institution_name', 'tFname', 'tLname']})

    return profs_info_dict


def _get_professor_list():
    '''Returns a list of professor information for all professors.

    Professor information is in a dictionary (i.e., Robert Gateman)
    {
    'tDept': 'Economics',
    'tSid': '1413',
    'institution_name': 'University of British Columbia',
    'tFname': 'Robert',
    'tMiddlename': '',
    'tLname': 'Gateman',
    'tid': 13305,
    'tNumRatings': 1061,
    'rating_class': 'good',
    'contentType': 'TEACHER',
    'categoryType': 'PROFESSOR',
    'overall_rating': '3.7'
    }
    '''
    profs_info_list = list()
    num_profs = _get_num_profs()
    num_pages = math.ceil(num_profs / 20)
    for i in range(1, num_pages + 1):
        print(f"\tGetting professor information from page {i} out of {num_pages}")

        page = requests.get(f"{RMP_API_URL}/?&page={i}&filter=teacherlastname_sort_s+asc&query=*%3A*&"
                            f"queryoption=TEACHER&queryBy=schoolId&sid={RMP_CAMPUS_ID}")
        temp_jsonpage = json.loads(page.content)

        temp_list = temp_jsonpage['professors']
        profs_info_list.extend(temp_list)

    return profs_info_list


def _get_num_profs():
    '''Returns the number of professors.
    Adapted from https://github.com/Rodantny/Rate-My-Professor-Scraper-and-Search.
    '''
    page = requests.get(f"{RMP_API_URL}/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&"
                        f"queryoption=TEACHER&queryBy=schoolId&sid={RMP_CAMPUS_ID}")
    temp_jsonpage = json.loads(page.content)

    num_profs = temp_jsonpage['remaining'] + 20
    return num_profs
