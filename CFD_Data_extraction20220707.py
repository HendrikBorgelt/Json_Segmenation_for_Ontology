import collections
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from collections import OrderedDict
import re
import time


def determining_dividers_reoccurring_lines_convergence(section_convergence: list[str]) -> list[int]:
    """
    determines the dividers which are used to cut the section into timescale tableaux and iteration tableaux
    :param section_convergence: list of string containing only timescale and iteration step text except for CPU
    ending indicator
    :return: list of
    """
    section_div_conv = []
    for line_con_1 in range(len(section_convergence)):
        if '===' in section_convergence[line_con_1]:
            section_div_conv.append(line_con_1)
        elif 'CFD' in section_convergence[line_con_1]:
            section_div_conv.append(line_con_1)
    return section_div_conv


def trimming_sections_conv(section_div_conv: list[int], section_convergence: list[str]) -> dict[list[str]]:
    """
    trims list of string into list of lists of strings separating timescale tableaux and iteration tableaux into
    separate lists
    :param section_div_conv:
    :param section_convergence:
    :return:
    """
    dict_conv_sec = {}
    for secs_conv in range(len(section_div_conv) - 1):
        # todo function split_conv_sections extract boxes in them and evaluate tableaux style text
        next_section_conv = section_convergence[(section_div_conv[secs_conv] + 1):(section_div_conv[secs_conv + 1] - 1)]
        dict_conv_sec_next = {secs_conv: next_section_conv}
        dict_conv_sec.update(dict_conv_sec_next)
    return dict_conv_sec


def segmenting_sections_conv(dict_conv_sec: dict[int, list[str]]) -> tuple[dict[int, list[str]],
                                                                           dict[int, list[str]],
                                                                           list[str]]:
    """
    Takes segmented dict with list of string from convergence section and returns a dictionary of the Iterations
    steps and or the Timescale settings, as well as a list of segments it has identified
    :param dict_conv_sec: dict of separated segments
    :return: dict of iteration segments, dict of timescale segments, list of found segments
    """
    dict_conv_time = {}
    dict_conv_loop = {}
    n_conv_time = 0
    n_conv_loop = 0
    list_of_convergence_segments = []
    for dict_len in range(len(dict_conv_sec) - 1):
        if 'Timescale' in dict_conv_sec[dict_len][0]:
            n_conv_time += 1
            dict_conv_time.update({n_conv_time: dict_conv_sec[dict_len][:]})
            list_of_convergence_segments.append('Timescale')
        elif 'OUTER LOOP' in dict_conv_sec[dict_len][0]:
            n_conv_loop += 1
            dict_conv_loop.update({n_conv_loop: dict_conv_sec[dict_len][:]})
            list_of_convergence_segments.append('OUTER LOOP')
    return dict_conv_time, dict_conv_loop, list_of_convergence_segments


def convergence_internal_to_dict_iterations(dict_conv_loop: dict[int, list[str]]) -> dict[int, dict[str, list[str]]]:
    """
    Converts interation step text into dictionaries containing the information
    :param dict_conv_loop: dict of text lines of iteration steps
    :return: dict of tableaux of iteration steps
    """
    dict_conv_loop_it = {}
    for len_dict_loop in range(len(dict_conv_loop)):
        number_loop = dict_conv_loop[len_dict_loop + 1][0][
                      :dict_conv_loop[len_dict_loop + 1][0].index('C')].strip().split('=')
        cpu_time_loop = dict_conv_loop[len_dict_loop + 1][0][
                        dict_conv_loop[len_dict_loop + 1][0].index('C') - 1:].strip().split('=')
        number_loop = [s.strip() for s in number_loop]
        cpu_time_loop = [s.strip() for s in cpu_time_loop]
        dict_conv_loop_it.update(
            {(len_dict_loop + 1): {number_loop[0]: number_loop[1], cpu_time_loop[0]: cpu_time_loop[1]}})
        int_list_dict_loop = []
        for len_dict_loop_int in range(len(dict_conv_loop[len_dict_loop + 1]) - 1):
            if '----' not in dict_conv_loop[len_dict_loop + 1][len_dict_loop_int + 1]:
                dict_conv_loop_int = dict_conv_loop[len_dict_loop + 1][len_dict_loop_int + 1].strip()[1:-1].split('|')
                dict_conv_loop_int = [s.strip() for s in dict_conv_loop_int]
                int_list_dict_loop.append(dict_conv_loop_int)
        for i in list(int_list_dict_loop[1:]):
            if len(i) == 1:
                int_list_dict_loop.pop(int_list_dict_loop.index(i))
        numpy_array = np.array(int_list_dict_loop[1:]).T.tolist()
        dict_out_loop = dict(zip(int_list_dict_loop[0], numpy_array))
        dict_conv_loop_it[len_dict_loop + 1].update(dict_out_loop)
        # todo here the conversion of values from string to integer would be possible
    return dict_conv_loop_it


