# standard imports
import logging
import re

# third-party imports
import yaml

logg = logging.getLogger()


action_values = {
        'read': 4,
        'write': 2,
        }

class YAMLAcl:
    
    def __init__(self, data):
        data = yaml.load(data, Loader=yaml.FullLoader)
        self.matchers = {}
        self.data = {}
        for d in data:
            k = list(d.keys())[0]
            self.matchers[k] = re.compile(k)
            self.data[k] = d[k]

    def check(self, credentials, path, action):
        i = 0
        for k in self.matchers.keys():
            m = self.matchers[k]
            logg.debug('testing {} {} {}'.format(path, k, action))
            if re.match(m, path) and self.data[k].get(action) != None:
                for a in self.data[k][action]:
                    t = credentials.val(a)
                    if not t & action_values[action]:
                        logg.info('access match fail {}'.format(path, action, a))
                        return False
                return True
            i += 1
        return False
