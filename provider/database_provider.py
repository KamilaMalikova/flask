from configparser import ConfigParser


class DatabaseProvider:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def get_database_configuration(self, filename='database.ini', section='postgres'):
        # create a parser
        parser = ConfigParser()
        # read config file
        filename = filename = self.root_dir + '/static/' + filename
        parser.read(filename)
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return db