def convergence_internal_to_dict_time(dict_conv_time: dict[int, list[str]],
                                      pos_number: list[int]) -> dict[int, dict[str, list[str] | int]]:
    """
    converts sections of timescale into dictionaries and assigns the timescales the iteration number at which they
    change
    :param dict_conv_time: Dictionary of timescale listing
    :param pos_number: position of timescale change measured on iteration steps
    :return: dict of timescale tableaux
    """
    dict_conv_time_it = {}
    for len_dict_time in range(len(dict_conv_time)):
        dict_conv_time_it.update(
            {(len_dict_time + 1): {'TIMESCALE': pos_number[len_dict_time]}})
        int_list_dict_time = []
        for len_dict_time_int in range(len(dict_conv_time[len_dict_time + 1]) - 1):
            if '----' not in dict_conv_time[len_dict_time + 1][len_dict_time_int + 1]:
                dict_conv_time_int = dict_conv_time[len_dict_time + 1][len_dict_time_int + 1].strip()[1:-1].split('|')
                dict_conv_time_int = [s.strip() for s in dict_conv_time_int]
                int_list_dict_time.append(dict_conv_time_int)
        numpy_array = np.array(int_list_dict_time[1:]).T.tolist()
        dict_out_time = dict(zip(int_list_dict_time[0], numpy_array))
        dict_conv_time_it[len_dict_time + 1].update(dict_out_time)
    return dict_conv_time_it


def finding_sub_sub_sections_in_convergence(convergence_section: list[str]) -> list[list[str]]:
    """
    divides convergence section into reoccurring and none reoccurring segments, reoccurring = iteration & Timescale
    :param convergence_section: list of strings containing the convergence tables
    :return:
    """
    segmenting_line = [0]
    sections = []
    for lines_1 in range(len(convergence_section) - 2):
        if bool(re.search('[=]{70}', convergence_section[lines_1])) & bool(
                re.search('[=]{70}', convergence_section[lines_1 + 2])):
            segmenting_line.append(lines_1 + 1)
    segmenting_line.append(len(convergence_section))
    for lines_2 in range(len(segmenting_line) - 1):
        sections.append(convergence_section[segmenting_line[lines_2]: segmenting_line[lines_2 + 1]])
        if bool(re.search('[=]{70}', sections[lines_2][-1])):
            sections[lines_2].pop(-1)
    return sections


def convergence_list_to_position_numbers(list_of_convergence_segments: list[str]) -> [list[int]]:
    """
    function determining the position number for the timescale setting compared to the iteration steps
    :param list_of_convergence_segments: ordered list of convergence tables
    :return: position list of timescale changes
    """
    pos_number = []
    for line in range(len(list_of_convergence_segments)):
        if 'Timescale' in list_of_convergence_segments[line]:
            pos_number.append(line - len(pos_number))
    return pos_number


def convergence_to_dict(section_convergence: list[str]) -> dict:
    """
    general function for converting 'Convergence' segment into table like structure inside dict
    :param section_convergence: list of strings containing convergence section
    :return: dict separated into Iteration-, Timescale- and CPU-time-steps
    """
    sub_sub_sections = finding_sub_sub_sections_in_convergence(section_convergence)
    section_div_conv = determining_dividers_reoccurring_lines_convergence(sub_sub_sections[0])
    dict_conv_sec = trimming_sections_conv(section_div_conv, section_convergence)
    dict_conv_time, dict_conv_loop, list_of_convergence_segments = segmenting_sections_conv(dict_conv_sec)
    dict_conv_loop_it = convergence_internal_to_dict_iterations(dict_conv_loop)
    pos_number = convergence_list_to_position_numbers(list_of_convergence_segments)
    dict_conv_time_it = convergence_internal_to_dict_time(dict_conv_time, pos_number)
    dict_out = {'Iterations': dict_conv_loop_it,
                'Timescale': dict_conv_time_it,
                'CPU': {section_convergence[-2].split(':')[0].strip():
                            section_convergence[-2].split(':')[-1].strip(),
                        section_convergence[-1].split(':')[0].strip():
                            section_convergence[-1].split(':')[-1].strip()}}
    return dict_out


