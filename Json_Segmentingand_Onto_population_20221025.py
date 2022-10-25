import os
import types
import json
import time
import copy
import owlready2
import matplotlib.pyplot as plt
import py_modules_for_onto.functions_for_populating_onto_testing_20221017 as ffpo
from py_modules_for_onto.Central_functions_for_Ontology_mod_20220810 import *
# from py_modules_for_onto.import_segmentationhierarchy_list_2022_08_10 import list_of_keys,\
#         tuple_list_of_named_inst, tuple_list_of_non_named_inst, dict_for_instance_renaming
import py_modules_for_onto.import_segmentationhierarchy_list_2022_08_10 as shl
import py_modules_for_onto.Tools_for_translator_template_20220805 as Tftt
import py_modules_for_onto.modify_ontologiy_by_adding_classes_functions_20220805 as mobcf
# import py_modules_for_onto.Functions_for_Segmentation_20220805 as FfS
import py_modules_for_onto.Functions_for_Segmentation_20221006_testing as FfS_t
# import py_modules_for_onto.Tries_of_implementing_mongo_db_20220805 as Toimdb
# import py_modules_for_onto.Tools_for_creating_own_KPIs_20220805 as TcKPI
import py_modules_for_onto.Tools_for_creating_own_KPIs_20220929 as TcKPI
import py_modules_for_onto.Add_properties_to_emmo_20221017 as Apte

# import openpyxl
# from openpyxl import load_workbook
# import timeit
import datetime
# from uuid import uuid1, uuid3, uuid4, uuid5

"""
Section for testing with Mongodb
"""
"""
see file tries_of_implementing_mongo_db
"""

"""
Section for choosing the correct file pathes
"""
# __selected_ontology__ = 'emmo-compacted-1-0-0-beta4.owl'
# __selected_ontology__ =  'emmo_inferred_20220216_trying_classes_2.rdf'
# __selected_ontology__ =  'emmo_inferred_20220216_trying_classes_2.rdf'
__selected_ontology__ = 'emmo-inferred-1-0-0-beta1.owl'
__onto_name_for_py__ = 'emmo'
__base_iri__ = 'http://emmo.info/emmo#'
__onto_namespace__ = 'http://emmo.info/emmo#'

if os.path.exists('C:/Users/smhhborg'):
    __Path_for_out_file_dicts__ = 'D:/Json_Dict_unmodified1'
    __owlready2_JAVA_EXE__ = 'C:/Users/smhhborg/Desktop/Protege-5.5.0-win/Protege-5.5.0/jre/bin/java.exe'
    # __owlready2_onto_path__ = 'C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis'
    __owlready2_onto_path__ = './Json_Dict_911_Simulations'
    __Read_Path_of_Translator__ = \
        './Translator_test_modified - Kopie.xlsx'
    __Write_Path_of_Translator__ = \
        './Translator_Templates/'
    __path_for_instances__ = 'D:/dict_inst_all_data_911_sims'
    __onto_write_path__ = './Ontologies'
    print(f'Hello smhhborg \n')
elif os.path.exists('H:/NicksDaten/Json_Dict_unmodified2/'):
    __Path_for_out_file_dicts__ = 'H:/NicksDaten/Json_Dict_unmodified2/'
    __owlready2_JAVA_EXE__ = 'C:/Users/hendr/Desktop/Protege-5.5.0/jre/bin/java.exe'
    __owlready2_onto_path__ = 'C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis'
    __Read_Path_of_Translator__ = \
        'C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis/Translator_test_modified - Kopie.xlsx'
    __Write_Path_of_Translator__ = \
        'C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis/Translator_Templates/'
    __path_for_instances__ = 'H:/NicksDaten/dict_inst_all_data_911_sims'
    __onto_write_path__ = 'C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis/Ontologies'
    print(f'Hello Hendrik \n')
