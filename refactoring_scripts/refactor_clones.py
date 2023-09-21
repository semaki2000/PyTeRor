import ast
import sys
from pathlib import Path
from refactoring_utils.RefactorAST import RefactorAST
from refactoring_utils.MultiFileRefactorAST import MultiFileRefactorAST


#currently with function names from test_files/test_check.py

def main():
    if len(sys.argv) == 1:
        print("Usage: python refactor_clones.py filepath [filepaths...]")
        sys.exit()

    filepaths = get_filepaths(sys.argv[1:])
    if len(filepaths) == 1:
        rfAST = RefactorAST(filepaths[0])
    else:
        rfAST = MultiFileRefactorAST(filepaths)    

    target_location = Path("../refactored_files").resolve()


    clone_names : list = get_clone_names() #list with lists of matching clones
    
    matched_clone_pairs : list = rfAST.find_clone_nodes_in_AST(clone_names)
    
    #print("Matched clone pairs:", len(matched_clone_pairs))

    ast_refactor_type2_clones(rfAST, matched_clone_pairs)

    rfAST.parse_AST_to_file(target_location / (Path(sys.argv[1]).stem + "_refactored.py"))



def get_filepaths(args):
    filepaths = []
    for arg in args:
        new_path = Path(arg)
        if new_path.exists() and new_path.is_file():
            filepaths.append(new_path.resolve())  
        else:
            raise FileNotFoundError(new_path)

    return filepaths

def get_clone_names():
    #TODO: actually implement. need info from clone detector
    return [["test_addition", "test_addition2"]]
    test_check = """return [
        ["test_check_with_commented_values", 
         "test_check_with_commented_lines",
         "test_check_without_enddate",
         "test_check_with_enddate"],

        ["test_check_with_blank_lines",
         "test_check_with_leading_blank_lines",
         "test_check_with_missing_yaml_terminator"]
         ]"""
    """return [
        ["test_roman_numeral_4", "test_roman_numeral_10", "test_roman_numeral_54", "test_roman_numeral_111", "test_roman_numeral_bad_input"]
    ]"""



def ast_refactor_type2_clones(rfAST, nodes):
    #type 2 clones -> need to parametrize
    #example solution: unparse to string and find differences (too simple??)

    for clones_list in nodes:


        #unparse clones to str and split by line
        unparsed_clones = [] # str list
        for clone in clones_list:
            unparsed_clones.append(ast.unparse(clone).splitlines()[1:])
    


        lines_with_differences = []
        #for-loop builds up lines_with_differences by comparing contents between clones for each line, adding line-indexes that are different
        for i in range(len(unparsed_clones[0])):

            #current line for all clones
            cur_line_str = []
            for clone in unparsed_clones:
                cur_line_str.append(clone[i])

            if any(clone_str != cur_line_str[0] for clone_str in cur_line_str):
                lines_with_differences.append(i)

        differing_nodes_list = [] #list of lists of differing nodes, each inner list as long as amount of matched clones
        for ind in lines_with_differences:
            
            differing_nodes_list += rfAST.extract_differences([clone.body[ind] for clone in clones_list])
        
        #create pytest decorator
        values = []
        for ind in range(len(differing_nodes_list[0])):
            values.append(tuple([l[ind].value for l in differing_nodes_list]))
            

        decorator = rfAST.get_ast_node_for_pytest_decorator(rfAST.name_gen.names, values)

        rfAST.add_parameters_to_func_def(clones_list[0], rfAST.name_gen.names)
        clones_list[0].decorator_list.insert(0, decorator)
        rfAST.detach_redundant_clones(clones_list[1:])

main()