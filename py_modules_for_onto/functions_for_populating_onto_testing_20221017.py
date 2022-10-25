import os
import time
import types
import json
import collections
import copy
from py_modules_for_onto.Testing_Inventory_module_20221017 import ModifyOnto
from py_modules_for_onto.Central_functions_for_Ontology_mod_20220810 import *

global inventory_int


def change_filepath_name_in_dict(dict_int):
    for k_int, v_int in list(dict_int.items()):
        if ' = ' in k_int:
            try:
                dict_int[k_int.split(' = ')[0].rstrip(' ')] = k_int.split(' = ')[1].lstrip(' ') + list(v_int.keys())[0]
            except:
                test =1
            del dict_int[k_int]
        elif isinstance(v_int, (dict, OrderedDict)):
            change_filepath_name_in_dict(v_int)


def change_names_in_dict_by_adding_prefix_2(dictionary, list_of_names_to_be_preffixed):
    dict_int = dictionary
    for k_1, v_1 in list(dict_int.items()):
        if type(v_1) is dict:
            dict_int[' '.join(list_of_names_to_be_preffixed) + ' ' + k_1] = \
                change_names_in_dict_by_adding_prefix_2(v_1, list_of_names_to_be_preffixed)
            dict_int.pop(k_1)
        else:
            if '.json Option' in k_1:
                dict_int[' '.join(list_of_names_to_be_preffixed) + ' ' + 'Individual Option'] = dict_int.pop(k_1)
            else:
                dict_int[' '.join(list_of_names_to_be_preffixed) + ' ' + ''.join(k_1)] = dict_int.pop(k_1)
    return dict_int


time_measurement = []


def change_names_in_dict_by_adding_prefix_3(dictionary, list_of_names_to_be_preffixed, list_of_inst_int):
    dict_int = dictionary
    for k_1, v_1 in list(dict_int.items()):
        if type(v_1) is dict:
            if any([(True if i_2 == k_1 else False) for i_2 in list_of_inst_int]):
                list_of_names_to_be_preffixed = (k_1, list_of_names_to_be_preffixed[-1],)
                dict_int[k_1 + ' ' + list_of_names_to_be_preffixed[-1]] = \
                    change_names_in_dict_by_adding_prefix_3(v_1, list_of_names_to_be_preffixed, list_of_inst_int)
                dict_int.pop(k_1)
                pass
            else:
                dict_int[' '.join(list_of_names_to_be_preffixed) + ' ' + k_1] = \
                    change_names_in_dict_by_adding_prefix_3(v_1, list_of_names_to_be_preffixed, list_of_inst_int)
                dict_int.pop(k_1)
        else:
            if '.json Option' in k_1:
                dict_int[' '.join(list_of_names_to_be_preffixed) + ' ' + 'Individual Option'] = dict_int.pop(k_1)
            else:
                dict_int[' '.join(list_of_names_to_be_preffixed) + ' ' + ''.join(k_1)] = dict_int.pop(k_1)
    return dict_int


def search_instance_folder_and_insert_into_emmo_1(path_int, dict_of_excel_translator_int, tuple_list_of_named_inst_int,
                                                  tuple_list_of_non_named_inst_int, inventory_onto_int,
                                                  int_debug=0):
    global inventory_int
    inventory_int = inventory_onto_int
    temp_list = copy.deepcopy(tuple_list_of_named_inst_int)
    list_of_named_inst_int = change_list_of_tuples_to_list_of_str(temp_list)
    temp_list_2 = copy.deepcopy(tuple_list_of_non_named_inst_int)
    list_of_non_named_inst_int = change_list_of_tuples_to_list_of_str(temp_list_2)
    list_of_inst_int = list_of_named_inst_int + list_of_non_named_inst_int
    for root_3, dirs_3, files_3 in os.walk(path_int):
        counter_2 = len(files_3)
        for counter, name_3 in enumerate(files_3):
            start_time = time.perf_counter()
            print(f"{counter}/{counter_2}", end='\r')
            with open(root_3 + str('/') + name_3, 'r') as in_file:
                dict_for_emmo_instances = json.load(in_file)
            start_dict_to_emmo_individuals_3(dict_for_emmo_instances, name_3, dict_of_excel_translator_int,
                                             list_of_inst_int)
            time_measurement.append(time.perf_counter() - start_time)
            if bool((time.perf_counter() - start_time) >= 5) & bool(int_debug >= 2):
                t_0 = time.perf_counter() - start_time
                print(f'very slow instance \'{name_3}\' found with required time of \'{t_0}\'')
            if bool(5 > (time.perf_counter() - start_time) >= 1) & bool(int_debug >= 2):
                t_1 = time.perf_counter() - start_time
                print(f'slow instance \'{name_3}\' found with required time of \'{t_1}\'')
    return time_measurement


