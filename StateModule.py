from dotteddict import dotteddict

class State(object):
    def __init__(self):
        self.Uf = 0
        self.Ug = 0
        self.Ua = 0
        self.Ue = 0
        self.Ie = 0
        self.helper = {
            'plot': False,
            'UI': {}
        }

    def set_param(self, key):
        def set_value(value):
            if key == 'Uf':
                self.Uf = value
            if key == 'Ug':
                self.Ug = value
            if key == 'Ua':
                self.Ua = value
            if key == 'Ue':
                self.Ue = value
            if key == 'Ie':
                self.Ie = value
        return set_value