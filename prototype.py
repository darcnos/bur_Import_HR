import os
import re


def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Define our workspace
path = 'C:\\Burris_rename\\resources\\'
filepath = 'C:\\Burris_rename\\WebDocs\\'

# Read resources into memory, parse into a list
tem = open(path + 'dividerstomatch.txt', 'r')
dividerstomatch = tem.read().splitlines()
dividerstomatch = [x.lower() for x in dividerstomatch]

# Same as above
tem = open(path + 'dividerstoreplace.txt', 'r')
dividerstoreplace = tem.read().splitlines()
dividerstoreplace = [x.lower() for x in dividerstoreplace]

# Same as above
tem = open(path + 'separatorstomatch.txt', 'r')
separatorstomatch = tem.read().splitlines()
separatorstomatch = [x.lower() for x in separatorstomatch]

# Same as above
tem = open(path + 'separatorstoreplace.txt', 'r')
separatorstoreplace = tem.read().splitlines()
separatorstoreplace = [x.lower() for x in separatorstoreplace]

# Zip our lists together into a associated dict
divider_lookup_dict = dict(zip(dividerstomatch, dividerstoreplace))
separator_lookup_dict = dict(zip(separatorstomatch, separatorstoreplace))

# Run the above function and store its results in a variable.
full_file_path = get_filepaths(filepath)
i = 0


def is_w4(i):
    # Yields true/false depending on if file is W4
    foo = full_file_path[i]
    level = foo.rsplit('\\')
    bar = str(level[4]).lower()
    #if 'w4' or 'w-4' or 'w-4s' or "w4's" in str(level[4].lower()):
    if bar.find("w4") and bar.find("w-4") and bar.find("w-4s") and bar.find("w4's") and bar.find("w-4's") == -1:
        return False
    else:
        return True


def is_i9(i):
    # Yields true/false depending on if file is W4
    foo = full_file_path[i]
    level = foo.rsplit('\\')
    bar = str(level[4]).lower()
    if bar.find("i9") and bar.find("i9's") and bar.find("i9s") and bar.find("i-9") and bar.find("i-9s") and bar.find("i-9's") == -1:
        return False
    else:
        return True


def get_emp_num(i):
    # Returns the employee number if it can be found, or 999999 if there is no employee number
    word = str(full_file_path[i])
    empl_num_patter = re.compile('\d{6,14} -')
    if empl_num_patter.search(word) is not None:
        employee_info = re.findall(empl_num_patter, word)
        return = re.findall('\d{6,14}', str(employee_info))
    else:
        return '999999'


def get_filename_and_extension(i):
    # Returns the filename with its extension
    head, tail = os.path.split(full_file_path[i])
    return tail


def get_filename(i):
    # Returns the  filename without its extension
    foo = os.path.splitext(full_file_path[i])[0]
    head, tail = os.path.split(foo)
    return tail


def is_emp_dir(div_map_input):
    # Returns True/False depending on if the folder in question is the employee folder
    emp_num = str(get_emp_num(i))
    if bool(re.search('\d{6,14}', div_map_input)) == True or emp_num == '999999':
        return True
    else:
        return False


def get_div_map_input(i):
    # Returns what the divider mapping input for a given file should be
    emp_num = str(get_emp_num(i))
    div_map_path = "\\".join(full_file_path[i].split('\\')[:-1]).lower()
    foo = div_map_path.rsplit('\\')
    foo.reverse()
    itercount = 0
    for itercount in range(10):
        div_map_input = foo[itercount]
        if is_emp_dir(div_map_input) == True or bool(re.search('999999', emp_num)) == True:
            return 'historical data'
        else:
            if divider_lookup_dict.has_key(str(foo[int(itercount)])) == True:
                div_map_input = str(foo[int(itercount)])
                return div_map_input
            else:
                itercount = itercount + 1


def get_div_mapping(i):
    # Returns the divider mapping based on the divider input
    if is_i9(i) == True:
        return "I-9".lower()
    elif is_w4(i) == True:
        return "W-4-Federal".lower()
    elif is_emp_dir == True:
        return 'historical data'
    else:
        div_map_input = get_div_map_input(i)
        return divider_lookup_dict[str(div_map_input.lower())].lower()


def get_sep_mapping(i):
    # Returns the separator mapping based on the divider mapping
    div_mapping = str(get_div_mapping(i)).lower()
    return str(separator_lookup_dict[str(div_mapping)]).lower()

