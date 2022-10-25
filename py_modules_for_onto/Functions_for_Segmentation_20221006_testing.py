import copy
import json
from py_modules_for_onto.Central_functions_for_Ontology_mod_20220810 import *
import os
import collections
from collections import defaultdict


def check_if_key_str_is_name_inst(key_str_int, list_of_named_inst_int):
    if any([(True if i_2 == key_str_int else False) for i_2 in list_of_named_inst_int]):
        return True
    else:
        return False


def swap_dict_individual_2(tuple_keys, dict_int, ind_name):
    if tuple_keys:
        if len(tuple_keys) >= 2:
            dict_int[tuple_keys[0]] = swap_dict_individual_2(tuple_keys[1:], dict_int[tuple_keys[0]], ind_name)
            return dict_int
        else:
            if 'Individuals_json_Links' not in dict_int[tuple_keys[0]].keys():
                dict_int[tuple_keys[0]]['Individuals_json_Links'] = ind_name
            else:
                if isinstance(dict_int[tuple_keys[0]]['Individuals_json_Links'], str):
                    dict_int[tuple_keys[0]]['Individuals_json_Links'] = [
                        dict_int[tuple_keys[0]]['Individuals_json_Links'], ind_name]
                else:
                    dict_int[tuple_keys[0]]['Individuals_json_Links'].append(ind_name)
            try:
                del dict_int[tuple_keys[0]][ind_name.split(',')[-1].rstrip('.json').split('+')[-1].split('_')[0]]
            except:
                test = True
            # dict_int[tuple_keys[0]]] = ind_name # oldest and definetly wrong structure since it only generates one link
            test = True
            return dict_int
    else:
        print('Error: tuple is Empty')


def change_name_of_sub_sub_inst_2(all_sims, sub_sub_dict_folder_path, tuple_list_of_named_inst_int):
    str_list_of_named_inst_int = change_list_of_tuples_to_list_of_str(tuple_list_of_named_inst_int)
    modified_all_sims = copy.deepcopy(all_sims)
    for root_3, dirs_3, files_3 in os.walk(sub_sub_dict_folder_path):
        for name_3 in files_3:
            with open(root_3 + str('/') + name_3, 'r') as in_file:
                loaded_json = json.load(in_file)
                for i_1_int in modified_all_sims:
                    if i_1_int in loaded_json['Sims']:
                        tuple_int = loaded_json['Tuple']
                        if check_if_key_str_is_name_inst(name_3.split(',')[0], str_list_of_named_inst_int):
                            swap_dict_individual_2(tuple_int, modified_all_sims[i_1_int], name_3)
                        else:
                            swap_dict_individual_2(tuple_int[:-1], modified_all_sims[i_1_int], name_3)
    return modified_all_sims


def add_tuples_and_str_to_tuple_or_str(tuple_1_int, tuple_2_int):
    return_tuple = tuple_1_int
    if isinstance(return_tuple, str):
        if isinstance(tuple_2_int, str):
            return_tuple = (return_tuple, tuple_2_int)
        else:
            return_tuple = (return_tuple,) + tuple_2_int
    else:
        if isinstance(tuple_2_int, str):
            return_tuple = return_tuple + (tuple_2_int,)
        else:
            return_tuple = return_tuple + tuple_2_int
    return return_tuple


def search_for_inst_in_inst_dict_2(dict_to_be_appended_int, ind_name, dict_of_individual_a, sim_name):
    test = search_for_instance_in_dict(dict_to_be_appended_int, ind_name)
    dict_to_be_appended_int = clean_dict_from_indiv_links(dict_to_be_appended_int)
    if not dict_of_individual_a:
        # dict_of_individual_a.append(
        #     [ind_name + '_' + str(len(dict_of_individual_a)), [sim_name], dict_to_be_appended_int, {sim_name: test}])
        dict_of_individual_a.append(
            [ind_name + '_' + str(len(dict_of_individual_a)), {sim_name: test}, dict_to_be_appended_int])
    elif dict_to_be_appended_int not in [i_int[2] for i_int in dict_of_individual_a]:
        # dict_of_individual_a.append(
        #     [ind_name + '_' + str(len(dict_of_individual_a)), [sim_name], dict_to_be_appended_int, {sim_name: test}])
        dict_of_individual_a.append(
            [ind_name + '_' + str(len(dict_of_individual_a)), {sim_name: test}, dict_to_be_appended_int, ])
    elif dict_to_be_appended_int in [i_int[2] for i_int in dict_of_individual_a]:
        for i_int in dict_of_individual_a:
            if dict_to_be_appended_int == i_int[2]:
                # if sim_name not in i_int[1]:
                #     i_int[1].append(sim_name)
                if sim_name not in i_int[1].keys():
                    i_int[1].update({sim_name: test})
    return dict_of_individual_a


def add_multiple_tuples_to_tuple(list_of_tuples):
    new_tuple = tuple()
    for i in list_of_tuples:
        new_tuple = add_tuples_and_str_to_tuple_or_str(new_tuple, i)
    return new_tuple


