from py_modules_for_onto.Central_functions_for_Ontology_mod_20220810 import *
import types
import pandas as pd


def read_in_dict_of_excel_translator(path_int):
    df_1 = pd.read_excel(path_int, sheet_name='For testing on Components 3')
    dict_of_excel_translator_int = df_1.to_dict()
    dict_of_excel_translator_int['Implementation_Check'] = dict(zip(
        list(range(len(dict_of_excel_translator_int['Onto_superclass']))),
        [False] * len(dict_of_excel_translator_int['Onto_superclass'])))
    return dict_of_excel_translator_int


def add_static_classes_to_emmo(emmo=emmo_int_1):
    with emmo:
        namespace = 'emmo'
        ProgramSettings = types.new_class('ProgramSettings', (emmo.Symbolic,))
        emmo.ProgramSettings.prefLabel = 'ProgramSettings'
        DomainSettings = types.new_class('DomainSettings', (emmo.ProgramSettings,))
        emmo.DomainSettings.prefLabel = 'DomainSettings'
        CfxFunctionSetting = types.new_class('CfxFunctionSetting', (emmo.ProgramSettings,))
        emmo.CfxFunctionSetting.prefLabel = 'CfxFunctionSetting'
        ParallelHostSettings = types.new_class('ParallelHostSettings', (emmo.ProgramSettings,))
        emmo.ParallelHostSettings.prefLabel = 'ParallelHostSettings'
        MaterialSettings = types.new_class('MaterialSettings', (emmo.ProgramSettings,))
        emmo.MaterialSettings.prefLabel = 'MaterialSettings'
        InputFieldSettings = types.new_class('InputFieldSettings', (emmo.ProgramSettings,))
        emmo.InputFieldSettings.prefLabel = 'InputFieldSettings'
        CfxFunctionDataField = types.new_class('CfxFunctionDataField', (emmo.ProgramSettings,))
        emmo.CfxFunctionDataField.prefLabel = 'CfxFunctionDataField'
        MathematicalSimulations = types.new_class('MathematicalSimulations', (emmo.Symbolic,))
        emmo.MathematicalSimulations.prefLabel = 'MathematicalSimulations'
    return emmo


def modify_ontology_by_adding_classes(dict_of_excel_translator_int, emmo_int=emmo_int_1):
    emmo_int = add_static_classes_to_emmo(emmo_int)
    n_iter_counter = 0
    length_of_emmo_classes_before = len(list_of_emmo_classes(emmo_int))
    while (bool(n_iter_counter <= 10) & bool(not (all(dict_of_excel_translator_int['Implementation_Check']) & bool(
            dict_of_excel_translator_int['Implementation_Check'][0] is False)))):
        n_iter_counter += 1
        list_onto_superclass = list(dict_of_excel_translator_int['Onto_superclass'].values())
        list_onto_name = list(dict_of_excel_translator_int['Onto_name'].values())
        list_dict_names = list(dict_of_excel_translator_int['Dict_name'].values())
        list_implementation_check = list(dict_of_excel_translator_int['Implementation_Check'].values())
        zipped_list = zip(list_onto_superclass,
                          list_onto_name,
                          list_dict_names,
                          list_implementation_check)
        for iterator, (item_1, item_2, item_3, item_4) in enumerate(zipped_list):
            list_onto_classes = list_of_emmo_classes(emmo_int)
            if bool(not item_4) & bool(item_1 in list([i_1[0] for i_1 in list_onto_classes])):
                dict_of_excel_translator_int['Implementation_Check'][iterator] = True
                with emmo_int:
                    new_class = types.new_class(item_2, (search_for_index(item_1, list_onto_classes),))
                    new_class.prefLabel = [owlready2.locstr(item_2, lang='en')]
    print('number of EMMO.classes added:   ', len(list_of_emmo_classes(emmo_int)) - length_of_emmo_classes_before)
    print('number of EMMO.classes missing: ', len(dict_of_excel_translator_int['Implementation_Check']) - (
            len(list_of_emmo_classes(emmo_int)) - length_of_emmo_classes_before))
    return emmo_int
