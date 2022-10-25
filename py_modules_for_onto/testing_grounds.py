# from Test_for_adding_classes_to_ontology_functions_4_cleaned import *
import pandas as pd
from py_modules_for_onto.Central_functions_for_Ontology_mod_20220810 import list_of_emmo_data_properties, \
    list_of_emmo_individuals, list_of_emmo_classes, list_of_emmo_object_properties
import os
import types
from ontopy import World
import owlready2

# owlready2.reasoning.JAVA_MEMORY = 1000


# world = World()


# try:
#     if os.path.exists('C:/Users/hendr/Desktop/Protege-5.5.0/jre/bin/java.exe'):
#         owlready2.JAVA_EXE = 'C:/Users/hendr/Desktop/Protege-5.5.0/jre/bin/java.exe'
#     elif os.path.exists('C:/Users/smhhborg/Desktop/Protege-5.5.0-win/Protege-5.5.0/jre/bin/java.exe'):
#         owlready2.JAVA_EXE = 'C:/Users/smhhborg/Desktop/Protege-5.5.0-win/Protege-5.5.0/jre/bin/java.exe'
#     else:
#         raise FileNotFoundError
# except FileNotFoundError:
#     print('file not found')
#
# try:
#     if os.path.exists('C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis'):
#         owlready2.onto_path.append('C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis')
#     elif os.path.exists('C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis'):
#         owlready2.onto_path.append('C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis')
#     else:
#         raise FileNotFoundError
# except FileNotFoundError:
#     print('file not found')
#
# emmo = world.get_ontology('Ontologies/emmo_inferred_20220804_15_55_02_trying_classes_all_data.owl')
# emmo.name = 'emmo'
# emmo.load()
# emmo.sync_python_names()
# # emmo.base_iri = "http://emmo.info/emmo#"
#
# with emmo:
#     namespace = 'emmo'
#     ProgramSettings = types.new_class('ProgramSettings', (emmo.Symbolic,))
#     emmo.ProgramSettings.prefLabel = 'ProgramSettings'
#     DomainSettings = types.new_class('DomainSettings', (emmo.ProgramSettings,))
#     emmo.DomainSettings.prefLabel = 'DomainSettings'
#
# emmo.save(os.path.join('C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis',
#                        'emmo_inferred_20220216_trying_classes_3_2_1.owl'))
# test = os.path.exists('C:/Users/hendr/Desktop/Protege-5.5.0/jre/bin/java.exe')


# def list_of_emmo_classes(emmo_int=emmo):
#     list_emmo_classes = list(emmo_int.classes())
#     for i_1, i_2 in enumerate(list_emmo_classes):
#         list_emmo_classes[i_1] = i_2.prefLabel
#         try:
#             list_emmo_classes[i_1] = [str(list_emmo_classes[i_1][0]), i_2]
#         except IndexError:
#             print(i_1, i_2)
#     return list_emmo_classes


# def list_of_emmo_data_properties(emmo_int=emmo):
#     list_emmo_data_properties = list(emmo_int.data_properties())
#     for i_1, i_2 in enumerate(list_emmo_data_properties):
#         list_emmo_data_properties[i_1] = [i_2.get_python_name(), i_2]
#     return list_emmo_data_properties


# def list_of_emmo_object_properties(emmo_int=emmo):
#     list_emmo_object_properties = list(emmo_int.object_properties())
#     for i_1, i_2 in enumerate(list_emmo_object_properties):
#         list_emmo_object_properties[i_1] = [i_2.get_python_name(), i_2]
#     return list_emmo_object_properties


# def list_of_emmo_individuals(emmo_int=emmo):
#     list_emmo_individuals = list(emmo_int.individuals())
#     for i_1, i_2 in enumerate(list_emmo_individuals):
#         list_emmo_individuals[i_1] = [i_2.get_preflabel(), i_2]
#     return list_emmo_individuals


