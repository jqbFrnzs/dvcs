import os, time
from os import listdir
from os.path import isfile, join

VERSION_DIR = '.gites/files/'
WORKING_DIR = 'stage/'

def create_txt_file():
    filename = input("Enter a file name to create:\n")

    with open(WORKING_DIR+filename, 'w') as f:
        while True:
            user_input = input("Enter a line of text or 'q' to quit: ")
            if user_input == 'q':
                break
            f.write(user_input + '\n')


def create_stage_area():
    if os.path.isdir('stage'):
        print('Staging area (Working directory) already created!')
    else:
        os.mkdir("stage")
        print('Created working directory (stage)')

def create_vcs_area():
    if os.path.isdir('.gites'):
        print('Version control system already initialized and running!')
    else:
        os.mkdir(".gites")
        os.mkdir(".gites/files")
        print('Version control system has been initialized! (.gites)')

# initialize version control system
def vcs_init():
    create_stage_area()
    create_vcs_area()

def is_vcs_initialized():
    if os.path.isdir('.gites') and os.path.isdir('stage'):
        return True
    else:
        print('Version control system not initialized, first use init command')
        return False

def create_stage_area():
    if os.path.isdir('stage'):
        print('Staging area (Working directory) already created!')
    else:
        os.mkdir("stage")

def get_file_modification_date(file):
    tm = os.path.getmtime(file)
    return time.strftime('%m/%d/%Y, %H:%M:%S', time.gmtime(tm))

def print_all_versioned_files_dir():
    path = VERSION_DIR
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        print('Filename: ' + file + '  - last time modified: ' + get_file_modification_date(path+file))
    print('')
  
def print_all_staged_files_dir():
    path = WORKING_DIR
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        print('Filename: ' + file + '  - last time modified: ' + get_file_modification_date(path+file))
    print('')

def save_file_with_next_version(next_version_filename):
    base_path = VERSION_DIR
    filename_to_version = WORKING_DIR + next_version_filename.split('_')[0]
    versioned_file = base_path + next_version_filename
    with open(filename_to_version,'r') as firstfile, open(versioned_file,'w') as secondfile:
        for line in firstfile:
            secondfile.write(line)

def get_list_of_file_versions():
    directory = VERSION_DIR
    list_of_filenames = []
    for filename in os.scandir(directory):
        if filename.is_file():
            filename_with_version = os.path.basename(filename).split('/')[-1]
            list_of_filenames.append(filename_with_version)
    return list_of_filenames	
            

def generate_filename_with_next_version(list_of_file_versions, base_file_name):

    next_version_num = 1
    # base_path = WORKING_DIR + base_file_name
    list_of_searched_filenames = []
    list_of_searched_version_nums = []
    for filename in list_of_file_versions:
        if base_file_name in filename:
            list_of_searched_filenames.append(filename)
    if len(list_of_searched_filenames) == 0:
        filename_with_next_version = base_file_name + '_' + str(next_version_num)
        return filename_with_next_version
    else:
        for version in list_of_searched_filenames:
            list_of_searched_version_nums.append(int(version.split('_')[-1]))
        next_version_num = max(list_of_searched_version_nums) + 1
        filename_with_next_version = base_file_name + '_' + str(next_version_num)
        return filename_with_next_version

def get_working_dir_file_list():
    # print(WORKING_DIR)
    file_list = []
    path = WORKING_DIR
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        file_list.append(file)
    if len(file_list) == 0:
        return 'Working dir is empty!'
    return file_list

def get_vcs_dir_file_list():
    # print(WORKING_DIR)
    file_list = []
    path = VERSION_DIR
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:
        file_list.append(file)
    return file_list

def save_all_files_with_next_version(list_of_files):
    if len(list_of_files) == 0:
        print('No files to add/update - dir is empty!')
    else:
        list_of_files_versions = get_list_of_file_versions()
        # print(list_of_files_versions)
        for filename in list_of_files:
            filename_of_next_version = generate_filename_with_next_version(list_of_files_versions,filename)
            print('\n+Added ' + filename + ' as "' + filename_of_next_version + '"')
            save_file_with_next_version(filename_of_next_version)
        print('\nAll files from stage added to vcs')
        
    
def save_specified_files_with_next_version():
    print('\nSelect which files you want to add/update to vcs')
    working_dir_list = get_working_dir_file_list()
    files_to_version = []
    while True:
        print('\nFiles in working dir: \n')
        print_all_staged_files_dir()
        print('Type in . to add all files')
        filename = input('Or enter filename from above followed by enter, type in QUIT to exit:\n')
        if filename == 'QUIT':
            break
        elif filename == '.':
            # print(working_dir_list)
            save_all_files_with_next_version(working_dir_list)
            break
        elif filename not in working_dir_list:
            print('Specified file that is not in working directory!')
            print('Specify one/more of the files from below: ')
            print(working_dir_list)
            continue
        else:
            list_of_file_versions = get_list_of_file_versions()
            filename_of_next_version = generate_filename_with_next_version(list_of_file_versions, filename)
            save_file_with_next_version(filename_of_next_version)
            print('\n+Added ' + filename + ' as "' + filename_of_next_version + '"\n')

    

def diff_two_files_content():
    pass

    
# list_of_file_versions = get_list_of_file_versions()
# # filename_of_next_version = generate_filename_with_next_version(list_of_file_versions, 'ss')
# working_file_list = get_working_dir_file_list()
# save_all_files_with_next_version(working_file_list)
# # save_file_with_next_version(filename_of_next_version)
# print_all_versioned_files_dir()
# print(get_working_dir_file_list())



# 	>>> import os
# >>> os.path.basename('/home/abc/xyz/12345_993456_pqr')
# '12345_993456_pqr'

# >>> os.path.basename('/home/abc/xyz/12345_993456_pqr').split('_')
# ['12345', '993456', 'pqr']

# >>> os.path.basename('/home/abc/xyz/12345_993456_pqr').split('_')[1]
# '993456'

# >>> os.path.basename('/home/abc/xyz/12345_993456_pqr').split('_')[1][:2]
# '99'