def line_to_diction_comm_lang(line_lang: str) -> dict:
    """
    function for converting line into keyword: value assignement
    :param line_lang: string containing assignment sign (':','=')
    :return: dictionary
    """
    if ':' in line_lang:
        a = line_lang.split(':')
    elif '=' in line_lang:
        a = line_lang.split('=')
    else:
        line_lang = line_lang + '= ERROR'
        a = line_lang.split('=')
    if a[1].strip() == '':
        a[1] = 'EMPTY'
    dict_from_line = {a[0].strip(): a[1].lstrip()}
    return dict_from_line


def update_key(to_be_updated_dict: dict, content_dict: dict, key: str, *subkey: str) -> dict:
    """
    function for determining whether a dictionary must be nested into a sub key or can be directly assigned to a key
    :param to_be_updated_dict:
    :param content_dict:
    :param key:
    :param subkey: optional variable
    :return:
    """
    if subkey:
        to_be_updated_dict[key][subkey[0]].update(content_dict)
    elif to_be_updated_dict[key] != 'EMPTY':
        to_be_updated_dict[key].update(content_dict)
    else:
        to_be_updated_dict[key] = content_dict
    return to_be_updated_dict


def get_subsection_comm_lang(section_text_int: list[str]) -> list[str]:
    """
    determines and returns sections of the same indentation
    :param section_text_int: list of text after current line
    :return: list of text up to next indentation of same level
    """
    found_type_int_fun = True
    current_indentation_fun = len(section_text_int[0]) - len(section_text_int[0].lstrip())
    sub_section = []
    for line_int in range(len(section_text_int)):
        indentation = len(section_text_int[line_int]) - len(section_text_int[line_int].lstrip())
        if found_type_int_fun:
            if 'END' in section_text_int[line_int] and (indentation == current_indentation_fun):
                t_line_int = section_text_int[line_int].rstrip('\n')
                sub_section.append(t_line_int)
                break
            elif indentation < current_indentation_fun:
                break
            else:
                t_line_int = section_text_int[line_int].rstrip('\n')
                sub_section.append(t_line_int)
    return sub_section


def comm_lang_to_dict(section: list[str], indent_current: int) -> OrderedDict:
    """
    Recursive function for converting dictionary like structure of the command language into a nested dictionary.
    Recursive structure was used to achive nested structure. Function is quiet unwieldy as the dictionary structur
    contains keywords with direct assignment (keyword1 = assignment2:{keyword2: assignment2})
    :param section: list of text for a recursive calling only a subsegment of the text)
    :param indent_current: integer of the current indentation value inside the list of strings
    :return: OrderedDict with data extracted from the dictionary-like structure from the .out-files
    """

    section_int = section
    section_indent = indent_current + 2
    dict_test = OrderedDict()
    last_key = ""
    dict_test_indent = OrderedDict()
    last_sub_key = ""
    while section_int:
        current_indent = len(section_int[0]) - len(section_int[0].strip())
        if dict_test_indent == OrderedDict():
            pass
        elif last_sub_key:
            dict_test = update_key(dict_test, dict_test_indent, last_key, last_sub_key)
        else:
            dict_test = update_key(dict_test, dict_test_indent, last_key)

        if 'END' in section_int[0]:
            section_int.pop(0)
        elif not section_indent < current_indent:  # parallel
            check_existing_keys = list(line_to_diction_comm_lang(section_int[0]))[
                0]
            if check_existing_keys in dict_test.keys():  # if key already exists create NEW subkey
                try:
                    dict_test[check_existing_keys][last_sub_key].update(dict_test_indent)
                except:
                    pass
                dict_test[check_existing_keys].update({list(line_to_diction_comm_lang(section_int[0]).items())[-1][-1]:
                                                       OrderedDict()})
                last_key = check_existing_keys
                last_sub_key = list(line_to_diction_comm_lang(section_int[0]).items())[-1][-1]
            elif bool(list(line_to_diction_comm_lang(section_int[0]).items())[-1][-1] != 'EMPTY') \
                    & bool(re.search(':', section_int[0])):
                # if key not empty create FIRST subkey
                dict_test.update({list(line_to_diction_comm_lang(section_int[0]))[-1]:
                                  {list(line_to_diction_comm_lang(section_int[0]).items())[-1][-1]:
                                   OrderedDict()}})
                last_key = check_existing_keys
                last_sub_key = list(line_to_diction_comm_lang(section_int[0]).items())[-1][-1]
            else:
                dict_test.update({list(line_to_diction_comm_lang(section_int[0]))[0]:
                                  list((line_to_diction_comm_lang(section_int[0])).items())[-1][-1]})
                last_key = check_existing_keys
                last_sub_key = []
            dict_test_indent = OrderedDict()
            section_int.pop(0)

        else:  # indented
            next_section = get_subsection_comm_lang(section_int)
            next_section_key = list(line_to_diction_comm_lang(next_section[0]).items())[0][0]
            len_int = len(next_section)
            if next_section_key in dict_test_indent.keys():
                dict_test_indent[next_section_key].update(
                    comm_lang_to_dict(next_section, section_indent)[next_section_key])
            else:
                dict_test_indent = comm_lang_to_dict(next_section, section_indent)
            del section_int[:len_int]
    if dict_test_indent == OrderedDict():
        pass
    elif last_sub_key:
        dict_test = update_key(dict_test, dict_test_indent, last_key, last_sub_key)
    else:
        dict_test = update_key(dict_test, dict_test_indent, last_key)
    return dict_test