# from owlready2 import comment
# comment[emmo.DomainSettings, owlready2.rdfs_subclassof, emmo.ProgramSettings] = 'test_12345'
# emmo.save(os.path.join('C:/Users/smhhborg/Documents/GitHub/Hendrik_Borgelt_Masterthesis',
#                        'emmo_inferred_20220216_trying_classes_5_4_3_2_1.owl'))


class ModifyOnto:
    """
    Central Class for creating an Inventory of an Ontology, which keeps it up to date, by updating the inventory when a
    ontology object is introduced via the method
    """
    def __init__(self,
                 world: owlready2.namespace.World,
                 ontology_iri: str,
                 columns_list: list[str],
                 onto_subject: str | None = None,
                 onto_predicate: str | None = None,
                 onto_object: str | None = None,
                 onto_superclass_class: str | None = None,
                 onto_class: str | None = None,
                 onto_current_individual: str | None = None,
                 onto_super_object_property: str | None = None,
                 onto_object_property: str | None = None,
                 onto_super_data_property: str | None = None,
                 onto_data_property: str | None = None,
                 subject_str_int: str | None = None,
                 obj_str_int: str | None = None,
                 central_object_property: owlready2.prop.ObjectPropertyClass = None,
                 central_data_property: owlready2.prop.DataPropertyClass = None):
        """
        :param world: World object containing the Ontology, if none has been created use DefaultWord as given by
                      owlready2
        :param ontology_iri:
        :param columns_list:
        :param onto_subject:
        :param onto_predicate:
        :param onto_object:
        :param onto_superclass_class:
        :param onto_class:
        :param onto_current_individual:
        :param onto_super_object_property:
        :param onto_object_property:
        :param onto_super_data_property:
        :param onto_data_property:
        :param subject_str_int:
        :param obj_str_int:
        :param central_object_property:
        :param central_data_property:
        """
        self.world = world
        self.ontology = self.world.ontologies[ontology_iri]
        self.columns_list = columns_list
        self.dataframe_of_classes \
            = pd.DataFrame(list_of_emmo_classes(self.world)).set_axis(self.columns_list, axis='columns')
        self.dataframe_of_individuals \
            = pd.DataFrame(list_of_emmo_individuals(self.world)).set_axis(self.columns_list, axis='columns')
        self.dataframe_of_object_properties \
            = pd.DataFrame(list_of_emmo_object_properties(self.world)).set_axis(self.columns_list, axis='columns')
        self.dataframe_of_data_properties \
            = pd.DataFrame(list_of_emmo_data_properties(self.world)).set_axis(self.columns_list, axis='columns')
        self.onto_subject = onto_subject
        self.onto_predicate = onto_predicate
        self.onto_object = onto_object
        self.onto_superclass_class = onto_superclass_class
        self.onto_class = onto_class
        self.onto_current_individual = onto_current_individual
        self.onto_super_object_property = onto_super_object_property
        self.onto_object_property = onto_object_property
        self.onto_super_data_property = onto_super_data_property
        self.onto_data_property = onto_data_property
        self.subject_str_int = subject_str_int
        self.obj_str_int = obj_str_int
        self.central_object_property = central_object_property
        self.central_data_property = central_data_property

    def create_new_class(self):  # todo Security protocols
        new_class = types.new_class(self.onto_class, (self.onto_superclass_class,))
        new_class.prefLabel = self.onto_class
        intermediate_list = [new_class.prefLabel[0], new_class]  # todo must the new_class variable be closed?
        intermediate_data_frame = pd.DataFrame(intermediate_list).T
        intermediate_data_frame.columns = self.columns_list
        self.dataframe_of_classes = pd.concat([self.dataframe_of_classes, intermediate_data_frame],
                                              ignore_index=True)

    def create_individual_connection(self):  # todo Security protocols
        onto_individual = self.onto_class(self.onto_current_individual)
        onto_individual.prefLabel = self.onto_current_individual
        intermediate_list = [onto_individual.get_preflabel(),
                             onto_individual]  # todo must the new_class variable be closed?
        intermediate_data_frame = pd.DataFrame(intermediate_list).T
        intermediate_data_frame.columns = self.columns_list
        self.dataframe_of_individuals = pd.concat([self.dataframe_of_individuals, intermediate_data_frame],
                                                  ignore_index=True)

    def create_object_property(self):  # todo Security protocols
        with self.ontology:
            new_object_property = types.new_class(self.onto_object_property, (self.onto_super_object_property,))
            new_object_property.prefLabel = self.onto_object_property
            intermediate_list = [new_object_property.get_preferred_label(),
                                 new_object_property]  # todo must the new_class variable be closed?
            intermediate_data_frame = pd.DataFrame(intermediate_list).T
            intermediate_data_frame.columns = self.columns_list
            self.dataframe_of_object_properties = pd.concat([self.dataframe_of_object_properties,
                                                             intermediate_data_frame],
                                                            ignore_index=True)

    def create_data_property(self):  # todo Security protocols
        with self.ontology:
            new_data_property = types.new_class(self.onto_data_property, (self.onto_super_data_property,))
            new_data_property.prefLabel = self.onto_data_property
            intermediate_list = [new_data_property.get_preferred_label(),
                                 new_data_property]  # todo must the new_class variable be closed?
            intermediate_data_frame = pd.DataFrame(intermediate_list).T
            intermediate_data_frame.columns = self.columns_list
            self.dataframe_of_data_properties = pd.concat([self.dataframe_of_data_properties,
                                                           intermediate_data_frame],
                                                          ignore_index=True)

    def return_onto_object(self, name_int, type_int):
        """
        correct keywords 'class', 'individual', 'object_property', 'data_property'
        :param name_int:
        :param type_int:
        :return:
        """
        try:
            if type_int == 'class':
                object_int = self.dataframe_of_classes[
                    self.dataframe_of_classes[
                        self.columns_list[0]] == name_int][self.columns_list[1]].to_list()[0]
            elif type_int == 'individual':
                object_int = self.dataframe_of_individuals[
                    self.dataframe_of_individuals[
                        self.columns_list[0]] == name_int][self.columns_list[1]].to_list()[0]
            elif type_int == 'object_property':
                object_int = self.dataframe_of_object_properties[
                    self.dataframe_of_object_properties[
                        self.columns_list[0]] == name_int][self.columns_list[1]].to_list()[0]
            elif type_int == 'data_property':
                object_int = self.dataframe_of_data_properties[
                    self.dataframe_of_data_properties[
                        self.columns_list[0]] == name_int][self.columns_list[1]].to_list()[0]
            else:
                print('type or object not found')
                object_int = []
            return object_int
        except IndexError:
            return None

    def onto_object_append(self):
        try:
            if self.onto_subject is None:
                test_0 = True
                raise KeyError
            if self.onto_predicate is None:
                test_1 = True
                raise KeyError
            if self.onto_object is None:
                test_2 = True
                raise KeyError
            else:
                with self.ontology:
                    if self.onto_subject.__getattr__(self.onto_predicate) is None:
                        # exec('self.ontology.%s.%s = [self.ontology.%s]' % (self.subject_str_int, self.onto_predicate, self.obj_str_int))
                        setattr(self.onto_subject, self.onto_predicate, [self.onto_object])
                    else:
                        self.onto_subject.__getattr__(self.onto_predicate).append(self.onto_object)
        except ValueError:
            print(ValueError, self.onto_subject, self.onto_predicate, self.onto_object)
        except KeyError:
            print(KeyError, self.onto_subject, self.onto_predicate, self.onto_object)

    def clear_modonto(self):
        self.onto_subject = None
        self.onto_predicate = None
        self.onto_object = None
        self.onto_superclass_class = None
        self.onto_class = None
        self.onto_current_individual = None
        self.onto_super_object_property = None
        self.onto_object_property = None
        self.onto_super_data_property = None
        self.onto_data_property = None
        self.subject_str_int = None
        self.obj_str_int = None

    def create_indiv_with_inventory(self, indiv_str, class_str):
        """

        :param indiv_str:
        :param class_str:
        :return:
        """
        # with self.ontology:
        self.onto_class = self.return_onto_object(class_str, 'class')
        self.onto_current_individual = indiv_str
        self.create_individual_connection()
        self.clear_modonto()

    def connect_indiv_obj_indiv_with_inventory(self, subject_str, predicate_str, object_str):
        """

        :param subject_str:
        :param predicate_str:
        :param object_str:
        :return:
        """
        # with self.ontology:
        # if self.return_onto_object(predicate_str, 'object_property') is None:
        #     self.create_object_prop_with_inventory(predicate_str, self.central_object_property)
        self.onto_subject = self.return_onto_object(subject_str, 'individual')
        self.onto_predicate = predicate_str
        self.onto_object = self.return_onto_object(object_str, 'individual')
        self.subject_str_int = subject_str
        self.obj_str_int = object_str
        self.onto_object_append()
        self.clear_modonto()

    def create_data_prop_with_inventory(self, data_prop_str, super_data_construct):
        """

        :param data_prop_str:
        :param super_str:
        :return:
        """
        # with self.ontology:
        # self.onto_super_data_property = self.return_onto_object(super_str, 'data_property')
        self.onto_super_data_property = super_data_construct
        self.onto_data_property = data_prop_str
        self.create_data_property()
        self.clear_modonto()

    def create_object_prop_with_inventory(self, object_prop_str, super_str):
        """

        :param object_prop_str:
        :param super_str:
        :return:
        """
        # with self.ontology:
        self.onto_super_object_property = super_str
        self.onto_object_property = object_prop_str
        self.create_object_property()
        self.clear_modonto()

    def onto_data_append(self) -> None:
        # with self.ontology:
        try:
            if self.onto_subject is None:
                test_0 = True
                raise AttributeError
            if self.onto_predicate is None:
                raise AttributeError
            if self.onto_object is None:
                raise AttributeError
            else:
                with self.ontology:
                    if self.onto_subject.__getattr__(self.onto_predicate) is None:
                        setattr(self.onto_subject, self.onto_predicate, [self.onto_object])
                    else:
                        self.onto_subject.__getattr__(self.onto_predicate).append(self.onto_object)
        except ValueError as ve:
            print(ValueError, ve, self.onto_subject, self.onto_predicate, self.onto_object)
        except TypeError:
            print(TypeError, 'data')
        except AttributeError as ae:
            # pass
            print(AttributeError, ae, '\'data\'', self.onto_subject, self.onto_predicate, self.onto_object)

    def place_data_with_inventory(self,
                                  subject_str: str,
                                  predicate_str: str,
                                  data_str_or_float: str | float | int) -> None:
        """
        :param subject_str:
        :param predicate_str:
        :param data_str_or_float:
        :return:
        """
        # with self.ontology:
        #     if self.return_onto_object(predicate_str, 'data_property') is None:
        #         self.create_data_prop_with_inventory(predicate_str, self.central_data_property)
        self.onto_subject = self.return_onto_object(subject_str, 'individual')
        self.onto_predicate = predicate_str
        self.onto_object = data_str_or_float
        self.subject_str_int = subject_str
        self.obj_str_int = data_str_or_float
        self.onto_data_append()
        self.clear_modonto()

    # {'data_property': owlready2.prop.DataPropertyClass,
    # 'object_property': owlready2.prop.ObjectPropertyClass,
    # 'class': type(owlready2.entity.ThingClass),
    # 'individual':type(type(owlready2.entity.ThingClass))}

# A = ModifyOnto(emmo, ['prefLabel', 'OntoThing'])
# A.onto_class = A.return_onto_object('DomainIndividual','class')
# A.onto_individual = 'test'
# A.create_individual_connection


# define_datatype_in_ontology(Hex, "http://www.w3.org/2001/XMLSchema#hexBinary", onto)

# emmo_2 = world.get_ontology('emmo-inferred-1-0-0-beta4.owl')
# emmo_2.name = 'emmo'
# emmo_2.load()
# emmo_2.sync_reasoner(reasoner='HermiT')
