import sys
import os
import shutil

from pathlib import Path

class RunCloneDetector:    

    def run(path, tmp_dir_path):
        orig_path = path

        orig_dir_name = str(path.name)

        path = RunCloneDetector.create_tmp_filestructure(path, tmp_dir_path)
        
        #run nicad clone detector on tmp filestructure to find clones in test files
        os.system("nicad6 functions py " + str(path) + "/ type2")

        target_xml_path = ""
        #clones_xml_file = target_xml_path + "/" + orig_dir_name +"_test_clones.xml"
        clones_xml_file = "clone_classes.xml"
        os.system("cp " + str(path) + "_functions-blind-clones/tmp_subfolder_functions-blind-clones-0.00-classes.xml " + clones_xml_file)
        

        return (clones_xml_file, orig_path, path)



    def create_tmp_filestructure(path, tmp_dir_path):
        """Copies the directory structure at the given path into the current working directory,
        Also copies over all files which adhere to pytests test discovery rules
        TODO: include specific rules for this repo, set up in pytest.ini, or similar file (.toml, etc.)"""
        
        #problems with these two options: first creates regular directory. Second creates directory in tmp/, but has to be deleted by user
        #tmp_dir_path = Path(os.getcwd() + "/"+ str(path.name) + "_temp_filestructure").mkdtemp
        #tmp_dir_path = tempfile.mkdtemp()
        
        #therefore we use tmp_dir_path supplied from caller on run function. Should be created in context manager ("with ... as ...:")
        tmp_dir_path = tmp_dir_path / Path("tmp_subfolder")
        try:
            shutil.copytree(str(path), str(tmp_dir_path), ignore=RunCloneDetector.ignore_non_test_py_files)
        except FileExistsError:
            print("This error should not occur... remove tmp directory?")
            sys.exit()
        except shutil.Error: #permissions thing
            pass
        return tmp_dir_path


    #copytree will only copy test files and directories
    def ignore_non_test_py_files(dir, files):
        pdir = Path(dir)
        ignore_files = []
        for file in files:
            
            filepath = Path(dir + "/" + file)
            if filepath.match("*/test_*.py") or filepath.match("*_test.py") or filepath.is_dir():
                pass
            else:
                
                ignore_files.append(file)
        return ignore_files