class Segmenting:
    """
    Class for assisting in Segmenting text into its different structures (CEL dictionary, Convergence tables, text,
    box, table)
    """

    def __init__(self, section: list):
        self.section = section
        self.line = []
        self.statement = []
        self.check, self.keyword = self.check_and_return_main_sections()

    @staticmethod
    def test_line_for_keyword_start_and_ending(section_line: str) -> bool:
        """
        checks if a line is part of a header or subheader, by checking if it is a dashed line in a box
        :param section_line: Line to be checked
        :return: bool, True for "dashed box" line
        """
        statement = False
        if section_line:
            if bool('+' in section_line[-1]):  # & bool('+' in Section_all[line][0]):
                if section_line[1]:
                    if '+' in section_line[1]:
                        if not section_line[2:-2].strip('-'):
                            statement = True
        return statement

    @staticmethod
    def test_line_for_keyword_spacing(section_line: str) -> bool:
        """
        checks if a line is part of a header, by checking if it is a blank line in a box
        :param section_line: Line to be checked
        :return: bool, True for "blank box" line
        """
        statement = False
        if section_line:
            if bool('|' in section_line[-1]):
                if section_line[1]:
                    if '|' in section_line[1]:
                        if not section_line[2:-2].strip():
                            statement = True
        return statement

    def check_and_return_main_sections(self) -> tuple[bool, str]:
        """
        function checking whether a line is a section header or not and returning the string of the header
        :return: tuple of (bool True if found, line subheader)
        """
        check = False
        keyword = []
        if self.test_line_for_keyword_start_and_ending(self.section[0]) & self.test_line_for_keyword_start_and_ending(
                self.section[4]):
            if self.test_line_for_keyword_spacing(self.section[1]) & self.test_line_for_keyword_spacing(
                    self.section[3]):
                if self.section[3]:
                    if not bool('--' in self.section[2].strip().lstrip('|').rstrip('|')):
                        keyword = self.section[2].strip().lstrip('|').rstrip('|').strip()
                        check = True
        return check, keyword

    def check_and_return_subsection(self) -> tuple[bool, str]:
        """
        function checking whether a line is a section subheader or not and returning the string of the subheader
        :return: tuple of (bool True if found, line header)
        """
        check = False
        keyword = []
        if bool('' in self.section[0]) & bool('' in self.section[4]):
            if self.test_line_for_keyword_start_and_ending(
                    self.section[1]) & self.test_line_for_keyword_start_and_ending(self.section[3]):
                if self.section[2]:
                    if not (bool('--' in self.section[2].strip().lstrip('|').rstrip('|')) | bool(
                            '|' in self.section[2].strip().lstrip('|').rstrip('|'))):
                        keyword = self.section[2].strip().lstrip('|').rstrip('|').strip()
                        check = True
        return check, keyword


