from APIs.ExternalAPIs.MiunDrive.MiunDriveAPI import get_list_of_all_data_files, update_file, open_file, get_file_object, FileTree

ID_names = ['id','ID','תעודת זהות','מספר זהות']

def fetch_fields_dict(root: FileTree, json_dict: dict, candidate_id: int) -> dict:
    all_field_to_fetch = [item for sublist in json_dict.values() for item in sublist] #flatten the list of lists
    all_field_to_fetch.sort()
    field_dict = {}
    last_loaded_file = ''
    file_df = None
    for field in all_field_to_fetch:
        index = field.find(':')
        current_file = field[:index]
        if(current_file != last_loaded_file):
            file_obj = get_file_object(root, current_file)
            update_file(file_obj)
            file_df = open_file(file_obj)
            #print(file_df)
        for id_name in ID_names:
            if id_name in file_df:
                print(file_df[id_name])
                ind = file_df[id_name]==candidate_id
                print(ind)
                print(list(file_df[field[index + 1:]][ind]),'GG\n')
                field_dict[field] = list(file_df[field[index + 1:]][ind])[0]
        last_loaded_file = current_file
    return field_dict


    