else:
    print('please define new user at the start of File \' Test_for_adding_classes_to_ontology_fur_stud_testing.py \' \n'
          'and rerun code, otherwise define the following attributes : \n'
          ' - Path_for_out_file_dicts: \n'
          ' - owlready2_JAVA_EXE:      \n'
          ' - owlready2_onto_path:     \n'
          ' - Read_Path_of_Translator: \n'
          ' - path_for_instances:      \n'
          ' - onto_write_path:         \n'

          ' - selected_ontology:       \n'
          ' - onto_name_for_py:        \n'
          ' - base_iri:                \n'
          ' - onto_namespace:          \n')
    __Path_for_out_file_dicts__ = input('Path_for_out_file_dicts:')
    __owlready2_JAVA_EXE__ = input('owlready2_JAVA_EXE')
    __owlready2_onto_path__ = input('owlready2_onto_path')
    __Read_Path_of_Translator__ = input('Read_Path_of_Translator')
    __Write_Path_of_Translator__ = input('Write_Path_of_Translator')
    __path_for_instances__ = input('path_for_instances')
    __onto_write_path__ = input('onto_write_path')

    __selected_ontology__ = input('selected_ontology') or 'emmo-compacted-1-0-0-beta4.owl'
    __onto_name_for_py__ = input('onto_name_for_py') or 'emmo'
    __base_iri__ = input('base_iri') or 'http://emmo.info/emmo#'
    __onto_namespace__ = input('onto_namespace') or 'http://emmo.info/emmo#'

"""
Loading in dictionaries and cleaning them for Work
"""

all_sims = OrderedDict()
for __name__ in os.listdir(__Path_for_out_file_dicts__):
    # for name in os.listdir('C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis/Json_Dict_unmodified2'):
    if __name__.endswith(".json"):
        with open(__Path_for_out_file_dicts__ + '/' + __name__) as __outfile__:
            all_sims.update({__name__.rstrip('.json'): json.load(__outfile__)})

ffpo.change_filepath_name_in_dict(all_sims)

"""
Initializing Emmo for working with it
"""

__start__ = time.perf_counter()
world = World()
owlready2.JAVA_EXE = __owlready2_JAVA_EXE__
owlready2.onto_path.append(__owlready2_onto_path__)
emmo = world.get_ontology(__selected_ontology__)
emmo.name = __onto_name_for_py__
emmo.load()
emmo.sync_python_names()
emmo.base_iri = __base_iri__
namespace = emmo.get_namespace(__onto_namespace__)

"""
Section for adding classes into the Ontology
"""

__time_1__ = time.perf_counter()
dict_of_excel_translator = mobcf.read_in_dict_of_excel_translator(__Read_Path_of_Translator__)
emmo = mobcf.modify_ontology_by_adding_classes(dict_of_excel_translator, emmo)
__time_2__ = time.perf_counter()
# test = list_of_emmo_classes(emmo)
print('implementing Classes time', datetime.timedelta(seconds=time.perf_counter() - __time_1__))

emmo.save(os.path.join('C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis',
                       'emmo_with_classes_of_911_Sims.owl'))
"""
Section for loading preconstructed_ontology instead
"""

"""
Section for creating a template for the Translator by renaming dict entries by segmentation hierarchy list
"""
__time_2_1__ = time.perf_counter()
__time_trans_template__ = str(datetime.datetime.now()).replace('-', '') \
    .split('.')[0].replace(' ', '_').replace(':', '_')
__path_for_translator_template__ = __Write_Path_of_Translator__ + \
                                   f'Translator_test_modified_and_ready_for_testing_{__time_trans_template__}.xlsx'
__sims_for_trans_template__ = copy.deepcopy(all_sims)
__list_for_trans_template__ = copy.deepcopy(shl.list_of_keys)
Tftt.create_excel_file_for_translator(__path_for_translator_template__,
                                      __sims_for_trans_template__,
                                      __list_for_trans_template__)
print('Time for TranslatorTemplate', datetime.timedelta(seconds=time.perf_counter() - __time_2_1__))
__time_3__ = time.perf_counter()

"""
Section for Segmenting Json-dicts into archived Segments
"""

dict_for_instance_renaming_int = shl.create_dict_for_instance_renaming(__path_for_instances__)
tuple_list_of_named_inst_int = shl.tuple_list_of_named_inst
tuple_list_of_non_named_inst_int = shl.tuple_list_of_non_named_inst
__new_dict_for_inst_separation__ = copy.deepcopy(all_sims)
# FfS.archive_and_change_all_instances(dict_for_instance_renaming_int,
#                                      new_dict_for_inst_separation,
#                                      tuple_list_of_named_inst_int,
#                                      tuple_list_of_non_named_inst_int)
FfS_t.archive_and_change_all_instances(dict_for_instance_renaming_int,
                                       __new_dict_for_inst_separation__,
                                       tuple_list_of_named_inst_int,
                                       tuple_list_of_non_named_inst_int)
