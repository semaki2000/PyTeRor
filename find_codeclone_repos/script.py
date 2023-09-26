import sys
from pathlib import Path
#remove files which aren't test_*py or *_test.py (TODO: also check potential pytest.ini file(or hidden .pytest.ini))
# run nicad on remaining files to see if code clones in tests of repo


def main():
    path = getPathObj()

    test_files = [x for x in path.rglob("test_*.py")]
    test_files += [x for x in path.rglob("*_test.py")]
    gen = path.rglob("*")
    while True:
        try:
            next_file = next(gen)
            if next_file in test_files:
                print("keeping ", next_file)
            else:
                resp = "yes" # input()
                if (resp == "yes"):
                #next_file.unlink()
                    print("unlinking", next_file)
        except StopIteration:
            break




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