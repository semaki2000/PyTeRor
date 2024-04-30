import ast

class KwCallNodeSet():
    """Set of nodes containing function calls with keyword parameters."""
    def __init__(self, nodes, target_index):
        self.nodes = nodes
        self.target_index = target_index
        self.same_kws_called = False

    def same_keywords(self):
        """Checks the consistency of kw list between nodes.
        If the same keywords appear (even if wrong order), returns True.
        Else, returns False.
        """
        self.same_kws_called = True
        #initialize sets
        node_sets = [set() for node in self.nodes]

        #add all keywords to all sets
        for node_ind in range(len(self.nodes)):
            node = self.nodes[node_ind]
            for keyword in node.keywords:
                node_sets[node_ind].add(keyword.arg)

        #compare to make sure all sets are equal
        equal = True
        for ind in range(1, len(node_sets)):
            if node_sets[ind] != node_sets[ind - 1]:
                equal = False
        
        if not equal:
            self.set_split_indices(node_sets)
            return False

        self.keywords = list(node_sets[0])
        return True
        
    def sort_keywords(self):
        """Sorts the keywords of every node in the class.
        After this function is employed, the nodes will have keywords in the same order.
        Depends on the same_keywords function to have been called first."""
        assert self.same_kws_called
        #sort our keywords
        self.keywords.sort()

        for node in self.nodes:
            new_kw_list = []
            for sorted_keyword_id in self.keywords:
                for keyword in node.keywords:
                    if keyword.arg == sorted_keyword_id:
                        new_kw_list.append(keyword)
            node.keywords = new_kw_list

    def set_split_indices(self, node_kw_sets):
        """Given a list of sets containing keywords for each node,
        groups nodes into split groups. Nodes with the same keywords go in the same group."""
        self.split_groups = {}
        for ind in range(len(node_kw_sets)):
            self.split_groups.setdefault(str(node_kw_sets[ind]), []).append(ind)
        
