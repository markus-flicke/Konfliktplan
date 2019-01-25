import os
import pandas as pd

class DataReader:
    @classmethod
    def read_all(self):
        return self.read_credentials(), self.read_regelstudienplaene(), self.read_veranstaltungen()

    @classmethod
    def read_credentials(self):
        file = self.find('Credentials')
        with open(file, 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
        return username, password

    @classmethod
    def read_regelstudienplaene(self):
        return pd.read_csv(self.find("Regelstudienplaene"))

    @classmethod
    def read_veranstaltungen(self):
        return pd.read_csv(self.find('Veranstaltungen'))

    @staticmethod
    def find(path):
        rel_path = "../{}/".format(path)
        files = os.listdir(rel_path)

        if len(files) == 0:
            raise Exception("No files found in: {}\nPlease insert files as specified by Readme".format(rel_path))

        if len(files) > 1:
            print(files)
            raise Exception("More than one file found in: {}\nPlease remove files until exactly one file is in location as specified by Readme".format(rel_path))

        return rel_path + files[0]


print(DataReader.read_credentials())