def start_dict_to_emmo_individuals_3(dict_int, name_int, dict_of_excel_trans_int, list_of_named_inst_int):
    new_name_int = [name_int.rstrip('.json').split(',')[0].replace('-', ' '),
                    name_int.rstrip('.json').split(',')[1].title().replace(' ', '').replace('-', ' ').replace('+', '_')]
    list_of_sims = [item_1.replace('-', '_').replace(' ', '_').replace(',', '__').replace('.', '__')for item_1 in dict_int['Sims']]

    if isinstance(dict_int['dict'], (dict, OrderedDict)):
        change_names_in_dict_by_adding_prefix_3(dict_int['dict'], (new_name_int[0], '-' + new_name_int[1] + '-'),
                                                list_of_named_inst_int)
        if new_name_int[1] not in [item for item in inventory_int.dataframe_of_individuals.prefLabel]:
            indiv_class = dict_of_excel_trans_int['Onto_name'][list(dict_of_excel_trans_int['Dict_name'].keys())[
                list(dict_of_excel_trans_int['Dict_name'].values()).index(new_name_int[0] + ' Individual')]]
            inventory_int.create_indiv_with_inventory(new_name_int[1], indiv_class)
        for i_1 in dict_int['Sims']:
            sim_name = i_1.replace('-', '_').replace(' ', '_').replace(',', '__').replace('.', '__')
            if sim_name not in [item for item in inventory_int.dataframe_of_individuals.prefLabel]:
                inventory_int.create_indiv_with_inventory(sim_name, 'MathematicalSimulations')
            inventory_int.connect_indiv_obj_indiv_with_inventory(new_name_int[1], 'hasSimulation', sim_name)
            inventory_int.connect_indiv_obj_indiv_with_inventory(sim_name, 'hasIndividual', new_name_int[1])
        list_of_sims = [item.replace('-', '_').replace(' ', '_').replace(',', '__').replace('.', '__')
                        for item in dict_int['Sims']]
        dict_to_emmo_individual_1(dict_int['dict'], dict_of_excel_trans_int, list_of_sims, new_name_int[1],
                                  new_name_int[1])
    else:
        if new_name_int[1] not in [item for item in inventory_int.dataframe_of_individuals.prefLabel]:
            # if new_name_int[0] + ' Individual' in {'FLOW DOMAIN FLUID MODELS Individual',
            #                                        'FLOW DOMAIN SUBDOMAIN Individual'}:
            #     indiv_class = dict_of_excel_trans_int['Onto_name'][list(dict_of_excel_trans_int['Dict_name'].keys())[
            #         list(dict_of_excel_trans_int['Dict_name'].values()).index(new_name_int[0])]]
            # else:
            #     indiv_class = dict_of_excel_trans_int['Onto_name'][list(dict_of_excel_trans_int['Dict_name'].keys())[
            #         list(dict_of_excel_trans_int['Dict_name'].values()).index(new_name_int[0] + ' Individual')]]
            indiv_class = dict_of_excel_trans_int['Onto_name'][list(dict_of_excel_trans_int['Dict_name'].keys())[
                list(dict_of_excel_trans_int['Dict_name'].values()).index(new_name_int[0] + ' Individual')]]
            inventory_int.create_indiv_with_inventory(new_name_int[1], indiv_class)
        for i_1 in dict_int['Sims']:
            sim_name = i_1.replace('-', '_').replace(' ', '_').replace(',', '__').replace('.', '__')
            if sim_name not in [item for item in inventory_int.dataframe_of_individuals.prefLabel]:
                inventory_int.create_indiv_with_inventory(sim_name, 'MathematicalSimulations')
            inventory_int.connect_indiv_obj_indiv_with_inventory(new_name_int[1], 'hasSimulation', sim_name)
            inventory_int.connect_indiv_obj_indiv_with_inventory(sim_name, 'hasIndividual', new_name_int[1])
        # list_of_sims = [item.replace('-', '_').replace(' ', '_').replace(',', '__').replace('.', '__')
        #                 for item in dict_int['Sims']]
        data_prop_name_check = 'has' + new_name_int[0].title().replace(' ', '')
        if len(str(dict_int['dict']).split('[')) == 2:
            try:
                indiv_value = float(dict_int['dict'].split('[')[0])
            except ValueError:
                value_int = dict_int['dict'].split('[')[0]
                indiv_value = f'not a float:{value_int}'
            indiv_unit = dict_int['dict'].split('[')[1].rstrip(']')
            if inventory_int.return_onto_object(data_prop_name_check + 'Value', 'data_property') is None:
                inventory_int.create_data_prop_with_inventory(data_prop_name_check + 'Value', owlready2.DataProperty)
            if inventory_int.return_onto_object(data_prop_name_check + 'Unit', 'data_property') is None:
                inventory_int.create_data_prop_with_inventory(data_prop_name_check + 'Unit', owlready2.DataProperty)
            inventory_int.place_data_with_inventory(new_name_int[1].replace('.', '_-'),
                                                    data_prop_name_check + 'Value',
                                                    indiv_value)
            inventory_int.place_data_with_inventory(new_name_int[1].replace('.', '_-'),
                                                    data_prop_name_check + 'Unit',
                                                    indiv_unit)
        else:
            if inventory_int.return_onto_object(data_prop_name_check + 'Value', 'data_property') is None:
                inventory_int.create_data_prop_with_inventory(data_prop_name_check + 'Value', owlready2.DataProperty)
            inventory_int.place_data_with_inventory(new_name_int[1],
                                                    data_prop_name_check + 'Value',
                                                    dict_int['dict'])
        pass

    # if ((name_int == 'FLOW-DOMAIN INTERFACE,Flow Analysis 1+Default Solid Solid Interface_0.json') or
    #         (name_int == 'FUNCTION-DATA FIELD,MassFrac+Biodiesel Mass Fraction_0.json') or
    #         (name_int == 'FLOW-DOMAIN,Flow Analysis 1+Default Domain_0.json')):
    for sim_int, sim_instance_dicts in dict_int['Sims'].items():
        sim_name = sim_int.replace('-', '_').replace(' ', '_').replace(',', '__').replace('.', '__')
        if sim_instance_dicts:
            if isinstance(sim_instance_dicts, dict):
                for k_1, v_1 in sim_instance_dicts.items():
                    test_3 = v_1
                    if isinstance(v_1, list):
                        for v_2 in v_1:
                            if ',' not in k_1:
                                test_2 = 'has' + k_1.title().replace(' ', '')
                                test_3 = 'is' + k_1.title().replace(' ', '') + 'Of'
                            else:
                                test_2 = 'has' + v_2.split(',')[0].split('-')[-1].title().replace(' ', '')
                                test_3 = 'is' + v_2.split(',')[0].split('-')[-1].title().replace(' ', '') + 'Of'
                            if '.json' not in v_2:
                                if inventory_int.return_onto_object(test_2 + 'Value', 'data_property') is None:
                                    inventory_int.create_data_prop_with_inventory(test_2 + 'Value', owlready2.DataProperty)
                                inventory_int.place_data_with_inventory(sim_name, test_2 + 'Value', v_2)
                            else:
                                test_4 = v_2.rstrip('.json').split(',')[1].title().replace(' ', '').replace('-', ' ').replace('+', '_')
                                test_5 = f'{sim_name} {test_2} {test_4}'
                                test_5_1 = test_5
                                if inventory_int.return_onto_object(test_2, 'object_property') is None:
                                    inventory_int.create_object_prop_with_inventory(test_2, owlready2.ObjectProperty)
                                if inventory_int.return_onto_object(test_3, 'object_property') is None:
                                    inventory_int.create_object_prop_with_inventory(test_3, owlready2.ObjectProperty)
                                inventory_int.connect_indiv_obj_indiv_with_inventory(sim_name, test_2, test_4)
                                inventory_int.connect_indiv_obj_indiv_with_inventory(test_4, test_3, sim_name)
                                # inventory_int.connect_indiv_obj_indiv_with_inventory(new_name_int[1], test_2, test_4)
                                # inventory_int.connect_indiv_obj_indiv_with_inventory(test_4, test_3, new_name_int[1])
                    elif isinstance(v_1, str):
                        if not ',' in k_1:
                            test_2 = 'has' + k_1.title().replace(' ', '')
                            test_3 = 'is' + k_1.title().replace(' ', '') + 'Of'
                        else:
                            test_2 = 'has' + v_1.split(',')[0].split('-')[-1].title().replace(' ', '')
                            test_3 = 'is' + v_1.split(',')[0].split('-')[-1].title().replace(' ', '') + 'Of'
                        if '.json' not in v_1:
                            if inventory_int.return_onto_object(test_2 + 'Value', 'data_property') is None:
                                inventory_int.create_data_prop_with_inventory(test_2 + 'Value', owlready2.DataProperty)
                            inventory_int.place_data_with_inventory(sim_name, test_2 + 'Value', v_1)
                        else:
                            try:
                                test_6 = v_1.rstrip('.json').split(',')[1].title().replace(' ', '').replace('-', ' ').replace('+', '_')
                            except IndexError as ie:
                                print(ie)
                                test = ie
                            test_7 = f'{sim_name} {test_2} {test_6}'
                            test_7_1 = test_7
                            if inventory_int.return_onto_object(test_2, 'object_property') is None:
                                inventory_int.create_object_prop_with_inventory(test_2, owlready2.ObjectProperty)
                            if inventory_int.return_onto_object(test_3, 'object_property') is None:
                                inventory_int.create_object_prop_with_inventory(test_3, owlready2.ObjectProperty)
                            inventory_int.connect_indiv_obj_indiv_with_inventory(sim_name, test_2, test_6)
                            inventory_int.connect_indiv_obj_indiv_with_inventory(test_6, test_3, sim_name)
                            # inventory_int.connect_indiv_obj_indiv_with_inventory(new_name_int[1], test_2, test_6)
                            # inventory_int.connect_indiv_obj_indiv_with_inventory(test_6, test_3, new_name_int[1])
            else:
                test_4 = sim_instance_dicts





