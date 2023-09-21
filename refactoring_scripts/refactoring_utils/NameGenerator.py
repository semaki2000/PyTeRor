

class NameGenerator:
    names = []
    cnt = 0
    def __init__(self, basename: str):
        self.basename = basename

    def new_name(self):
        name = self.basename + "_" + str(self.cnt)
        self.cnt += 1
        self.names.append(name)
        return name