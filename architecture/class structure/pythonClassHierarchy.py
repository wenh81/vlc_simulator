import pandas as pd
import os
import numpy as np


class ClassWriter(object):
    def __init__(self, excel_file):

        # name of auto gen folder
        self.auto_gen_folder = '__auto_gen__'

        # Create auto_gen, if not exists
        if not os.path.exists(self.auto_gen_folder):
            os.mkdir(self.auto_gen_folder)
            
        # get all tab names, and assign as classNames or parent classes
        self.excel_file = excel_file
        self.eval_class_names()


    def create_classes(self):
        """Method to create the auto generated classes given spreadsheet."""
        
        # For each class (tab) write classes and unit tests
        for idxC, className in enumerate(self.listOfClasses):

            # get parent class name (if any)
            parentClass = self.listOfParentClasses[idxC]

            # Get dict for each tab / listOfTabs
            df_in = pd.read_excel(self.excel_file, sheet_name=self.listOfTabs[idxC])


            # Write the class for that module
            self.write_class(df_in, className, parentClass)

            print(f'\n******** SUCCESS: Class "{className}" created! ********\n')
            

    def create_unittests(self):
        """Method to create the auto generated unittests given spreadsheet."""
        
        # For each class (tab) write classes and unit tests
        for idxC, className in enumerate(self.listOfClasses):

            # # get parent class name (if any)
            # parentClass = self.listOfParentClasses[idxC]

            # Get dict for each tab / listOfTabs
            df_in = pd.read_excel(self.excel_file, sheet_name=self.listOfTabs[idxC])
            
            # Write basic unit tests
            self.write_unit_tests(df_in, className)

            print(f'\n******** SUCCESS: Unit test for class "{className}" created! ********\n')


    
    def get_class_tab(self, className):
        """Method to get the tab index for a given class."""

        # For each class (tab) write classes and unit tests
        for idxC, classNameTemp in enumerate(self.listOfClasses):
            if classNameTemp == className:
                # get parent class name (if any)
                # parentClass = self.listOfParentClasses[idxC]
                return idxC

    def eval_class_names(self):
        """Method to analyse the spreadsheet and return the list of 
class and parent class names."""
        # get all tab names, and assign as classNames
        xl = pd.ExcelFile(self.excel_file)
        self.listOfClasses = []
        self.listOfParentClasses = []
        self.listOfTabs = []

        for className in xl.sheet_names:
            
            # Ignore tab if name is all_config
            if className != 'all_config':

                # get the actual tab name
                self.listOfTabs.append(className)

                # Check if there is a parent class
                # if '<' in className and '>' in className:
                if '#' in className:
                    className = className.split('#')
                    self.listOfClasses.append(className[0])
                    self.listOfParentClasses.append(className[1])
                else:
                    self.listOfClasses.append(className)
                    self.listOfParentClasses.append("None")


    def write_class(self, df, className, parentClass):
        """Method to write a class given a dictionary of contents.
The string 'classStr' stores the text to become the final python script."""
        
        
        
        # write class header, with or without parent hierarchy 
        # and importing its parent
        if parentClass == "None":
            classStr = f"class {className}(object):"
        else:
            classStr = f"from {parentClass} import {parentClass}\n\n"
            classStr += f"class {className}({parentClass}):"
        
        
        # store in lists each entry from the dictionary
        listOfVars = df['variables']
        listOfDefaultVars = df['default']
        listOfVarComments = df['comment']
        listOfMethods = df['methods']
        listOfDocStrings = df['docstring']
        listOfArgsList = df['argslist']

        # Check if there is an '__init__' method. If not, raise error.
        if np.sum([1 if method == '__init__' else 0 for method in listOfMethods]) != 1:
            raise ValueError(f"\n\n*Error --> Method '__init__' not \
found at Class '{className}'.\n")
        else:
            idM = [idM for idM,method in enumerate(listOfMethods) if method == '__init__']
            idM = int(idM[0])

            # keep writting classStr with constructor method
            argslist = listOfArgsList[idM]
            docstring = listOfDocStrings[idM]
            # create the list of arguments (should be seprated by comma)
            if str(argslist) != 'nan':
                # print(argslist)
                # argslist = [item.strip() for item in argslist.split(',')]
                tempArgs = ['self']
                dict_parent_map = {}
                for item in argslist.split(','):
                    if '[' in item.strip() and  ']' in item.strip():
                        temp = item.strip().replace(']', '').split('[')
                        dict_parent_map[temp[1]] = temp[0]
                        tempArgs.append(temp[0])
                    else:
                        tempArgs.append(item.strip())
                argslist = ', '.join(tempArgs)
                # argslist = ', '.join(argslist)
                argslist = f"{argslist}"
            else:
                argslist = 'self'
            # Write the actual method
            classStr += f"""
    def __init__({argslist}):
        \"\"\"{docstring}\"\"\""""
        
        # If there is a parent, get write the inheritance "super" statement
        if parentClass != "None":
            parent_tab = self.get_class_tab(parentClass)
            df_in_parent = pd.read_excel(self.excel_file, sheet_name=self.listOfTabs[parent_tab])
            parentArgslist = df_in_parent['argslist']
            parentMethodslist = df_in_parent['methods']
            idM = [idM for idM,method in enumerate(parentMethodslist) if method == '__init__']
            idM = int(idM[0])
            argsParent = parentArgslist[idM]
            if str(argsParent) != 'nan':
                # argsParent = [item.strip() for item in argsParent.split(',')]
                tempArgs = ['self']
                for item in argsParent.split(','):
                    try:
                        tempArgs.append(f'{item.strip()} = {dict_parent_map[item.strip()]}')
                    except:
                        raise ValueError(f"\n\n*Error --> __init__ for class '{className}' \
expects mapping to parent variable '{item.strip()}' when calling parent class '{parentClass}'!\n")
                # argsParent = ', '.join(argsParent)
                # argsParent = f"self, {argsParent}"
                argsParent = ', '.join(tempArgs)
            else:
                argsParent = 'self'
        
            classStr += f"""

        {parentClass}.__init__({argsParent})
        """
        # {parentClass}.__init__({argsParent})
        # super({className},self).__init__( {argslist} )


        # Given all variables, define them with their default and 
        # a comment (if any) above each line
        for idx,var in enumerate(listOfVars):
            default = listOfDefaultVars[idx]
            comment = listOfVarComments[idx]

            # check if there is a comment
            if str(comment) != 'nan':
                comment = f"""

        # {comment}"""
            else:
                comment = ""

            # define the variable
            if str(var) != 'nan':
                if str(default) == 'nan':
                    raise ValueError(f"\n\n*Error --> No default value passed for \
variable '{var}' at Class '{className}'.\n")
                classStr += f"""{comment}
        self.{var} = {default}"""
            
        # final line break
        classStr += """
    
        pass
"""


        # Given all methods, define them with their default and 
        # a comment (if any) above each line
        for idx,funcname in enumerate(listOfMethods):
            if str(funcname) != 'nan' and str(funcname) != '__init__':
                docstring = listOfDocStrings[idx]
                # check if there is a docstring (mandatory for each method)
                if str(docstring) == 'nan':
                    raise ValueError(f"\n\n*Error --> Class '{className}' \
Method '{funcname}' at line '{idx+2}': \
does not have a docstring!\n")

                # remove brackets and strip spaces
                argslist = listOfArgsList[idx]
                # create the list of arguments (should be seprated by comma)
                if str(argslist) != 'nan':
                    argslist = [item.strip() for item in argslist.split(',')]
                    argslist = ', '.join(argslist)
                    argslist = f"self, {argslist}"
                else:
                    argslist = 'self'

                # Write the actual method
                classStr += f"""
    def {funcname}({argslist}):
        \"\"\"{docstring}\"\"\"
        pass
    
"""
        
        # Open the class file, and dump it
        python_file = os.path.join(self.auto_gen_folder, f'{className}.py')
        with open(python_file, 'w') as f:
            f.write(classStr)



    def write_unit_tests(self, df, className):
        """Method to write the unit tests for each class, from given
dictionary of contents. The string 'classUnitStr' stores the text to
become the final python unit test script."""
        
        # init by importing unittest
        classUnitStr = "import unittest\n\n"
        
        self.auto_gen_folder
        # then import the class to be tested
        classUnitStr += f"from {className} import {className}\n\n"


        # store in lists each entry from the dictionary
        listOfVars = df['variables']
        listOfDefaultVars = df['default']
        # listOfVarComments = df['comment']
        listOfMethods = df['methods']
        # listOfDocStrings = df['docstring']
        listOfArgsList = df['argslist']
        listOfDataTypeList = df['datatype']

        # classUnitStr += """def setUp(self):"""

        # get __init__ constructor
        idM = [idM for idM,method in enumerate(listOfMethods) if method == '__init__']
        idM = int(idM[0])
        argslist = listOfArgsList[idM]
        # create the list of arguments (should be seprated by comma)
        if str(argslist) != 'nan':
            tempArgs = []
            for item in argslist.split(','):
                if '[' in item.strip() and  ']' in item.strip():
                    temp = item.strip().replace(']', '').split('[')
                    tempArgs.append(temp[0])
                else:
                    tempArgs.append(item.strip())
            argslist = ', '.join(tempArgs)
            argslist = [item.strip() for item in argslist.split(',')]
            argslist = ', '.join(argslist)
            argslist = f"{argslist}"
        else:
            argslist = ''

        classUnitStr += f"""\nclass Test{className}Types(unittest.TestCase):
    
    def setUp(self):
        \"\"\" Setup function TestTypes for class {className} \"\"\"
        
        self.{className}Obj = {className}({argslist})\n"""

        # Init each var, with its default values
        for idxV,var in enumerate(listOfVars):
            # init define for the variables
            if str(var) != 'nan':
                classUnitStr += f"""
        self.{var} = self.{className}Obj.{var}"""
                
        # Add a pass for the case there are no vars, for some reason
        classUnitStr += f"""
        
        pass\n"""

        classUnitStr += f"""\n
    def test_types(self):
        \"\"\" Function to test data types for class {className} \"\"\"
        """

        # For each var, test it's data type
        for idxV,var in enumerate(listOfVars):
            default = listOfDefaultVars[idxV]
            datatype = listOfDataTypeList[idxV]

            # init define for the variables
            if str(var) != 'nan':
                if str(datatype) != 'nan':
                    classUnitStr += f"""
        self.assertIsInstance(self.{var}, {datatype})"""
                else:
                    raise ValueError(f"\n\n*Error --> Class '{className}' \
at line '{idxV+2}' does not have a datatype!\n")


        # Add a pass for the case there are no vars, for some reason
        classUnitStr += f"""
        
        pass\n"""


        ###### Write test functions for each method

        # Given all methods, write a test class for it
        for idx,funcname in enumerate(listOfMethods):
            if str(funcname) != 'nan' and str(funcname) != '__init__':
                
                # write the test class name with the setup initial function
                funcname_upper = funcname[0].upper() + funcname[1:]
                classUnitStr += f"""\nclass Test{funcname_upper}(unittest.TestCase):
    
    def setUp(self):
        \"\"\" Setup function to test method {className}.{funcname}() \"\"\"
        
        """

        #         classUnitStr += f"""self.{className}Obj = {className}()\n"""

        #         # Init each var, with its default values
        #         for idxV,var in enumerate(listOfVars):
        #             # init define for the variables
        #             if str(var) != 'nan':
        #                 classUnitStr += f"""
        # self.{var} = self.{className}Obj.{var}"""
                
                # Add a pass for the case there are no vars, for some reason
                classUnitStr += f"""
        pass\n"""
                

