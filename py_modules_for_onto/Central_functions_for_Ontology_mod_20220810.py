import emmopy
import ontopy
from ontopy import World
import owlready2
from mergedeep import merge
from collections import OrderedDict


world = World()

owlready2.JAVA_EXE = 'C:/Users/hendr/Desktop/Protege-5.5.0/jre/bin/java.exe'

owlready2.onto_path.append('C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis')
emmo_int_1 = world.get_ontology('emmo_inferred_20220216_trying_classes_2.rdf')
emmo_int_1.name = 'emmo'
emmo_int_1.load()
emmo_int_1.sync_python_names()
emmo_int_1.base_iri = "http://emmo.info/emmo#"


def list_of_emmo_classes(emmo_int=emmo_int_1):
    list_emmo_classes = list(emmo_int.classes())
    for i_1, i_2 in enumerate(list_emmo_classes):
        list_emmo_classes[i_1] = i_2.prefLabel
        list_emmo_classes[i_1] = [str(list_emmo_classes[i_1][0]), i_2]
    return list_emmo_classes


def list_of_emmo_data_properties(emmo_int=emmo_int_1):
    list_emmo_data_properties = list(emmo_int.data_properties())
    for i_1, i_2 in enumerate(list_emmo_data_properties):
        list_emmo_data_properties[i_1] = [i_2.get_python_name(), i_2]
    return list_emmo_data_properties


def list_of_emmo_object_properties(emmo_int=emmo_int_1):
    list_emmo_object_properties = list(emmo_int.object_properties())
    for i_1, i_2 in enumerate(list_emmo_object_properties):
        list_emmo_object_properties[i_1] = [i_2.get_python_name(), i_2]
    return list_emmo_object_properties


def list_of_emmo_individuals(emmo_int=emmo_int_1):
    list_emmo_individuals = list(emmo_int.individuals())
    for i_1, i_2 in enumerate(list_emmo_individuals):
        list_emmo_individuals[i_1] = [i_2.get_preflabel(), i_2]
    return list_emmo_individuals


def search_for_index(name_int, list_onto_classes_int):
    for i in list_onto_classes_int:
        if i[0] == name_int:
            onto_thing = i[1]
            return onto_thing
        else:
            pass


def create_merged_dict(dict_to_be_merged):
    dict_merged = OrderedDict()
    for i_4_int in dict_to_be_merged:
        merge(dict_merged, dict_to_be_merged[i_4_int])
    return dict_merged


def change_list_of_tuples_to_list_of_str(list_of_tuples):
    for i_1, i_2 in enumerate(list_of_tuples):
        if isinstance(i_2, tuple):
            new_str_for_list = ''
            for i_3 in i_2:
                new_str_for_list += ' ' + i_3
            list_of_tuples[i_1] = new_str_for_list.lstrip(' ')
    return list_of_tuples
