

class NameGenerator:
    names = []
    constants_cnt = 0 #parametrized constants
    names_cnt = 0 #parametrized names
    other_cnt = 0 #should be 0
    def __init__(self, basename: str):
        self.basename = basename #not used any more, remove (in CCR class)

    def new_name(self, context=""):
        name = "parametrized"
        if context == "name":
            name += "_name_" + str(self.names_cnt)
            self.names_cnt += 1
        elif context == "constant":
            name += "_constant_" + str(self.constant_cnt)
            self.constant_cnt += 1
        else:
            name += "var" + str(self.other_cnt)
            self.other_cnt += 1
        self.names.append(name)
        return name
    