def return_subdict(dict_int, tuple_int):
    return_dict = dict_int
    if isinstance(tuple_int, str):
        if tuple_int not in return_dict:
            return None
        else:
            return_dict = return_dict[tuple_int]
    elif isinstance(tuple_int, tuple):
        for i_int in tuple_int:
            try:
                if i_int not in return_dict:
                    return None
                else:
                    return_dict = return_dict[i_int]
            except:
                test_1 = True
                pass
    return return_dict


def return_sub_dict_and_path_2(dictionary, keyword):
    if type(dictionary) == dict or type(dictionary) == collections.OrderedDict:
        for key_1, value_1 in dictionary.items():
            if keyword == key_1:
                return value_1, key_1
            else:
                if return_sub_dict_and_path_2(value_1, keyword) is not None:
                    a_1, b_1 = return_sub_dict_and_path_2(value_1, keyword)
                    if type(b_1) == str:
                        return a_1, (key_1,) + (b_1,)
                    else:
                        return a_1, (key_1,) + tuple(list(b_1))


def search_for_name_in_outdict_and_save(all_sims_int, outdict_int, path_int):
    for i in outdict_int:
        name_inst = '-'.join(outdict_int[i]['Inst_Tuples']) + ',' + str(i)
        tuple_path = outdict_int[i]['Path_Tuples']
        list_of_individuals = []
        for i_2 in all_sims_int:
            if return_subdict(all_sims_int[i_2], tuple_path):
                sub_dict_int = return_subdict(all_sims_int[i_2], tuple_path)
                list_of_individuals = search_for_inst_in_inst_dict_2(
                    sub_dict_int, name_inst,
                    list_of_individuals, i_2)
        for i_1 in list_of_individuals:
            try:
                os.makedirs(path_int)
            except:
                pass
            with open(path_int + i_1[0] + ".json", "w") as out_file:
                json.dump({'dict': i_1[2], 'Sims': i_1[1], 'Tuple': outdict_int[i]['Path_Tuples']}, out_file)
            # print(i_1[0])
    # for i_3 in test_list:
    #     print(i_3)
    # return test_list


def check_if_tuple_in_dict_return_path(dict_int, tuple_tbc_int, dict_of_prev_inst_int_1, bool_for_named_inst):
    if not dict_of_prev_inst_int_1:
        dict_of_prev_inst_int = {'': {'Key_Tuples': tuple(),
                                      'Inst_Tuples': tuple(),
                                      'Path_Tuples': ('CFX Command Language for Run',)
                                      }}
    else:
        dict_of_prev_inst_int = dict_of_prev_inst_int_1
    dict_of_next_inst = dict()
    for i in dict_of_prev_inst_int:
        path_tuples = dict_of_prev_inst_int[i]['Path_Tuples']
        sub_dict_int = return_subdict(dict_int, path_tuples)
        if bool_for_named_inst:
            if return_sub_dict_and_path_2(sub_dict_int, tuple_tbc_int):
                dict_int_2, path_tuple = return_sub_dict_and_path_2(sub_dict_int, tuple_tbc_int)
                for i_2 in dict_int_2:
                    key_name = (i + '+' + i_2).lstrip('+')
                    dict_of_next_inst[key_name] = copy.deepcopy(dict_of_prev_inst_int[i])
                    dict_of_next_inst[key_name]['Key_Tuples'] = dict_of_next_inst[key_name]['Key_Tuples'] + (i_2,)
                    dict_of_next_inst[key_name]['Path_Tuples'] = add_multiple_tuples_to_tuple(
                        [dict_of_next_inst[key_name]['Path_Tuples'], path_tuple, (i_2,)])
                    dict_of_next_inst[key_name]['Inst_Tuples'] = add_tuples_and_str_to_tuple_or_str(
                        dict_of_next_inst[key_name]['Inst_Tuples'], tuple_tbc_int)

        else:
            if return_sub_dict_and_path_2(sub_dict_int, tuple_tbc_int):
                key_name = (i + '+' + tuple_tbc_int).lstrip('+')
                to_be_discarded, path_tuple = return_sub_dict_and_path_2(sub_dict_int, tuple_tbc_int)
                dict_of_next_inst[key_name] = dict_of_prev_inst_int[i]
                dict_of_next_inst[key_name]['Key_Tuples'] = \
                    dict_of_next_inst[key_name]['Key_Tuples'] + (tuple_tbc_int,)
                dict_of_next_inst[key_name]['Path_Tuples'] = \
                    add_multiple_tuples_to_tuple([dict_of_next_inst[key_name]['Path_Tuples'], path_tuple])
                dict_of_next_inst[key_name]['Inst_Tuples'] = add_tuples_and_str_to_tuple_or_str(
                    dict_of_next_inst[key_name]['Inst_Tuples'], tuple_tbc_int)
    return dict_of_next_inst


