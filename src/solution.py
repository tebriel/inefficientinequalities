#!/usr/bin/env python

"""
Written by Chris Moultrie <chris@moultrie.org> @tebriel
Available on Github at https://github.com/tebriel/inefficientinequalities
This was a lot of fun, thanks.

Usage: python solution.py
"""

# Order is important here
operators = ['==', '>=', '>', '<=', '<', '!=']

def parse_version(version):
    versionObj = {}
    for operator in operators:
        if version.startswith(operator):
            versionObj['operator'] = operator
            numbers = version.lstrip(operator).split('.')
            versionObj['numbers'] = [int(num) for num in numbers]
            break

    return versionObj

def organize_and_sort(versions_string):
    versions = versions_string.split(' ')
    versionObjs = [parse_version(version) for version in versions]
    versionObjs = sorted(versionObjs, key=lambda version: version['numbers'])
    return versionObjs

def reduce_list(versions):
    if len(versions) <= 1:
        return versions
    for index, version in enumerate(versions):
        # Out of range, bail
        if index+1 == len(versions):
            continue
        # Eliminate redundant operators for versions
        cur_op = version['operator']
        next_op = versions[index+1]['operator']
        if cur_op == next_op:
            del versions[index]
            continue
        elif '==' in [cur_op, next_op]:
            return "unsatisfiable"

    return versions


inputs = ["<5.0.1 >=3.0", "<3.0 <3.1", ">2 >=2.1 <4 !=4.5", "<3.0 ==3.1"]

if __name__ == "__main__":
    #input_string = raw_input('Enter Version String: ')
    # DEBUG
    for input_string in inputs:
        versionObjs = organize_and_sort(input_string)
        print reduce_list(versionObjs)
