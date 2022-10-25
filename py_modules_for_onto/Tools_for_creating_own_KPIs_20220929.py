import emmopy
import owlready2
from py_modules_for_onto.Central_functions_for_Ontology_mod_20220810 import *
from py_modules_for_onto.testing_grounds import *
import types
import numpy as np
import matplotlib.pyplot as plt
# import ontopy

global inventory_int

# world = World()
#
# owlready2.JAVA_EXE = 'C:/Users/hendr/Desktop/Protege-5.5.0/jre/bin/java.exe'
#
# owlready2.onto_path.append('C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis')
# emmo = world.get_ontology('emmo_inferred_20220216_trying_classes_2.rdf')
# emmo.name = 'emmo'
# emmo.load()
# emmo.sync_python_names()
# emmo.base_iri = "http://emmo.info/emmo#"


def add_own_kpis_and_save_figs(all_sims_int):
    new_con_dict = dict()
    for i_1_int in all_sims_int:
        plt.close()
        try:
            dict_section_with_data_int = all_sims_int[i_1_int]['Solver']['Convergence History']['Iterations']
            data_dict = dict()
            data_dict.update({i_3_int: {'Rate': [], 'RMS Res': [], 'Max Res': []} for i_3_int in
                              dict_section_with_data_int['1']['Equation']})
            for i_2_int in 'Rate', 'RMS Res', 'Max Res':
                for i_4_int, i_5_int in enumerate(dict_section_with_data_int['1']['Equation']):
                    data_dict[i_5_int][i_2_int].extend([float(dict_section_with_data_int[i_6_int][i_2_int][
                                                                  dict_section_with_data_int['1']['Equation'].index(
                                                                      i_5_int)]) for i_6_int in
                                                        dict_section_with_data_int])
            for i_7_int in data_dict:
                data_dict[i_7_int].update({'Cleaned_Conv_without_Plateau': []})
                for i_8_int in data_dict[i_7_int]['RMS Res'][2:]:
                    if i_8_int > (data_dict[i_7_int]['RMS Res'][-1] * 1.5):
                        data_dict[i_7_int]['Cleaned_Conv_without_Plateau'].append(i_8_int)
                data_dict[i_7_int].update({'Convergence_Rate': np.divide(
                    np.add(np.array(data_dict[i_7_int]['Cleaned_Conv_without_Plateau'][1:]),
                           -np.array([data_dict[i_7_int]['RMS Res'][-1]] * len(
                               data_dict[i_7_int]['Cleaned_Conv_without_Plateau'][:-1]))),
                    np.add(np.array(data_dict[i_7_int]['Cleaned_Conv_without_Plateau'][:-1]),
                           -np.array([data_dict[i_7_int]['RMS Res'][-1]] * len(
                               data_dict[i_7_int]['Cleaned_Conv_without_Plateau'][:-1]))))})
                try:
                    data_dict[i_7_int].update({'min_Conv': data_dict[i_7_int]['Convergence_Rate'].min()})
                    data_dict[i_7_int].update({'max_Conv': data_dict[i_7_int]['Convergence_Rate'].max()})
                    data_dict[i_7_int].update({'arit_mean_Conv': data_dict[i_7_int]['Convergence_Rate'].mean()})
                    try:
                        data_dict[i_7_int].update(
                            {'geo_mean_Conv': np.power(np.prod(data_dict[i_7_int]['Convergence_Rate']),
                                                       (1 / data_dict[i_7_int]['Convergence_Rate'].size))})
                    except:
                        pass
                    # plt.ioff()
                    # # colors_int = ['r', 'y', 'c', 'g', 'b', 'k', 'm']
                    # for i_15_int, i_10_int in enumerate(data_dict):
                    #     # plt.semilogy(range(len(data_dict[i_10_int]['Cleaned_Conv_without_Plateau'])),
                    #     #              data_dict[i_10_int]['Cleaned_Conv_without_Plateau'], color=colors_int[i_15_int])
                    #     plt.semilogy(range(len(data_dict[i_10_int]['RMS Res'])),
                    #                  data_dict[i_10_int]['RMS Res'],
                    #                  color='k')  # color=colors_int[i_15_int])
                    #     plt.xlabel('Iterations [-]')
                    #     plt.ylabel('RMS Residual of [-]')
                    #     plt.grid(True)
                    #     plt.xlim(0,len(data_dict[i_10_int]['RMS Res']))
                    #     # plt.semilogy(range(len(data_dict[i_10_int]['RMS Res'])),
                    #     #              [data_dict[i_10_int]['RMS Res'][-1] for i in
                    #     #               range(len(data_dict[i_10_int]['RMS Res']))],
                    #     #               color=colors_int[i_15_int], linestyle='--')
                    #     # plt.semilogy(range(len(data_dict[i_10_int]['RMS Res'])),
                    #     #              data_dict[i_10_int]['RMS Res'][-1] * range(len(data_dict[i_10_int]['RMS Res'])))
                    #     # if data_dict[i_10_int]['arit_mean_Conv'] < 1:
                    #     #     plt.semilogy(range(len(data_dict[i_10_int]['Cleaned_Conv_without_Plateau'])), [
                    #     #         data_dict[i_10_int]['RMS Res'][0] * data_dict[i_10_int]['arit_mean_Conv'] ** i_11_int
                    #     #         for i_11_int in range(len(data_dict[i_10_int]['Cleaned_Conv_without_Plateau']))],
                    #     #                               '-.')
                    #     # plt.savefig(f'images/figure_{i_1_int}.pdf', dpi=300)
                    #     plt.savefig(f'images/figure_{i_1_int}_{i_10_int}.png', dpi=300, bbox_inches="tight")
                    #     plt.close()
                except:
                    pass
            new_con_dict.update({i_1_int: data_dict})
        except KeyError as err:
            print('KeyError for', i_1_int, 'missing key: ', err)
        except SyntaxError as err2:
            print('SyntaxError for', i_1_int, 'has: ', err2)

    return new_con_dict