def new_dicts_to_individualdicts(dict_int, list_of_keys_tbc, tuple_list_of_named_inst_int,
                                 tuple_list_of_non_named_inst_int, all_dicts_int, path_int):
    str_list_of_named_inst_int = change_list_of_tuples_to_list_of_str(tuple_list_of_named_inst_int)
    str_list_of_non_named_inst_int = change_list_of_tuples_to_list_of_str(tuple_list_of_non_named_inst_int)
    out_dict = dict()
    for i in list_of_keys_tbc:
        if i == 'EXPRESSIONS':
            test = True
        else:
            test = False
        name_tbc = ''
        dict_of_inst_int = dict()
        if isinstance(i, str):
            dict_of_inst_int = check_if_tuple_in_dict_return_path(dict_int, i, dict_of_inst_int,
                                                                  check_if_key_str_is_name_inst(i,
                                                                                                str_list_of_named_inst_int))
            # print(name_tbc, i, check_if_key_str_is_name_inst(name_tbc, str_list_of_named_inst_int))
            pass
        else:
            for i_1, i_2 in enumerate(i):
                name_tbc = ' '.join([name_tbc, i_2]).lstrip(' ')
                dict_of_inst_int = check_if_tuple_in_dict_return_path(dict_int, i_2, dict_of_inst_int,
                                                                      check_if_key_str_is_name_inst(name_tbc,
                                                                                                    str_list_of_named_inst_int))
                # print(name_tbc, i[:i_1 + 1], check_if_key_str_is_name_inst(name_tbc, str_list_of_named_inst_int))

        search_for_name_in_outdict_and_save(all_dicts_int, dict_of_inst_int, path_int)



def find_rename_and_replace_inst_dict(dict_int, list_instances_tbc, tuple_list_of_named_inst_int,
                                      tuple_list_of_non_named_inst_int, path_int):
    merged_dict_int = create_merged_dict(copy.deepcopy(dict_int))
    new_dicts_to_individualdicts(merged_dict_int, list_instances_tbc, tuple_list_of_named_inst_int,
                                 tuple_list_of_non_named_inst_int, dict_int, path_int)
    out_dict_int = change_name_of_sub_sub_inst_2(dict_int, path_int, tuple_list_of_non_named_inst_int)
    return out_dict_int


def archive_and_change_all_instances(dict_of_ordered_instances, dict_int, tuple_list_of_named_inst_int,
                                     tuple_list_of_non_named_inst_int):
    dict_to_be_changed = copy.deepcopy(dict_int)
    for counter, i in enumerate(dict_of_ordered_instances):
        print(f"{counter}/{len(dict_of_ordered_instances)}", end='\r')
        list_instances_tbc = dict_of_ordered_instances[i]['list_instances_tbc']
        path_int = dict_of_ordered_instances[i]['path']
        dict_to_be_changed = find_rename_and_replace_inst_dict(dict_to_be_changed, list_instances_tbc,
                                                               tuple_list_of_named_inst_int,
                                                               tuple_list_of_non_named_inst_int, path_int)


# def search_for_instance_in_dict(dict_int, last_ind_name):
#     list_of_instances = []
#     if isinstance(dict_int, dict):
#         for k, v in dict_int.items():
#             if isinstance(v, dict):
#                 intermediate = search_for_instance_in_dict(v)
#                 if isinstance(intermediate, list):
#                     for i_1 in intermediate:
#                         list_of_instances.append(i_1)
#                 else:
#                     list_of_instances.append(intermediate)
#             if isinstance(v, list):
#                 for i_2 in v:
#                     if len(i_2.split('.json')) == 2:
#                         list_of_instances.append(i_2.split('.json')[0])
#             if isinstance(v, str):
#                 if len(v.split('.json')) == 2:
#                     list_of_instances.append(v.split('.json')[0])
#     if isinstance(dict_int, list):
#         for i_2 in dict_int:
#             if len(i_2.split('.json')) == 2:
#                 list_of_instances.append(i_2.split('.json')[0])
#     if isinstance(dict_int, str):
#         if len(dict_int.split('.json')) == 2:
#             list_of_instances.append(dict_int.split('.json')[0])
#     return list_of_instances


def search_for_instance_in_dict(dict_int,last_indiv_name = 'direct_ancestor'):
    sim_and_json_inst_dict = defaultdict()
    if isinstance(dict_int, dict):
        for k, v in dict_int.items():
            if k == 'Individuals_json_Links':
                sim_and_json_inst_dict[last_indiv_name] = v
            elif 'File' in k:
                sim_and_json_inst_dict[k] = v
            else:
                sim_and_json_inst_dict.update(search_for_instance_in_dict(v, k))
    return sim_and_json_inst_dict


def clean_dict_from_indiv_links(dict_int):
    if isinstance(dict_int, dict):
        for k, v in list(dict_int.items()):
            if k == 'Individuals_json_Links':
                dict_int.pop(k)
            elif 'File' in k:
                dict_int[k] = {}
            else:
                dict_int[k] = clean_dict_from_indiv_links(v)
    return dict_int

