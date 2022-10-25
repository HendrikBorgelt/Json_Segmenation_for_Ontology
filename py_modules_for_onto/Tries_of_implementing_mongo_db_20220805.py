
# import pymongo
# from pymongo import MongoClient


# def transfer_data_to_mongo(data_int, mongo_db, mongo_collection, mongo_cluster):
#     cluster_int = MongoClient(mongo_cluster)
#     db_int = cluster_int[mongo_db]
#     mongo_collection_int = db_int[mongo_collection]
#     post = data_int
#     mongo_collection_int.insert_one(post)
#
#
# def transfer_instances_to_mongo_db(path, mongo_db, mongo_collection, mongo_cluster):
#     for root, dirs, files in os.walk(path):
#         for name_2 in files:
#             if name_2.endswith(".json"):
#                 with open(root + str('/') + name_2, 'r') as in_file:
#                     json_loaded = json.load(in_file)
#                     instance_name = name_2
#                     file_path = list(root.split('/'))[-1].split('\\')
#                     instance_key = file_path[0]
#                     instance_group = file_path[1]
#                     print('root: ', root)
#                     print('instance_key: ', instance_key)
#                     print('instance_group: ', instance_group)
#                     print('instance_name: ', instance_name)
#                     transfer_data_to_mongo(
#                         {'instance_name': instance_name, 'instance_key': instance_key, 'instance_group': instance_group,
#                          'dict': json_loaded}, mongo_db, mongo_collection, mongo_cluster)
#
#
# def transfer_simulation_dicts_to_mongo_db(path, mongo_db, mongo_collection, mongo_cluster):
#     for root, dirs, files in os.walk(path):
#         for name_2 in files:
#             if name_2.endswith(".json"):
#                 with open(root + str('/') + name_2, 'r') as in_file:
#                     json_loaded = json.load(in_file)
#                     instance_name = name_2
#                     transfer_data_to_mongo(
#                         {'simulation': instance_name,
#                          'dict': json_loaded}, mongo_db, mongo_collection, mongo_cluster)



# mongodb+srv://HendrikB:tAyJ0AtmHUiqaYNf@cluster0.4a1ca.mongodb.net/test
# cluster = MongoClient('mongodb+srv://HendrikB:tAyJ0AtmHUiqaYNf@cluster0.4a1ca.mongodb.net'
#                       '/myFirstDatabase?retryWrites=true&w=majority')
# db = cluster['MasterthesisDB']
# mongo_collection = db['JSONdicts']




# path = 'C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis/folder_for_dict_instances/'
# for name_2 in os.listdir('C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis'):
# modified_all_sims = all_sims
#     if name_2.endswith('.json'):
# dict_to_be_transfered_to_mongo =
# mongo_cluster = 'mongodb+srv://HendrikB:tAyJ0AtmHUiqaYNf@cluster0.4a1ca.mongodb.net/' \
#                 'myFirstDatabase?retryWrites=true&w=majority'
# mongo_db = 'MasterthesisDB'
# # mongo_collection = 'instance_JSON_dicts'
# mongo_collection_1 = 'unmodified_JSON_dicts'
# mongo_collection_2 = 'unmodified_JSON_dicts'
# Path_1 = 'C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis/folder_for_dict_instances/Named_instances/'
# Path_2 = 'C:/Users/hendr/Documents/GitHub/Hendrik_Borgelt_Masterthesis/Json_Dict_unmodified/'
# transfer_simulation_dicts_to_mongo_db(Path_2, mongo_db, mongo_collection_2, mongo_cluster)


# for root, dirs, files in os.walk(path):
#     for name_2 in files:
#         if name_2.endswith(".json"):
#             with open(root + str('/') + name_2, 'r') as in_file:
#                 # file_name = os.path.normpath(root.split(path)[1] + name_2.split('.out')[0])
#                 # file_name = file_name[1:].replace('\\', '_')
#                 # file_list_1.append([root, name_2, file_name])
#                 test_567 = json.load(in_file)
#                 instance_name = name_2
#                 test_678 = list(root.split('/'))[-1].split('\\')
#                 instance_key = test_678[0]
#                 instance_group = test_678[1]
#                 print('root: ', root)
#                 print('instance_key: ', instance_key)
#                 print('instance_group: ', instance_group)
#                 print('instance_name: ', instance_name)
#                 transfer_data_to_mongo({'instance_name': instance_name,
#                                         'instance_key': instance_key,
#                                         'instance_group': instance_group,
#                                         'dict': test_567},
#                                        mongo_db,
#                                        mongo_collection,
#                                        mongo_cluster)

# for i_int in test_567['Sims']:
#     print(test_567['Tuple'])
#     modified_all_sims_2 = modified_all_sims[i_int]
#     for i_2_int in test_567['Tuple'][:-1]:
#         modified_all_sims_2 = modified_all_sims_2[i_2_int]
#     print(modified_all_sims_2)
# print(test_567['Tuple'])
# with open(name_2) as outfile:
#     f_4.update({name_2.rstrip('.json'): json.load(outfile)})


# cluster = MongoClient('mongodb+srv://HendrikB:tAyJ0AtmHUiqaYNf@cluster0.4a1ca.mongodb.net/'
#                       'myFirstDatabase?retryWrites=true&w=majority')
# db = cluster['MasterthesisDB']
# mongo_db_collection = db['JSONdicts']
# mongo_db_collection.delete_many({})
# mongo_cluster = 'mongodb+srv://HendrikB:tAyJ0AtmHUiqaYNf@cluster0.4a1ca.mongodb.net/' \
#                 'myFirstDatabase?retryWrites=true&w=majority'
# mongo_db = 'MasterthesisDB'
# mongo_collection = 'JSON_dicts'

# transfer_data_to_mongo({'_id': 0, 'dict': 'test'}, mongo_db, mongo_collection, mongo_cluster)
#
# for number, json_dict in enumerate(all_sims):
#     transfer_data_to_mongo({'_id': number,
#                             'dict': {json_dict: all_sims[json_dict]}},
#                            mongo_db,
#                            mongo_collection,
#                            mongo_cluster)
