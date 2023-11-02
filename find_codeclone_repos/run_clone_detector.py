import sys
import os
import shutil
from pathlib import Path

class RunCloneDetector:    

    def run(path):
        orig_path = path

        orig_dir_name = str(path.name)
        
        print(os.getcwd())
        
        path = RunCloneDetector.create_tmp_filestructure(path)
        
        print(str(path))
        
        #run nicad clone detector on tmp filestructure to find clones in test files
        os.system("nicad6 functions py " + str(path) + "/ type2")

        target_xml_path = ""
        clones_xml_file = target_xml_path + "/" + orig_dir_name +"_test_clones.xml"
        os.system("cp " + str(path) + "_functions-blind-clones/" + orig_dir_name + "_temp_filestructure_functions-blind-clones-0.00-classes.xml " + clones_xml_file)
        #RunCloneDetector.remove_tmp_filestructure(path)

        print(clones_xml_file)
        return (clones_xml_file, orig_path, path)

    def remove_tmp_filestructure(path):
        """WIP, currently uses a ./cleanall script found in the nicad install location. Script has to be installed"""
        os.system("./cleanNicad.sh ")
        os.system("rm -r " + str(path))

    def create_tmp_filestructure(path):
        """Copies the directory structure at the given path into the current working directory,
        Also copies over all files which adhere to pytests test discovery rules
        TODO: include specific rules for this repo, set up in pytest.ini, or similar file (.toml, etc.)"""
        
        tmp_dir_path = Path(os.getcwd() + "/"+ str(path.name) + "_temp_filestructure")
        try:
            shutil.copytree(str(path), str(tmp_dir_path), ignore=RunCloneDetector.ignore_non_test_py_files)
        except FileExistsError:
            print("remove tmp directory first")
            sys.exit()
        except shutil.Error: #permissions thing
            pass
        return tmp_dir_path


    #copytree will only copy test files and directories
    def ignore_non_test_py_files(dir, files):
        print(dir)
        print(files)
        pdir = Path(dir)
        ignore_files = []
        for file in files:
            
            filepath = Path(dir + "/" + file)
            if filepath.match("*/test_*.py") or filepath.match("*_test.py") or filepath.is_dir():
                pass
            else:
                
                ignore_files.append(file)
        return ignore_files
