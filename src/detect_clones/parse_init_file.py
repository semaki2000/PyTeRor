from pathlib import Path


FILENAMES_SECTIONNAMES = {
    'pytest.ini': '[pytest]', 
    '.pytest.ini': '[pytest]', 
    'tox.ini': '[pytest]',
    'setup.cfg': '[tool:pytest]',
    'pyproject.toml': '[tool.pytest.ini_options]'}

def parse_init_file(path, verbose = False):
    """First, we look for pytest.ini file.
    Then we look for .pytest.ini file (hidden).
    Then we look for tox.ini file.
    Then we look for pyproject.toml file with pytest init inside"""
    #slightly incorrect test discovery order.
    #https://docs.pytest.org/en/stable/reference/customize.html#configuration-file-formats
    if verbose:
        print("Looking for a pytest config file...")
    for filename in FILENAMES_SECTIONNAMES.keys():
        filepath = find_config_file(path, filename)
        if filepath:
            print("Found config file:", filepath)
            return parse_file(filename, filepath)
    if verbose:
        print("Could not find pytest config file")
    return {}

def find_config_file(directory, config_file):
    for filepath in Path(directory).rglob(config_file): #shouldnt be more than one, why for-loop? returns straight away anyway
        return filepath
    return False

def parse_file(filename, path):
    section_name = FILENAMES_SECTIONNAMES[filename]
    length = len(section_name)
    in_section = False
    #options
    fileglob_option = 'python_files'
    fileglob = []
        #add more

    config = {'fileglob': fileglob} 
    #all config options would be added into dict
    
    with open(path) as file:
        for line in file:
            if in_section:
                if line[0] == '[':
                    in_section = False
                elif line[:len(fileglob_option)] == fileglob_option:
                    fileglob.extend(line.strip().split()[2:])
                #TODO: add more options here
                    #testpaths
                    #python_classes
                    #python_functions

            if line[:length] == section_name:
                in_section = True
    return config