#                 classUnitStr += f"""\n
#     def testTypes(self):
#         \"\"\" Function to test data types for method {className}.{funcname}() \"\"\"
#         """

#                 # For each var, test it's data type
#                 for idxV,var in enumerate(listOfVars):
#                     default = listOfDefaultVars[idxV]
#                     datatype = listOfDataTypeList[idxV]

#                     # init define for the variables
#                     if str(var) != 'nan':
#                         if str(datatype) != 'nan':
#                             classUnitStr += f"""
#         self.assertIsInstance(self.{var}, {datatype})"""
#                         else:
#                             raise ValueError(f"\n\n*Error --> Method <<{funcname}>> \
# at line <{idxV+2}> does not have a datatype!\n")


#                 # Add a pass for the case there are no vars, for some reason
#                 classUnitStr += f"""
        
#         pass\n"""

        classUnitStr += f"""

if __name__ == '__main__':
    unittest.main()"""

        # Open the class file, and dump it
        python_file = os.path.join(self.auto_gen_folder, f'test_{className}.py')
        with open(python_file, 'w') as f:
            f.write(classUnitStr)

        

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# df_in = pd.read_excel(arquivo_excel_in, sheet_name='Sheet1')
# lista = ['asd', 'bsdf', 'asd']
# x = lista.sort()
# print(x)
# print([i for i in lista if i.startswith('a')])

# print(df_in.header)
# print(dir())
# print(dir(df_in).sort(lambda key: key.startswith('k') ))


if __name__ == '__main__':
    classy = ClassWriter('class_structure.xlsx')
    # classy = ClassWriter('class_structure_example.xlsx')

    # Create auto_gen classes
    classy.create_classes()
    
    # Create auto_gen unittests
    classy.create_unittests()
