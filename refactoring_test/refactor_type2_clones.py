import ast;
from pathlib import Path
from refactoring_utilities import (
    parse_file_to_AST,
    parse_AST_to_file,
    find_clone_nodes_in_AST,
    get_ast_node_for_pytest_decorator
)




def main():
    filename = Path("../test_files/calculator_type2.py")
    ast_tree = parse_file_to_AST(filename)

    clone_names : list = [["test_addition", "test_subtraction"]] #list with lists of matching clones
    
    matched_clone_pairs : list = find_clone_nodes_in_AST(ast_tree, clone_names)
    
    print("Matched clone pairs:", len(matched_clone_pairs))

    ast_refactor_type2_clones(matched_clone_pairs)

    parse_AST_to_file(ast_tree, filename.stem + "_refactored.py")


def get_clone_names():
    return ["test_addition", "test_subtraction"]


def ast_refactor_type2_clones(nodes):
    #type 2 clones -> need to parametrize
    #example solution: unparse to string and find differences (too simple??)
    for clone_pair in nodes:
        clone0 = clone_pair[0]
        clone1 = clone_pair[1]

        decorator = get_ast_node_for_pytest_decorator(["var1", "var2"], [(1, 2), (2, 3), (3, 4)])

        #unparse clones to str and split by line
        func0_iter = iter(ast.unparse(clone0).splitlines())
        func1_iter = iter(ast.unparse(clone1).splitlines())

        next(func0_iter)
        next(func1_iter)    


        while True:
            try:
                func0_str = next(func0_iter)
                func1_str = next(func1_iter)
            except StopIteration:
                break;

            if func0_str != func1_str:
                #print(func0_str)
                #print(func1_str)
                words0 = func0_str.split()
                words1 = func1_str.split()
                for j in range(len(words0)):
                
                    #add space after delimiters "(", ")", "," etc.
                    #except if inside a string
                    if words0[j] != words1[j]:
                        pass
                        #print("Difference: " + words0[j] + " != " + words1[j])

        clone0.decorator_list.insert(0, decorator)
        #if reparsing the unparsed strings: function defs, if, while, for need "\n\t pass" after them 

        
main()