def determining_sections(file_text_cleaned: list) -> tuple[list[int], list[str]]:
    """
    determines the header title and line where the header is written
    :param file_text_cleaned: list
    :return: list of line numbers, list of section headers titles
    """
    dividing_lines = []
    dividing_lines_header = ['Initialization']
    for line in range(len(file_text_cleaned) - 5):
        test = Segmenting(file_text_cleaned[line:line + 5])
        if test.check_and_return_main_sections()[0]:
            dividing_lines.append(line + 2)
            dividing_lines_header.append(test.check_and_return_main_sections()[1])
    dividing_lines.append(len(file_text_cleaned))
    return dividing_lines, dividing_lines_header


def dividing_into_sections(file_text_cleaned: list[str], dividing_lines: list[int]) -> list[list[str]]:
    """
    Divides list of text into list of segments which in return are lists of strings
    :param file_text_cleaned: cleaned list of text
    :param dividing_lines: list of line number for segmenting text into sections
    :return: list of sections (list) of text
    """
    sub_sections = []
    last_entry = 0
    for entries in dividing_lines:
        sub_sections.append(file_text_cleaned[last_entry:entries])
        last_entry = entries
    return sub_sections


def clean_end_of_subsection(subsection_list: list) -> list:
    """
    Cleans subsection by removing subheader box remains at the end
    :param subsection_list: List of strings of a subsection segment
    :return: List without box remains
    """
    for line in reversed(subsection_list[-2:]):
        if bool(line != '') & (
                bool(line.strip().strip('|').strip() == '') or bool(line.strip().strip('+').strip('-') == '')):
            subsection_list = subsection_list[:-1]
    if len(subsection_list[-4:]) == 4:
        for line_1 in reversed(subsection_list[-4:]):
            if line_1.strip() == '':
                subsection_list = subsection_list[:-1]
            else:
                break
    return subsection_list


def clean_start_of_subsection(subsection_list):
    """
        Cleans subsection by removing subheader box remains at the start
        :param subsection_list: List of strings of a subsection segment
        :return: List without box remains
    """
    table_found = False
    for line in subsection_list[:2]:
        if (bool(line != '') | bool(line != ' ')) & (bool(line.count('|') == 2)):
            subsection_list = subsection_list[1:]
            table_found = True
    if table_found:
        subsection_list = subsection_list[1:]
    for line_1 in subsection_list[:len(subsection_list)]:
        if bool(line_1 == '') or bool(line_1 == ' '):
            subsection_list = subsection_list[1:]
        else:
            break
    return subsection_list


def line_to_diction(line: str) -> dict:
    """
    function converting line into keyword-value relation called dict
    :param line: line in form of a string
    :return: dictionary of assigned concepts
    """
    if ':' in line:
        a = line.split(':')
    elif '=' in line:
        a = line.split('=')
    else:
        line = line + '= ERROR'
        a = line.split('=')
    dict_from_line = {a[0].strip(): a[1].lstrip()}
    return dict_from_line


def table_lines_to_content(section_lines: list[str]) -> tuple[list[list], list[int], list[int]]:
    """
    function extracting table content and counting cells inside table
    :param section_lines:
    :return:
    """
    content = []
    multicolumn = False
    counter_1 = 0
    line_counter = []
    column_counter = []
    for line in section_lines:
        counter_2 = 0
        if multicolumn:
            multicolumn = False
            added_content = [i.strip() for i in line.strip().strip('|').split('|')]
            line_counter.append(counter_1)
            for to_be_edited_lines in range(len(content[-1])):
                content[-1][to_be_edited_lines] += added_content[to_be_edited_lines]
            continue
        if '|' not in line:
            continue
        else:
            line_content = [i.strip() for i in (''.join(line[1:])).strip('|').split('|')]
            new_line_content = []
            for iterator in range(len(line_content)):
                if re.search('([+][-])+', line_content[iterator]) is not None:
                    split_iterator = line_content[iterator].split('+-')
                    for line_iterator in range(len(split_iterator)):
                        if re.search('([-])+', split_iterator[line_iterator]) is not None:
                            split_iterator[line_iterator] = ''
                    new_line_content.extend(split_iterator)
                    multicolumn = True
                    column_counter.append(counter_2)
                else:
                    new_line_content.append(line_content[iterator])
                counter_2 += 1
            content.append(new_line_content)
        counter_1 += 1
    return content, line_counter, column_counter


