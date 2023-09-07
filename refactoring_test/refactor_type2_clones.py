import ast;
from pathlib import Path
from refactoring_utilities import (
    parse_file_to_AST,
    parse_AST_to_file,
    find_clone_nodes_in_AST
)




def main():
    filename = Path("../test_files/calculator_type2.py")
    ast_tree = parse_file_to_AST(filename)

    clone_names : list = [["test_addition", "test_subtraction"]] #list with lists of matching clones
    
    matched_clone_pairs : list = find_clone_nodes_in_AST(ast_tree, clone_names)
    
    print("Matched clone pairs:", len(matched_clone_pairs))

    ast_refactor_type2_clones(matched_clone_pairs)

    # parse_AST_to_file(ast_tree, filename.stem + "_refactored.py")


def get_clone_names():
    return ["test_addition", "test_subtraction"]


def ast_refactor_type2_clones(nodes):
    #type 2 clones -> need to parametrize
    #example solution: unparse to string and find differences (too simple??)
    for clone_pair in nodes:
        clone0 = clone_pair[0]
        clone1 = clone_pair[1]

        #unparse clones to str and split by line
        function0_str = ast.unparse(clone0).split("\n")
        function1_str = ast.unparse(clone1).split("\n")


        for i in range(len(function0_str)):
        
            if function0_str[i] != function1_str[i]:
                print(function0_str[i])
                print(function1_str[i])


        #if reparsing the unparsed strings: function defs need "\n\t pass" after them 


"""     # DOES NOT WORK!     
        clone0_walk = ast.walk(clone0)
        clone1_walk = ast.walk(clone1)


        for node in clone0_walk:
            node1 = next(clone1_walk)
            
            print(node, " ", node1)
            if (node == node1):
                print("equal!")
 """

        #ast.Call object must be wrapped in ast.Expr, 
        #otherwise it will be added onto the same line as last node.
        # call_to_clone0 = ast.Expr(value=ast.Call(ast.Name(clone0.name), clone1.args.args, []))

        
        #clone1.body = []
        #clone1.body.append(call_to_clone0)

main()