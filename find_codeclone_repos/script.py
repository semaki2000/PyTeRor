import sys
import os
import shutil
from pathlib import Path
#remove files which aren't test_*py or *_test.py (TODO: also check potential pytest.ini file(or hidden .pytest.ini))
# run nicad on remaining files to see if code clones in tests of repo


def main():
    path = getPathObj()
    tmp_dir_path = Path(str(path) + "_temp_filestructure")
    try:
        shutil.copytree(str(path), str(path) + "_temp_filestructure")
    except FileExistsError:
        print("remove tmp directory first")
        sys.exit()
    except shutil.Error:
        pass
    path = tmp_dir_path
    print(path)
    test_files = [x for x in path.rglob("test_*.py")]
    test_files += [x for x in path.rglob("*_test.py")]
    gen = path.rglob("*")
    while True:
        try:
            next_file = next(gen)
            if not next_file in test_files:
                print("removing file:", next_file)
                next_file.unlink()
        except StopIteration:
            break

    #run nicad clone detector to find clones
    print(str(path))
    os.system("nicad6 functions py " + str(path) + "/ type2")

#    os.system("cat " + str(path) + "/" + str(path) )



def getPathObj():
    if len(sys.argv) != 2:
        print("Usage: python script.py path_to_repository")
        sys.exit()
    stringPath = sys.argv[1]
    pathObj = Path(stringPath)
    if not pathObj.exists():
        print("Given path does not exist: \n" + stringPath)
        sys.exit()
    elif not pathObj.is_dir():
        print("Given path does not point to a directory: \n" + stringPath)
        sys.exit()
    return pathObj








main()