def create_content_by_case(section_lines: list[str], case: int) -> dict:
    """
    function which extracts data from a list of text by it previously determined structure
    :param section_lines:
    :param case: Integer for determining the method of dataextraction
    :return: dictionary of the extracted case structure
    """
    # case_names = ['EMPTY', 'table', 'box', 'text']
    content = OrderedDict()
    if case == 0:  # empty line
        content = []
        for line in section_lines:
            content.append(line)
        pass
    elif case == 1:  # table
        content, position, column = table_lines_to_content(section_lines)
        if position:
            list_array = []
            for lines_1 in range(len(content)):
                if lines_1 < position[0] - 1:
                    next_line = [x for x in content[lines_1]]
                    list_array.append(next_line)
                else:
                    next_line = [x for x in content[lines_1][:column[0] + 1]]
                    list_insert = [x for x in content[lines_1][column[0] + 1:]]
                    next_line.append(list_insert)
                    list_array.append(next_line)
            list(map(list, zip(*list_array)))
            dict_table = OrderedDict()
            for entries in range(len(list_array)):
                dict_table.update({list_array[entries][0]: [list_array[entries][1:]]})
        else:
            array_1 = np.array([])
            for lines_2 in content:
                if lines_2 == content[0]:
                    next_line = [np.array(x) for x in lines_2]
                    array_1 = np.array(next_line)
                else:
                    next_line = [np.array(x) for x in lines_2]
                    array_1 = np.vstack([array_1, next_line])
            if array_1.ndim >= 2:
                keys_table = array_1[:, 0]
                items_table = array_1[:, 1:].tolist()
                dict_table = OrderedDict(zip(keys_table, items_table))
                content = dict_table
            else:
                print('Error: a table has smaller Dimension than x:2')

    elif case == 2:  # box
        content = ''
        for line in section_lines:
            if '+' in line:
                pass
            else:
                string = line.strip().strip('|').strip()
                content += string + ' \n'
    else:  # case 3 = text
        for line in section_lines:  # todo fall für gleichen Namen einprogramieren
            if bool(line.count(':') >= 2) or bool(line.count('=') >= 2) or bool(
                    (line.count(':') + line.count('=')) >= 2):
                content.update({line.strip(): []})
            elif bool('\\' in line):
                content.update({line.strip(): []})
            elif bool(':' in line) or bool('=' in line):
                content.update(line_to_diction(line))
            else:
                content.update({line.strip(): []})
    return content


def check_line(line: str, last_line_case: int) -> int:
    """
    function determining which regular segment is active in current line and whether a switch occurred
    :param line: current line
    :param last_line_case: last line
    :return: current line case
    """
    # info line_case = ['EMPTY', 'table', 'box', 'text']
    if bool(line.count('|') >= 3) or bool(line.count('+') >= 3):
        case = 1
    elif bool(last_line_case == 1) & bool(line.count('+') == 2):
        case = 1
    elif bool(line.count('|') == 2) or bool(line.count('+') == 2):
        case = 2
    elif bool(line != '') or bool(line != ' '):
        case = 3
    else:
        case = 0
    return case


def check_line_case(subsection_text: list[str]) -> dict:
    """
    Function for start checking line by line which regular segment is used
    :param subsection_text: list of text of respective section
    :return: dictionary ordered by the occurrence of respective regular element
    """
    case = 0
    case_names = ['EMPTY', 'table', 'box', 'text']
    case_lines = []
    dict_number = 0
    dict_subsection = OrderedDict()
    while subsection_text:
        last_line_case = case
        case = check_line(subsection_text[0], last_line_case)
        if last_line_case != case:
            if last_line_case == 0:
                case_lines = [subsection_text[0]]
            else:
                dict_subsection.update(collections.OrderedDict(
                    {dict_number: collections.OrderedDict({case_names[case]:
                                                           create_content_by_case(case_lines, last_line_case)})}))
                # todo hier kann geprüft werden warum leere Zeilen eingefügt werden
                case_lines = [subsection_text[0]]
                dict_number += 1
        else:
            case_lines.append(subsection_text[0])
        subsection_text.pop(0)
    last_line_case = case
    dict_number += 1
    dict_subsection.update(collections.OrderedDict({dict_number: collections.OrderedDict({case_names[
        case]: create_content_by_case(
        case_lines, last_line_case)})}))  # todo hier kann geprüft werden warum leere Zeilen eingefügt werden
    return dict_subsection


