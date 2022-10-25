from collections import OrderedDict


list_of_instance_keys = [
    # 'LIBRARY',
    'COMMAND FILE',
    'SIMULATION CONTROL',
    'PARAMETERIZATION'
]

list_of_instance_sub_keys = [
    'CEL',
    'EXECUTABLE SELECTION',
    'INTERPOLATOR STEP CONTROL',
    'PARALLEL HOST LIBRARY',
    'PARTITIONER STEP CONTROL',
    'RUN DEFINITION',
    'SOLVER STEP CONTROL'
]

list_of_keys_containing_named_instances = [
    'EXPRESSIONS',
    'FUNCTION',
    'MATERIAL',
    'FLOW',
    'HOST DEFINITION',
    'INPUT FIELD'
]

list_of_keys_containing_named_sub_instances = [
    ('FUNCTION', 'DATA FIELD'),
    ('FLOW', 'DOMAIN'),
    ('FLOW', 'DOMAIN INTERFACE')
]

list_of_keys_containing_non_named_sub_instances_in_named_instances = [
    ('FLOW', 'SOLVER CONTROL'),
    ('FLOW', 'ANALYSIS TYPE'),
    ('FLOW', 'SOLUTION UNITS'),
    ('FLOW', 'OUTPUT CONTROL')
]

list_of_keys_containing_named_sub_sub_instances = [
    ('FLOW', 'DOMAIN', 'BOUNDARY'),
    ('FLOW', 'DOMAIN', 'FLUID DEFINITION'),
    ('FLOW', 'DOMAIN', 'SOLID DEFINITION'),
    ('FLOW', 'OUTPUT CONTROL', 'MONITOR POINT'),
    ('FLOW', 'SOLVER CONTROL', 'EQUATION CLASS')
]

list_of_keys_containing_non_named_sub_sub_instances_in_named_instances = [
    ('FLOW', 'DOMAIN', 'FLUID MODELS'),
    ('FLOW', 'DOMAIN', 'DOMAIN MODELS'),
    ('FLOW', 'DOMAIN', 'SOLID MODELS'),
    ('FLOW', 'DOMAIN', 'SUBDOMAIN'),
    ('FLOW', 'DOMAIN INTERFACE', 'INTERFACE MODELS')
]

list_of_keys_containing_named_sub_sub_sub_instances = [
    ('FLOW', 'DOMAIN', 'BOUNDARY', 'COMPONENT'),
    ('FLOW', 'DOMAIN', 'FLUID MODELS', 'COMPONENT'),
    ('FLOW', 'DOMAIN', 'SUBDOMAIN', 'EQUATION SOURCE')
]


list_of_keys = list_of_keys_containing_named_sub_sub_sub_instances + \
                   list_of_keys_containing_named_sub_sub_instances + \
                   list_of_keys_containing_named_sub_instances + \
                   list_of_keys_containing_named_instances + \
                   list_of_instance_sub_keys + \
                   list_of_instance_keys + \
                   list_of_keys_containing_non_named_sub_instances_in_named_instances + \
                   list_of_keys_containing_non_named_sub_sub_instances_in_named_instances

tuple_list_of_named_inst = list_of_keys_containing_named_sub_sub_sub_instances + \
                           list_of_keys_containing_named_sub_sub_instances + \
                           list_of_keys_containing_named_sub_instances + \
                           list_of_keys_containing_named_instances

tuple_list_of_non_named_inst = list_of_instance_sub_keys + \
                               list_of_instance_keys + \
                               list_of_keys_containing_non_named_sub_instances_in_named_instances + \
                               list_of_keys_containing_non_named_sub_sub_instances_in_named_instances

dict_for_instance_renaming = OrderedDict({
    'named_sub_sub_sub_inst': {'list_instances_tbc': list_of_keys_containing_named_sub_sub_sub_instances,
                               'path': 'D:/dict_inst_all_data_2/named_sub_sub_sub_inst/'},
    'non_named_sub_sub_inst': {
        'list_instances_tbc': list_of_keys_containing_non_named_sub_sub_instances_in_named_instances,
        'path': 'D:/dict_inst_all_data_2/non_named_sub_sub_inst/'},
    'named_sub_sub_inst': {'list_instances_tbc': list_of_keys_containing_named_sub_sub_instances,
                           'path': 'D:/dict_inst_all_data_2/named_sub_sub_inst/'},
    'non_named_sub_inst': {'list_instances_tbc': list_of_keys_containing_non_named_sub_instances_in_named_instances,
                           'path': 'D:/dict_inst_all_data_2/non_named_sub_inst/'},
    'named_sub_inst': {'list_instances_tbc': list_of_keys_containing_named_sub_instances,
                       'path': 'D:/dict_inst_all_data_2/named_sub_inst/'},
    'named_inst': {'list_instances_tbc': list_of_keys_containing_named_instances,
                   'path': 'D:/dict_inst_all_data_2/named_inst/'},
    'sub_inst': {'list_instances_tbc': list_of_instance_sub_keys,
                 'path': 'D:/dict_inst_all_data_2/sub_inst/'},
    'inst': {'list_instances_tbc': list_of_instance_keys,
             'path': 'D:/dict_inst_all_data_2/inst/'}
})


def create_dict_for_instance_renaming(path_int):
    dict_for_instance_renaming_int = OrderedDict({
        'named_sub_sub_sub_inst': {'list_instances_tbc': list_of_keys_containing_named_sub_sub_sub_instances,
                                   'path': f'{path_int}/named_sub_sub_sub_inst/'},
        'non_named_sub_sub_inst': {
            'list_instances_tbc': list_of_keys_containing_non_named_sub_sub_instances_in_named_instances,
            'path': f'{path_int}/non_named_sub_sub_inst/'},
        'named_sub_sub_inst': {'list_instances_tbc': list_of_keys_containing_named_sub_sub_instances,
                               'path': f'{path_int}/named_sub_sub_inst/'},
        'non_named_sub_inst': {'list_instances_tbc': list_of_keys_containing_non_named_sub_instances_in_named_instances,
                               'path': f'{path_int}/non_named_sub_inst/'},
        'named_sub_inst': {'list_instances_tbc': list_of_keys_containing_named_sub_instances,
                           'path': f'{path_int}/named_sub_inst/'},
        'named_inst': {'list_instances_tbc': list_of_keys_containing_named_instances,
                       'path': f'{path_int}/named_inst/'},
        'sub_inst': {'list_instances_tbc': list_of_instance_sub_keys,
                     'path': f'{path_int}/sub_inst/'},
        'inst': {'list_instances_tbc': list_of_instance_keys,
                 'path': f'{path_int}/inst/'}
    })
    return dict_for_instance_renaming_int

