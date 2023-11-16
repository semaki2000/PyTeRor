from nicad_parser import NicadParser



def test_parse():
    result = NicadParser(
        xml_file="testfile.xml", 
        orig_filepath="/orig_test",
        tmp_filepath="/mnt/c/Skole/master/master-refactoring/find_codeclone_repos/2015-05-27-SWC-MCRI_temp_filestructure"
        ).parse()
    


test_parse()