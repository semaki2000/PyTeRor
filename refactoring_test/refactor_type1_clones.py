import ast;
import astor;




def main():
    ast_tree = parse_file_to_AST("../test_files/calculator_test_type1clone.py")

    clone_names : list = [("test_addition", "test_addition2")] #list with lists of matching clones
    flattened_clone_names = [item for subtuple in clone_names for item in subtuple]
    
    clone_nodes : list = find_clone_nodes_in_AST(ast_tree, flattened_clone_names)
    matched_clone_pairs : list = sort_clones_into_matched_clone_pairs(clone_nodes, clone_names)
    
    print("Test:", len(matched_clone_pairs))

    ast_rewrite_extract_method()


def parse_file_to_AST(filename):
    return astor.parse_file("../test_files/calculator_test_type1clone.py")


def get_clone_names():
    return ["test_addition", "test_addition2"]

def find_clone_nodes_in_AST(ast_tree, clone_names):

    clone_nodes = []

    #only for one file
    for i in range(len(ast_tree.body)):
        node = ast_tree.body[i]
        if isinstance(node, ast.FunctionDef) and node.name in clone_names:
            clone_nodes.append(node)

    return clone_nodes

def sort_clones_into_matched_clone_pairs(nodes, names):

    #TODO: inefficient
    all_matched_nodes = []
    for sublist in names:

        current_matched = []
        all_matched_nodes.append(current_matched)

        for node in nodes:
            if node.name in sublist:
                current_matched.append(node)
    return all_matched_nodes


def ast_refactor_type1_clones(nodes):

    

    pass


main()