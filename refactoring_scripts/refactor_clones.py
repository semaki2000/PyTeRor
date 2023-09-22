import ast
import sys
from pathlib import Path
from refactoring_utils.ast_parser import ASTParser
from refactoring_utils.clone_ast_utilities import CloneASTUtilities
from refactoring_utils.clone_class_refactorer import CloneClassRefactorer



#currently with function names from test_files/test_check.py

def main():
    if len(sys.argv) == 1:
        print("Usage: python refactor_clones.py filepath [filepaths...]")
        sys.exit()

    filepaths = get_filepaths(sys.argv[1:])
    asts_dict = {} # filepath -> ast_base (for said filepath)
    for filepath in filepaths:
        asts_dict[filepath] = ASTParser.parse_file_to_AST(filepath)
        
    print(asts_dict.keys())

    clones = get_clones()
    clone_classes = []
    #for each clone class
    for clone_class in clones:

        ast_clone_nodes = [] 
        #for filepath in clone class
        for key in clone_class.keys():
            #get ast_base
            ast_base = asts_dict[key]

            for lineno in clone_class[key]:

                #add clone on lineno in filepath to list of clone objects
                ast_clone_nodes.append(CloneASTUtilities.find_clone_node_in_AST(ast_base, clone_lineno=lineno))

        clone_classes.append(CloneClassRefactorer(ast_clone_nodes))

        

    for clone_class in clone_classes:
        clone_class.refactor_clones()

    


    target_location = Path("../refactored_files").resolve()
    for ast_base in asts_dict.values():
        ASTParser.parse_AST_to_file(ast_base, target_location / (Path(sys.argv[1]).stem + "_refactored.py"))



def get_filepaths(args):
    filepaths = []
    for arg in args:
        new_path = Path(arg)
        if new_path.exists() and new_path.is_file():
            filepaths.append(new_path.resolve())  
        else:
            raise FileNotFoundError(new_path)

    return filepaths

def get_clones():
    """Returns clones in this format
    list of clone classes (matching clones), each clone class is a dict
    DICT: from path to int, (absolute, not relative) filepath object to a list of linenumbers specifying start of clone
    """
    #TODO: actually implement. need info from clone detector
    return [{Path("../test_files/calculator/calculator_type2.py").resolve(): [5, 16]}]



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