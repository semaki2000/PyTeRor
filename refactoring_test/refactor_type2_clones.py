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
    
    #print("Matched clone pairs:", len(matched_clone_pairs))

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
        func0_strlist = ast.unparse(clone0).splitlines()[1:]
        func1_strlist = ast.unparse(clone1).splitlines()[1:]


        lines_with_differences = []
        for i in range(len(func0_strlist)):

            func0_str = func0_strlist[i]
            func1_str = func1_strlist[i]


            if func0_str != func1_str:
                words0 = func0_str.split()
                words1 = func1_str.split()
                for j in range(len(words0)):
                
                    if words0[j] != words1[j] and not i in lines_with_differences:
                            lines_with_differences.append(i)

        print("lines with differences:", lines_with_differences)

        for ind in lines_with_differences:
            print(ast.unparse(clone0.body[ind]))
            print(ast.unparse(clone1.body[ind]))
            find_differences(clone0.body[ind], clone1.body[ind])
        
        clone0.decorator_list.insert(0, decorator)


def find_differences(stmt1, stmt2):
    
    #specific solution for calculator example, (and assign statements). More general solution will require implementing nodevisitor?
    #left side of an assign should have special treatment?
    walk_stmt1 = ast.walk(stmt1)
    walk_stmt2 = ast.walk(stmt2)
    while True:
        try:
            w1 = next(walk_stmt1)
            w2 = next(walk_stmt2)

            if type(w1) != type(w2):
                print("Differing types:", type(w1), type(w2))
            elif type(w1) == ast.Constant and w1.value != w2.value:
                print("val w1", w1.value)
                print("val w1", w2.value)
            elif type(w1) == ast.Attribute and w1.attr != w2.attr:
                print(w1.attr)
                print(w2.attr)
        except StopIteration:
            break


main()