def create_add_and_save_kpis_in_ontology_and_images(dict_int, inventory_onto_int):
    global inventory_int
    inventory_int = inventory_onto_int
    kpis = add_own_kpis_and_save_figs(dict_int)
    for i_int in kpis:
        sim_name = i_int.replace('-', '_').replace(' ', '_').replace(',', '__').replace('.', '__')
        for i_int_2 in kpis[i_int]:
            for i_int_4 in ['Rate', 'RMS Res', 'Max Res', 'Convergence_Rate']:
                try:
                    data_prop_name \
                        = ('hasFinal' + i_int_2 + i_int_4 + 'Value').replace(' ', '').replace('-', '')
                    inventory_int.create_data_prop_with_inventory(data_prop_name, owlready2.DataProperty)
                    # has_data_prop = types.new_class(data_prop_name, (owlready2.DataProperty,))
                    # has_data_prop.python_name = data_prop_name
                    if not ((i_int_4 == 'Convergence_Rate')
                            & (not isinstance(kpis[i_int][i_int_2][i_int_4], list))):
                        try:
                            inventory_int.place_data_with_inventory(sim_name,
                                                                    data_prop_name,
                                                                    float(kpis[i_int][i_int_2][i_int_4][-1]))
                            # exec('emmo_int.%s.%s.append(%s)' % (sim_name,
                            #                                     data_prop_name,
                            #                                     kpis[i_int][i_int_2][i_int_4][-1]))
                        except ontopy.utils.NoSuchLabelError as err3:
                            print(err3, sim_name, '1')

                except KeyError:
                    print(i_int, i_int_4, KeyError)
            for i_int_5 in ['max_Conv', 'arit_mean_Conv', 'geo_mean_Conv']:
                if i_int_5 in kpis[i_int][i_int_2].keys():
                    data_prop_name = ('has' + i_int_2 + i_int_5 + 'Value').replace(' ', '').replace('-', '')
                    inventory_int.create_data_prop_with_inventory(data_prop_name, owlready2.DataProperty)
                    # has_data_prop = types.new_class(data_prop_name, (owlready2.DataProperty,))
                    # has_data_prop.python_name = data_prop_name
                    try:
                        inventory_int.place_data_with_inventory(sim_name,
                                                                data_prop_name,
                                                                float(kpis[i_int][i_int_2][i_int_5]))
                        # exec('emmo_int.%s.%s.append(%s)' % (sim_name, data_prop_name, kpis[i_int][i_int_2][i_int_5]))
                    except ontopy.utils.NoSuchLabelError as err4:
                        print(err4, sim_name, '2')
    return kpis
