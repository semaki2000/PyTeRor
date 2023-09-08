import ast;
from pathlib import Path
from refactoring_utilities import (
    parse_file_to_AST,
    parse_AST_to_file,
    find_clone_nodes_in_AST,
    get_ast_node_for_pytest_decorator,
    add_parameters_to_func_def,
    NameGenerator
)




def main():
    filename = Path("../test_files/calculator_type2.py")
    ast_tree = parse_file_to_AST(filename)

    clone_names : list = [["test_addition", "test_addition2"]] #list with lists of matching clones
    
    matched_clone_pairs : list = find_clone_nodes_in_AST(ast_tree, clone_names)
    
    #print("Matched clone pairs:", len(matched_clone_pairs))

    ast_refactor_type2_clones(matched_clone_pairs)

    parse_AST_to_file(ast_tree, filename.stem + "_refactored.py")


def get_clone_names():
    return ["test_addition", "test_addition2"]


def ast_refactor_type2_clones(nodes):
    #type 2 clones -> need to parametrize
    #example solution: unparse to string and find differences (too simple??)

    for clone_pair in nodes:
        clone0 = clone_pair[0]
        clone1 = clone_pair[1]
        

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

        diffs = []
        for ind in lines_with_differences:
            #print(ast.unparse(clone0.body[ind]))
            #print(ast.unparse(clone1.body[ind]))
            diffs += (find_differences_recursive(clone0.body[ind], clone1.body[ind]))
        #create pytest
        values = []
        for node_pair in diffs:
            values.append((node_pair[0].value, node_pair[1].value))    
            
        decorator = get_ast_node_for_pytest_decorator(name_gen.names, values)
        add_parameters_to_func_def(clone0, name_gen.names)
        clone0.decorator_list.insert(0, decorator)


def find_differences_recursive(stmt1, stmt2): #only looks at different constants (enough?)
    different_nodes = []
    iter_stmt1 = ast.iter_child_nodes(stmt1)
    iter_stmt2 = ast.iter_child_nodes(stmt2)
    while True:
        try:
            child1 = next(iter_stmt1)
            child2 = next(iter_stmt2)

            if type(child1) != type(child2):
                print("Differing types:", type(child1), type(child2))
            elif type(child1) == ast.Constant and child1.value != child2.value:
                
                different_nodes.append([child1, child2])

                #remove constant from the AST, replace with variable
                if type(stmt1) == ast.Assign:
                    stmt1.value = ast.Name(id=name_gen.new_name())
                elif type(stmt1) == ast.Tuple:
                    ind = stmt1.elts.index(child1)
                    stmt1.elts.pop(ind)
                    stmt1.elts.insert(ind, ast.Name(id=name_gen.new_name()))

            elif type(child1) == ast.Name and child1.id != child2.id:
                pass #do nothing, problem will be fixed by refactoring into one of the functions, 
                     #and deleting the other, thereby "choosing" one of the names
            different_nodes += find_differences_recursive(child1, child2)
        except StopIteration:
            break
    return different_nodes

name_gen = NameGenerator("new_var")
main()