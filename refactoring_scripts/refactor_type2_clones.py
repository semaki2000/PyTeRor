import ast;
from pathlib import Path
from refactoring_utils.RefactorAST import RefactorAST




def main():
    filename = Path("../test_files/calculator/calculator_type2.py")
    target_location = Path("../refactored_files").resolve()
    rfAST = RefactorAST(filename)

    clone_names : list = [["test_addition", "test_addition2"]] #list with lists of matching clones
    
    matched_clone_pairs : list = rfAST.find_clone_nodes_in_AST(clone_names)
    
    #print("Matched clone pairs:", len(matched_clone_pairs))

    ast_refactor_type2_clones(rfAST, matched_clone_pairs)

    rfAST.parse_AST_to_file(target_location / (filename.stem + "_refactored.py"))

    print("done")

def get_clone_names():
    return ["test_addition", "test_addition2"]


def ast_refactor_type2_clones(rfAST, nodes):
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
            diffs += rfAST.find_differences([clone0.body[ind], clone1.body[ind]])
        #create pytest
        values = []
        for node_pair in diffs:
            values.append((node_pair[0].value, node_pair[1].value))    
            
        decorator = rfAST.get_ast_node_for_pytest_decorator(rfAST.name_gen.names, values)
        rfAST.add_parameters_to_func_def(clone0, rfAST.name_gen.names)
        clone0.decorator_list.insert(0, decorator)
        rfAST.detach_redundant_clones([clone1])

main()