print('Time for segmenting', datetime.timedelta(seconds=time.perf_counter() - __time_3__))
__time_4__ = time.perf_counter()

"""
Section for Populating Segments into the Ontology
"""
emmo = Apte.add_basic_props_to_emmo(emmo)
__basic_path_for_instances__ = 'D:/dict_inst_all_data_2/'
__time_mes_int__ = []
owlready2.set_datatype_iri(float, "http://www.w3.org/2001/XMLSchema#float")
inventory_emmo = ffpo.ModifyOnto(world, emmo.base_iri, ['prefLabel', 'OntoThing'])
inventory_emmo.central_object_property = owlready2.ObjectProperty
inventory_emmo.central_data_property = owlready2.DataProperty
for __i__ in dict_for_instance_renaming_int:
    print(f'Started: {__basic_path_for_instances__ + __i__}')
    __time_mes_int__ = ffpo.search_instance_folder_and_insert_into_emmo_1(__basic_path_for_instances__ + __i__,
                                                                             dict_of_excel_translator,
                                                                             shl.tuple_list_of_named_inst,
                                                                             shl.tuple_list_of_non_named_inst,
                                                                             inventory_emmo)
    print(f'Finished: {__basic_path_for_instances__ + __i__}')
print('Finished')
print('Time for mapping', datetime.timedelta(seconds=time.perf_counter() - __time_4__))
emmo_1 = inventory_emmo.ontology
# test_2 = list_of_emmo_classes(emmo)
"""
Section for implementing KPIs into the ontology
"""
__time_5__ = time.perf_counter()
# KPIS, emmo_1 = TcKPI.create_add_and_save_kpis_in_ontology_and_images(all_sims, emmo_1)
KPIS = TcKPI.create_add_and_save_kpis_in_ontology_and_images(all_sims, inventory_emmo)
print('KPI implementation time', datetime.timedelta(seconds=time.perf_counter() - __time_5__))

"""
Section for cleaning naming scheme in the ontology 
"""

# for i in list_of_emmo_data_properties(emmo):
#     if not i[1].prefLabel:
#         i[1].prefLabel = [owlready2.locstr(i[1].name, lang='en')]
#         i[1].python_name = i[1].name
#
# for i in list_of_emmo_individuals(emmo):
#     if not i[1].prefLabel:
#         i[1].prefLabel = [owlready2.locstr(i[1].name, lang='en')]
#         i[1].python_name = i[1].name
#
print('Overall time', datetime.timedelta(seconds=time.perf_counter() - __start__))

"""
Section for saving emmo with dynamic timestamp
"""

__time_for_onto__ = str(datetime.datetime.now()).replace('-', '').split('.')[0].replace(' ', '_').replace(':', '_')
emmo_1.save(os.path.join(__onto_write_path__,
                         f'emmo_inferred_{__time_for_onto__}_trying_classes_all_data.owl'))
print(f'saved file: emmo_inferred_{__time_for_onto__}_trying_classes_all_data.owl')
plt.plot(range(len(__time_mes_int__)), __time_mes_int__)

"""
SPARQL-Querying with Owlready2 (very fast)
!!! Attention this is not regular SPARQL !!!
even though most of the syntax can be used
https://owlready2.readthedocs.io/en/latest/sparql.html
here only skos was required to be defined as emmo is self defined and rdfs,xml,... are predefined
"""

# sparql_results = list(world.sparql("""
# PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
# SELECT ?Sim_prefL ?Boundary ?individual_prefL ?Value
# WHERE {
#     ?indiv_class skos:prefLabel ?indiv_class_prefL .
#     ?individual a ?indiv_class .
#     ?individual skos:prefLabel ?individual_prefL .
#     ?individual emmo:hasSimulation ?Sim .
#     ?Sim skos:prefLabel ?Sim_prefL .
#     ?Sim emmo:hasUMommax_ConvValue ?Value .
#     ?Boundary emmo:hasDefinedIndividual ?individual .
#     ?BoundaryType emmo:hasIndividual ?Boundary .
#     ?BoundaryType emmo:hasBoundaryType ?Type .
#     FILTER(STR(?indiv_class_prefL) = "BoundaryComponentIndividual")
#     FILTER(?Value < 0.95)
#     FILTER(STR(?Type) = "INLET")
# }"""))