def text_to_subsection_dict(subsection_text: list, section_key: str, subsection_key: str) -> OrderedDict:
    """
    Function for checking whether a segment is a regular or a special syntaxed segment, currently only the
    "Convergence History" Segment and the "CFX Command Language for Run" are known to be special segments
    :param subsection_text: list of string of text for each segment
    :param section_key: string of the header
    :param subsection_key: string of the sub header
    :return: OrderedDict of the given section with the data extracted with its specific syntax
    """
    subsection_txt = subsection_text
    if bool(section_key == 'CFX Command Language for Run') & bool(subsection_key == 'Initialization'):
        subsection_dict = comm_lang_to_dict(subsection_text, -1)
    elif bool(section_key == 'Solver') & bool(subsection_key == 'Convergence History'):
        subsection_dict = convergence_to_dict(subsection_text)
    else:
        subsection_dict = check_line_case(subsection_txt)
    return subsection_dict


def dividing_into_subsections_and_convert(file_text_cleaned: list[str],
                                          sections: list[list[str]],
                                          dividing_lines_header: list[str]) -> OrderedDict:
    """
    Capital function for segmenting into subsections and extraction the data while doing so
    :param file_text_cleaned: cleaned list of text
    :param sections: list of sections with are in return lists of
    strings
    :param dividing_lines_header: list of headers for segments
    :return: OrderedDict in with information is
    devided into sections, subsections and specific data structures such as tables
    """
    baseline = 0
    dict_sections = OrderedDict()
    n = 0
    line_test = 0
    list_all_subsection_keys = []
    for section in sections:
        list_subsections_keys = []
        list_subsections_line = []
        dict_subsections = OrderedDict()
        dict_subsections.update({'Initialization': line_test})
        line_test += 5
        for lines in range(len(section) - 5):
            line_test += 1
            baseline += 1
            test_2 = Segmenting(section[lines:lines + 5])
            if test_2.check_and_return_subsection()[0]:
                if test_2.check_and_return_subsection()[1] in list_all_subsection_keys:
                    string = str(test_2.check_and_return_subsection()[1]) + '_1'
                    m = 1
                    while string in list_all_subsection_keys:
                        m += 1
                        string = ''.join(list(string)[-1] + str(m))
                    list_subsections_keys.append(string)
                else:
                    list_subsections_keys.append(test_2.check_and_return_subsection()[1])
                list_all_subsection_keys.append(test_2.check_and_return_subsection()[1])
                list_subsections_line.append(
                    line_test - 4)  # todo ich habe leider nicht verstanden, warum hier eine -4 hin muss'
                dict_subsections.update({list_subsections_keys[-1]: list_subsections_line[-1]})
        dict_subsections.update({'end': line_test})
        dict_sections.update({dividing_lines_header[n]: dict_subsections})
        n += 1
    dict_test_2 = OrderedDict()
    for sec in dict_sections.keys():
        dict_test = OrderedDict()
        for subsec_1, subsec_2 in zip(list(dict_sections[sec].keys())[:-1], list(dict_sections[sec].keys())[1:]):
            line_test_1 = dict_sections[sec][subsec_1]
            line_test_2 = dict_sections[sec][subsec_2]
            if re.search(".*\\d.*", subsec_1):
                subsec_1 = subsec_1.split('_')[0]
            dict_section_text = file_text_cleaned[line_test_1:line_test_2]
            dict_section_text = clean_start_of_subsection(dict_section_text)
            dict_section_text = clean_end_of_subsection(dict_section_text)
            subsection_dict = text_to_subsection_dict(dict_section_text, sec, subsec_1)
            dict_test.update({subsec_1: subsection_dict})
        dict_test_2.update({sec: dict_test})
    return dict_test_2


def clean_section_text(file_text: list) -> list:
    """
    Cleans list of text from multi row texts
    :param file_text: list
    :return: list
    """
    over_hanging_lines = []
    for iterator, line in enumerate(file_text):
        if line.strip():
            if '\\' in line.strip()[-1]:
                over_hanging_lines.append(iterator)
    for lines in reversed(over_hanging_lines):
        file_text[lines] = ''.join((file_text[lines].rstrip().rstrip('\\'), file_text[lines + 1].strip()))
        file_text.pop(lines + 1)
    cleaned_section = file_text
    return cleaned_section


