import xml.etree.ElementTree as ET
from pathlib import Path

class NicadParser():
    """Parses an XML file outputted by Nicad clone detector. 
    After parsing the result should be a list of clones in this format:
    
    
    list of clone classes (matching clones), each clone class is a dict
    DICT: from path to int, (absolute, not relative) filepath object to a list of linenumbers specifying start of clone
    """

    def __init__(self, xml_file: str | Path, orig_filepath: str | Path = None, tmp_filepath: str | Path = None) -> None:
        self.xml_file = Path(xml_file)
        self.orig_filepath = Path(orig_filepath)
        self.tmp_filepath = Path(tmp_filepath)
    

    def parse(self):
        """Parses the xml file provided in the construction of the object.
        Returns:
         
        list of clone classes (matching clones), 
        each clone class represented by a dict from path to int: 
        (absolute) filepath object to a list of linenumbers specifying start of clone
 """
        path = self.xml_file.resolve()

        assert path.exists(), "File does not exist: " + str(path)
        assert path.is_file(), "Path does not lead to a file: " + str(path)
        assert path.suffix == ".xml", "File not specified as XML file: " + str(path)


        clone_classes_list = []
        #parse XML
        tree = ET.parse(path) 
        root = tree.getroot()
        for clone_class in root.findall("class"):
            class_dict = {}
            for child in clone_class:
                child_path = self.convert_path(Path(child.attrib['file']))     
                
                lineno = child.attrib['startline']
                if not child_path in class_dict:
                    class_dict[child_path] = [lineno]
                else:
                    class_dict[child_path].append(lineno)
            clone_classes_list.append(class_dict)
            
        return clone_classes_list


    def convert_path(self, path):
        """Takes a path in the temporary filepath, and replaces it with a path to the same file in the original directory"""
        if not self.tmp_filepath is None:
            return Path(str(path).replace(str(self.tmp_filepath), str(self.orig_filepath)))
        return path