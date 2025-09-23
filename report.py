
from collections import defaultdict
import pandas as pd


import json

dictionary = [
    {
        'School': 'ACS BR',
        'Class': "1A2",
        'Students.Name': 'Peter',
        'Students.SurName': 'Wirija',
        'Students.Subject.Name': 'English',
        'Students.Subject.Sememester': 1,
        'Students.Subject.Grade': 'A',
        'Students.Parent.Surname': 'Wirija',
        'Students.Parent.Name': 'William',
        
    },
    {
        'School': 'ACS BR',
        'Class': "1A2",
        'Students.Name': 'Peter',
        'Students.SurName': 'Wirija',
        'Students.Subject.Name': 'English',
        'Students.Subject.Sememester': 1,
        'Students.Subject.Grade': 'A',
        'Students.Parent.Surname': 'Wirija',
        'Students.Parent.Name': 'Megawati',
        
    }

]

"""
    {
        'School': 'ACS BR',
        'Class': "1A2",
        "Students": [
            {
                "Name": "Peter",
                "SurName": "Wirija",
                "Subject": [
                    { 
                        "Name": "English",
                        "Semester": 1,
                        "Grade: "A"
                    }
                ]
            }  
        ]W
    }

"""

class reportDict:

    def init(self, data=[]):

        if len(data) == 0: 
            return 
        
        self.data = []
        self.hierachy = pd.DataFrame()
        self.set_hierachy(data)
        self.max_level = max(self.hierachy['level'])

        for item in data:
            tree = self.unflatten(item)
            self.data = self.append(tree)



    def set_hierachy(self, data):

        if len (data) == 0:
            print ("No data - Failed to set hierachy")
            return
        
        data = data[0]

        self.hierachy = pd.DataFrame ([x for x in data.keys()], columns=['ColumnName'])
        self.hierachy['level'] =  self.hierachy['ColumnName'].apply(lambda x: int(len(x.split('.'))) - 1)
        self.hierachy['parents'] = self.hierachy['ColumnName'].apply(lambda x: [x for x in x.split('.')[:-1]])
        



    def __unflatten(hierachy, flat_dict):
        """
        Converts a flat dictionary with dot-separated keys into a nested structure.

        This generalized function infers the structure by treating numeric keys
        as list indices and all other keys as dictionary keys.
        """
        nested_dict = {}

        for key, value in flat_dict.items():
            parts = key.split('.')
            current_level = nested_dict

            # Iterate through all parts of the key except the last one
            for i, part in enumerate(parts[:-1]):
                next_part = parts[i + 1]

                # This part is a dictionary key
                if part not in current_level:
                    # Look ahead to create either a list or a dict for the next level
                    current_level[part] =  {}
                # Move the pointer to the next dictionary
                current_level = current_level[part]

            # Set the value at the final level
            last_part = parts[-1]
            
            current_level[last_part] = value
                
        return nested_dict


    def unflatten2(flat_dict):
        """
        Converts a flat dictionary with dot-separated keys into a nested structure.

        This generalized function infers the structure by treating numeric keys
        as list indices and all other keys as dictionary keys.
        """
        nested_dict = {}

        for key, value in flat_dict.items():
            parts = key.split('.')
            current_level = nested_dict
            for i, part in enumerate(parts[:-1]):
                next_part = part[i+1]

                if part not in current_level:
                    current_level[part] = {}


                current_level = current_level[part]
                


        




if __name__ == "__main__":
    dict_list = []
    for item in dictionary:
        dict_list.append(unflatten(item))


    print (dict_list)
    dict_groupby(dict_list)




    my_data = [
    {'School': 'ACS BR', 'Class': '1A2', 'Students': {'Name': 'Peter', 'SurName': 'Wirija', 'Subject': {'Name': 'English', 'Sememester': 1, 'Grade': 'A'}, 'Parent': {'Surname': 'Wirija', 'Name': 'William'}}},
    {'School': 'ACS BR', 'Class': '1A2', 'Students': {'Name': 'Peter', 'SurName': 'Wirija', 'Subject': {'Name': 'English', 'Sememester': 1, 'Grade': 'A'}, 'Parent': {'Surname': 'Wirija', 'Name': 'Megawati'}}},
    {'School': 'ACS BR', 'Class': '1A2', 'Students': {'Name': 'Peter', 'SurName': 'Wirija', 'Subject': {'Name': 'English', 'Sememester': 2, 'Grade': 'A'}, 'Parent': {'Surname': 'Wirija', 'Name': 'Megawati'}}},
    {'School': 'ACS BR', 'Class': '1A3', 'Students': {'Name': 'Jane', 'SurName': 'Doe', 'Subject': {'Name': 'Math', 'Sememester': 1, 'Grade': 'B'}, 'Parent': {'Surname': 'Doe', 'Name': 'John'}}}
]

            