def dict_to_emmo_individual_1(dict_int, dict_of_excel_trans_int, list_sim_indiv, emmo_indiv, last_indiv):
    # list_sim_emmo_name = [inventory_int.return_onto_object(sim_indiv, 'individual')for sim_indiv in list_sim_indiv]
    for key_int, value_int in dict_int.items():
        name_for_trans_check = key_int.split('-')[0].rstrip(' ') + key_int.split('-')[2]
        if isinstance(value_int, (dict, OrderedDict)):
            if name_for_trans_check in list(dict_of_excel_trans_int['Dict_name'].values()):
                indiv_class = dict_of_excel_trans_int['Onto_name'][list(dict_of_excel_trans_int['Dict_name'].keys())[
                    list(dict_of_excel_trans_int['Dict_name'].values()).index(name_for_trans_check)]]
                if key_int.split('-')[2]:
                    new_indiv_name = key_int.split('-')[1] + '_' + key_int.split('-')[2].title().replace(' ', '')
                    inventory_int.create_indiv_with_inventory(new_indiv_name, indiv_class)
                    for sim_indiv_name in list_sim_indiv:
                        # inventory_int.connect_indiv_obj_indiv_with_inventory(new_indiv_name,
                        #                                                      'hasSimulation',
                        #                                                      sim_indiv_name)
                        inventory_int.connect_indiv_obj_indiv_with_inventory(sim_indiv_name,
                                                                             'hasIndividual',
                                                                              new_indiv_name)
                    inventory_int.connect_indiv_obj_indiv_with_inventory(emmo_indiv,
                                                                         'hasIndividual',
                                                                         new_indiv_name)
                    # if not last_indiv != new_indiv_name:
                    #     create_and_link_property_1(key_int.split('-')[2].title().replace(' ', ''),
                    #                                owlready2.ObjectProperty, last_indiv, new_indiv_name)
                    # if not last_indiv != new_indiv_name:
                    create_and_link_property_1(key_int.split('-')[2].title().replace(' ', ''),
                                               owlready2.ObjectProperty, last_indiv, new_indiv_name)
                    dict_to_emmo_individual_1(value_int, dict_of_excel_trans_int, list_sim_indiv, emmo_indiv,
                                              new_indiv_name)
                else:
                    new_indiv_name = last_indiv
                    dict_to_emmo_individual_1(value_int, dict_of_excel_trans_int, list_sim_indiv, emmo_indiv,
                                              new_indiv_name)
            else:
                print(f'Name not found1: {name_for_trans_check} \n with key_int {key_int}')
        elif isinstance(value_int, (str, list)):
            new_indiv_name = key_int.split('-')[1] + '_' + key_int.split('-')[2].title().replace(' ', '')
            if 'Individuals_json_Links' in key_int:
                if not isinstance(value_int, str):
                    for i_1 in value_int:
                        name_to_check = i_1.strip('.json').split(',')[-1].title().replace(' ', '').replace('+', '_')
                        if name_to_check in list(inventory_int.dataframe_of_individuals.prefLabel):
                            inventory_int.connect_indiv_obj_indiv_with_inventory(emmo_indiv,
                                                                                 'hasDefinedIndividual',
                                                                                 name_to_check)
                        else:
                            print('Individual not found: ', name_to_check)
                else:
                    name_to_check = value_int.strip('.json').split(',')[-1].title().replace(' ', '').replace('+', '_')
                    if name_to_check in [item for item in inventory_int.dataframe_of_individuals.prefLabel]:
                        inventory_int.connect_indiv_obj_indiv_with_inventory(emmo_indiv,
                                                                             'hasDefinedIndividual',
                                                                             name_to_check)
                    else:
                        print('Individual not found: ', name_to_check)
            elif ('Option' in key_int) & (last_indiv == emmo_indiv):
                inventory_int.place_data_with_inventory(emmo_indiv, 'hasOption', value_int)
            elif 'Option' in key_int:
                inventory_int.place_data_with_inventory(last_indiv, 'hasOption', value_int)
            elif name_for_trans_check in list(dict_of_excel_trans_int[
                                                  'Dict_name'].values()):
                # todo implementation of connection between individuals
                indiv_class = dict_of_excel_trans_int['Onto_name'][list(dict_of_excel_trans_int['Dict_name'].keys())[
                    list(dict_of_excel_trans_int['Dict_name'].values()).index(name_for_trans_check)]]
                # new_indiv_name = key_int.split('-')[1] + '_' + key_int.split('-')[2].title().replace(' ', '')
                inventory_int.create_indiv_with_inventory(new_indiv_name, indiv_class)
                for sim_indiv in list_sim_indiv:
                    inventory_int.connect_indiv_obj_indiv_with_inventory(new_indiv_name, 'hasSimulation', sim_indiv)
                    inventory_int.connect_indiv_obj_indiv_with_inventory(sim_indiv, 'hasIndividual', new_indiv_name)
                create_and_link_property_1(new_indiv_name.split('_')[-1], owlready2.ObjectProperty, emmo_indiv, new_indiv_name)
                data_prop_name_check = 'has' + key_int.split('-')[2].replace(' ', '')
                if len(str(value_int).split('[')) == 2:
                    try:
                        indiv_value = float(value_int.split('[')[0])
                    except ValueError:
                        indiv_value = f'not a float:{value_int}'
                    indiv_unit = value_int.split('[')[1].rstrip(']')
                    pass
                    if inventory_int.return_onto_object(data_prop_name_check + 'Value', 'data_property') is None:
                        inventory_int.create_data_prop_with_inventory(data_prop_name_check + 'Value',
                                                                      owlready2.DataProperty)
                    if inventory_int.return_onto_object(data_prop_name_check + 'Unit', 'data_property') is None:
                        inventory_int.create_data_prop_with_inventory(data_prop_name_check + 'Unit',
                                                                      owlready2.DataProperty)
                    # inventory_int.place_data_with_inventory(new_indiv_name,
                    #                                         data_prop_name_check + 'Value',
                    #                                         indiv_value)
                    # inventory_int.place_data_with_inventory(new_indiv_name,
                    #                                         data_prop_name_check + 'Unit',
                    #                                         indiv_unit)
                    inventory_int.place_data_with_inventory(emmo_indiv,
                                                            data_prop_name_check + 'Value',
                                                            indiv_value)
                    inventory_int.place_data_with_inventory(emmo_indiv,
                                                            data_prop_name_check + 'Unit',
                                                            indiv_unit)
                else:
                    pass
                    if inventory_int.return_onto_object(data_prop_name_check + 'Value', 'data_property') is None:
                        inventory_int.create_data_prop_with_inventory(data_prop_name_check + 'Value',
                                                                      owlready2.DataProperty)
                    # inventory_int.place_data_with_inventory(new_indiv_name,
                    #                                         data_prop_name_check + 'Value',
                    #                                         value_int)
                    inventory_int.place_data_with_inventory(emmo_indiv,
                                                            data_prop_name_check + 'Value',
                                                            value_int)
                if last_indiv != emmo_indiv:  # todo change from has Setting to hasIndividual Name
                    inventory_int.connect_indiv_obj_indiv_with_inventory(last_indiv, 'hasSetting', emmo_indiv)
            else:
                print(f'Name not found2: {name_for_trans_check} \n with key_int {key_int}')
        else:
            print('Error')


