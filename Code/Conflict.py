class Conflict:
    def __init__(self, data, degree, variant, semester):
        self.data = data
        self.degree = degree
        self.variant = variant
        self.semester = semester

    def __repr__(self):
        res = """\n{},{},{}
        {}
        """.format(self.degree, self.variant, self.semester, self.data)
        return res