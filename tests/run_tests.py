#!/usr/bin/python
import json
import os
import re
import argparse

# Constants
OPENROBOTS_DELIMITATION_PARAMETERS_TAGS = ['# Parameters to adapt the protocol',
                    '# End Parameters to adapt the protocol']

def get_arguments():
    parser = argparse.ArgumentParser(prog = 'run_tests.py', description= 'run opentrons_covid repo tests')

    parser.add_argument('-j', '--json', dest="json", metavar="json info file", type=str, required=True, help='REQUIRED. json file with parameters.')
    parser.add_argument('-t', '--template', dest="template", metavar="json info file", type=str, required=True, help='REQUIRED. Protocol template.')
    parser.add_argument('-o', '--output', type=str, required=False, help='Output file to save results')

    arguments = parser.parse_args()

    return arguments

def add_parameters_in_file (in_file, out_file, parameters):
    '''
    Description:
        The function will get protocol template file and add the parameters to create an output file
        that is stored in OPENROBOTS_OUTPUT_DIRECTORYthe Labware information used in the form to create the files
    Input:
        in_file     # template file
        out_file    # output file name
        parameters  # dictionnary with the information to include in the file
    Constans:
        OPENROBOTS_DELIMITATION_PARAMETERS_TAGS
    Return:
        form_data
    '''
    if not os.path.exists(in_file):
        return 'Protocol Template does not exists'

    with open (in_file, 'r') as in_fh:
        found_start = False
        delimitation_end_found = False
        parameters_added = True
        with open(out_file, 'w') as out_fh:
            for line in in_fh:
                parameter_section =  re.search(rf'^{OPENROBOTS_DELIMITATION_PARAMETERS_TAGS[0]}', line)
                end_parameter_section =  re.search(rf'^{OPENROBOTS_DELIMITATION_PARAMETERS_TAGS[1]}', line)
                if not found_start:
                    out_fh.write(line)
                if parameter_section :
                    found_start = True

                    for key in sorted(parameters):
                        type_of_data = get_type_of_data(parameters[key])
                        if type_of_data == 'boolean' or type_of_data == 'integer':
                            out_fh.write(key + ' = '+ str(parameters[key]) + '\n')
                        else:
                            out_fh.write(key + ' = \''+ parameters[key]+ '\'\n')
                    parameters_added = True
                    continue
                if end_parameter_section :
                    out_fh.write(line)
                    found_start = False
                    delimitation_end_found = True

    if parameters_added and delimitation_end_found :
        return 'True'
    return 'Unable to write the parameters in the protocol file'

def get_type_of_data (data):
    '''
    Description:
        The function get always as input a string class.
        By trying to convert the input data to int or bolealn it will decide the type of data
        If not possible to conver it returns string
    Return:
        type_of_data
    '''
    boolean_values = ['True', 'False', 'None']
    if data in boolean_values :
        return 'boolean'
    try:
        integer = int(data)
        return 'integer'
    except:
        return 'string'

def main():
    ## get args
    args = get_arguments()
    print(args)

    ## load json
    with open(args.json, 'r') as file:
        try:
            parameters=json.load(file)
        except ValueError as e:
            print("json decoding has failed")
            print(e)

    add_parameters_in_file(args.template,args.output,parameters)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