def create_and_link_property_1(prop_name_base, prop_type, indiv_source, indiv_target,
                               basic_prop_name='hasProgramSetting', inverse_basic_prop_name='isProgramSettingOf'):
    if not prop_name_base:
        prop_name_check = basic_prop_name
        inverse_prop_name_check = inverse_basic_prop_name
    else:
        prop_name_check = 'has' + prop_name_base
        inverse_prop_name_check = 'is' + prop_name_base + 'Of'
    if type(prop_type) == owlready2.prop.ObjectPropertyClass:
        if inventory_int.return_onto_object(prop_name_check, 'object_property') is None:
            inventory_int.create_object_prop_with_inventory(prop_name_check, prop_type)
        inventory_int.connect_indiv_obj_indiv_with_inventory(indiv_source, prop_name_check, indiv_target)
        if inventory_int.return_onto_object(inverse_prop_name_check, 'object_property') is None:
            inventory_int.create_object_prop_with_inventory(inverse_prop_name_check, prop_type)
        inventory_int.connect_indiv_obj_indiv_with_inventory(indiv_target, inverse_prop_name_check, indiv_source)

    if type(prop_type) == owlready2.prop.DataPropertyClass:
        if inventory_int.return_onto_object(prop_name_check, 'data_property') is None:
            inventory_int.create_data_prop_with_inventory(prop_name_check, prop_type)
        inventory_int.onto_data_append(indiv_source, prop_name_check, indiv_target)