def file_to_section(path, filename):
    """
    Converts ".out-file" via its path & name into a list of text
    :param path: str
    :param filename: str
    :return: list
    """
    file_text = []
    outfile = open(os.path.join(path, filename))
    with outfile as f_all:
        for line_all in f_all:
            t_line_all = str(line_all).rstrip('\n')
            file_text.append(t_line_all)
    return file_text


def file_to_dict_of_sections(path: str, filename: str) -> dict:
    """
    Function for converting an out-files via its path into a JSON-dictionary with all text structures converted into
    nested dictionaries. It starts a segmentation and conversion process for different segments.
    :param path: str
    :param filename: str
    :return: OrderedDict
    """
    file_text = file_to_section(path, filename)
    file_text_cleaned = clean_section_text(file_text)
    dividing_lines, dividing_lines_header = determining_sections(file_text_cleaned)
    sections = dividing_into_sections(file_text_cleaned, dividing_lines)
    return_dict = dividing_into_subsections_and_convert(file_text_cleaned, sections, dividing_lines_header)
    return return_dict


def folder_to_file_list(read_path: str):
    """
    returns the root filename and internal_name/saved_name of all '.out' files in the directory given by 'path' as a
    list of normalised pathes
    :param read_path: str
    :return: list of lists [path, filename, internal_name]
    """
    file_list = []
    for path, dirs, files in os.walk(read_path):
        for filename in files:
            if filename.endswith(".out"):
                internal_name = os.path.normpath(path.split(read_path)[1] + filename.split('.out')[0])
                internal_name = internal_name[1:].replace('\\', '_')
                file_list.append([path, filename, internal_name])
    return file_list


def dump_files_to_json(read_path, write_path='', dump=True):
    """
    Ansys out-file -> Json-dict
    Central function for extracting data from Ansys-out-files and dumping them into JSON-files. Define read_path
    as the source-directory of Ansys out-files and write_path as the saving_directory. Convert structures \
    from text-file (out-file) into a nested dictionary keyword-value-relation.
    :param read_path: str
    :param write_path: str (defaults to python_project_path)
    :param dump: bool (True = dumping, False = PythonConsole only)
    :return: Dictionary of all out-Files
    """
    file_list = folder_to_file_list(read_path)
    dict_collection = OrderedDict()
    for path, filename, internal_name in file_list:
        json_dict = file_to_dict_of_sections(path, filename)
        filename_with_dict = {internal_name: json_dict}
        dict_collection.update(filename_with_dict)
    if dump:
        for i_1, i_2 in dict_collection.items():
            with open(''.join(write_path) + ''.join(i_1) + ".json", "w") as out_file:
                json.dump(i_2, out_file)
    return dict_collection


# H:/NicksDaten/05 Simulationen
# C:/Users/hendr/Desktop/Für Hendrik
# Path_2 = 'C:\Users\smhhborg\Documents\GitHub\Hendrik_Borgelt_Masterthesis'


if __name__ == '__main__':
    start = time.perf_counter()

    try:
        if os.path.exists('D:/Nicks Daten/Fuer Hendrik'):
            Path = 'D:/Nicks Daten/Fuer Hendrik'
            print('ReadPath: %s' % Path)
        elif os.path.exists('H:/NicksDaten/05 Simulationen'):
            Path = 'H:/NicksDaten/05 Simulationen'
            print('ReadPath: %s' % Path)
        elif os.path.exists('C:/Users/hendr/Desktop/Für Hendrik'):
            Path = 'C:/Users/hendr/Desktop/Für Hendrik'
            print('ReadPath: %s' % Path)
        elif os.path.exists('C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis'):
            Path = 'C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis'
            print('ReadPath: %s' % Path)
        else:
            raise FileNotFoundError
        if os.path.exists('H:/NicksDaten'):
            Write_Path = 'H:/NicksDaten/Json_Dict_unmodified2/'
            print('WritePath: %s' % Write_Path)
        elif os.path.exists('D:'):
            Write_Path = 'D:/Json_Dict_unmodified2/'
            print('WritePath: %s' % Write_Path)
        else:
            raise FileNotFoundError
        try:
            os.makedirs(Write_Path)
        except FileExistsError:
            pass
        dict_1 = dump_files_to_json(Path, Write_Path)
        print('Finished')
        print(time.perf_counter() - start)

    except FileNotFoundError:
        print('Read-Folder not found')
