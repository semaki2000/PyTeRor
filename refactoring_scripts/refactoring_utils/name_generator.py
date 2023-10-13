

class NameGenerator:
    def __init__(self):
        
        self.names = []
        self.constants_cnt = 0 #parametrized constants
        self.names_cnt = 0 #parametrized names
        self.attrs_cnt = 0
        self.other_cnt = 0 #should be 0


    def new_name(self, context=""):
        name = "parametrized"
        if context == "name":
            name += "_name_" + str(self.names_cnt)
            self.names_cnt += 1
        elif context == "constant":
            name += "_constant_" + str(self.constants_cnt)
            self.constants_cnt += 1
        elif context == "attr":
            name += "_attr_" + str(self.attrs_cnt)
        else:
            name += "_var_" + str(self.other_cnt)
            self.other_cnt += 1
        self.names.append(name)
        return name
    
