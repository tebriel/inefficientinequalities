#!/usr/bin/env python3

"""
Written by Chris Moultrie <chris@moultrie.org> @tebriel
Available on Github at https://github.com/tebriel/inefficientinequalities
This was a lot of fun, thanks.

Usage: python solution.py (will ask for input)
       python solution.py "[string]"
       python solution.py test
"""

import sys
from code import InteractiveConsole

OP, VER, OG = range(0,3)

# Order is important here
operators = ['==', '>=', '>', '<=', '<', '!=']

def parse_version(version):
    versionObj = {}
    for operator in operators:
        if version.startswith(operator):
            numbers = version.lstrip(operator).split('.')
            numbers = [int(num) for num in numbers]
            versionObj = (operator, numbers, version)
            break

    return versionObj
def strip_zeros(numbers):
    result = numbers
    zero_index = -1
    for index, num in enumerate(reversed(numbers)):
        if num == 0:
            zero_index = index
        else:
            break
    if zero_index > -1:
        result = numbers[:(zero_index+1)*-1]

    return result


def organize_and_sort(versions_string):
    # Kill whitespace WITH FIRE, WE didn't start it, but it was always
    # burning...
    versions_string = versions_string.strip()
    versions = versions_string.split(' ')
    versionObjs = [parse_version(version) for version in versions]
    versionObjs = sorted(versionObjs, key=lambda version: version[VER])
    return versionObjs

def reduce_list(versions):
    # Safety Check
    # we can check if we want to, we can leave those versions behind.
    # 'cause your versions don't check and if they don't check well, they're
    # no versions of mine
    if len(versions) <= 1:
        return versions

    # Removing these from the list we're working on was a bad idea, the copy is
    #   nicer
    copy = [version for version in versions]

    for index, current in enumerate(versions):
        # Out of range, bail
        if index+1 == len(versions):
            continue
        following = versions[index+1]

        # Eliminate redundant operators for versions
        # This is horrifically gross and insecure, never ever ever ever ever
        # ever ever use this in production

        # Basically the idea here is, we can eval the ops given to us against
        # these sorted arrays of numbers. Python is nice enough to sort arrays
        # based on their individual contents, so [3,10,0] > [3,1,0]
        # If these numbers cannot coexist from left to right in numerical
        # order, things are no bueno. I have a vague sense that there's
        # some edge case I'm not thinking of here, but I haven't been able to
        # form one.
        following_ver = strip_zeros(following[VER])
        current_ver = strip_zeros(current[VER])

        to_eval_first = "%s%s%s" % (current_ver, following[OP], following_ver)
        first = eval(to_eval_first)

        to_eval_second = "%s%s%s" % (following_ver, current[OP], current_ver)
        second = eval(to_eval_second)

        # If the second one is invalid, kill it
        if first and not second:
            if copy.count(following):
                copy.remove(following)
        # If the first one is invalid, kill it
        elif not first and second:
            if copy.count(current):
                copy.remove(current)
        # If neither are valid, kill both with fire
        elif not first and not second:
            if copy.count(current):
                copy.remove(current)
            if copy.count(following):
                copy.remove(following)

        # Catch that gosh darn >3 !=3
        # But this breaks on >3 <3 and that makes me a sad panda
        if current_ver == following_ver:
            trouble = ['>', '<']
            # Gross
            if current[OP] in trouble and following[OP] in trouble:
                curr_idx = trouble.index(current[OP])
                follow_idx = trouble.index(following[OP])
                if curr_idx != follow_idx:
                    if copy.count(current):
                        copy.remove(current)
                    if copy.count(following):
                        copy.remove(following)
                    continue

            not_allowed = ['==','!=']
            if current[OP] not in not_allowed:
                copy.append(current)
            elif following[OP] not in not_allowed:
                copy.append(following)

    return copy

def format_output(versions):
    """Reconstruct our new version string"""
    output = ''
    strings = []
    if len(versions) == 0:
        return "unsatisfiable"
    versions = sorted(versions, key=lambda version: version[VER])
    for version in versions:
        strings.append("%s%s" % (version[OP], '.'.join(map(str, version[VER]))))
    return ' '.join(strings)

def do_tests():
    """Mini Test Harness, probably would've benefited from a real one..."""
    # Testing START
    inputs = [
        "<5.0.1 >=3.0",
        "<3.0 <3.1",
        ">3.0 >3.1",
        ">2 >=2.1 <4 !=4.5",
        "<3.0 ==3.1",
        ">2.10 >2.0",
        ">3.0.0 >3 >3.0",
        ">3 !=3",
        "!=3 >3",
        ">=2 <3 !=2.2",
        ">3.0 !=3",
        ">3 !=3.0",
        # Begin Yury's Tests
        '>=1.1 ==3',
        '>=1.1 ==3.1.1 <=7.0.2',
        '==3.1.1 <=7.0.2',
        '==3.1.1',
        '>=1.1 <=7.0.2 !=1.1 !=0.3',
        '>=1.1 !=1.1 !=0.3 !=2',
        '!=1.1 !=0.3 !=2',
        '!=1.1 !=0.3 !=2 <=2 !=999.999',
        '>7.7.1 <7.7.1',
        '>1 !=1',
        '>3 >=2.1 <=4.5 !=5.0',
    ]

    results = [
        ">=3.0 <5.0.1",
        "<3.0",
        ">3.1",
        ">=2.1 <4",
        "unsatisfiable",
        ">2.10",
        ">3",
        ">3",
        ">3",
        ">=2 !=2.2 <3",
        ">3.0",
        ">3",
        # Begin Yury's Results
        '==3',
        '==3.1.1',
        '==3.1.1',
        '==3.1.1',
        '!=1.1 >=1.1 <=7.0.2',
        '!=1.1 >=1.1 !=2',
        '!=0.3 !=1.1 !=2',
        '!=0.3 !=1.1 !=2 <=2',
        'unsatisfiable',
        '>1',
        '>3 <=4.5',
    ]

    for index, input_string in enumerate(inputs):
        previous_run = ''
        current_run = input_string
        while current_run not in [previous_run, 'unsatisfiable']:
            previous_run = current_run
            versionObjs = organize_and_sort(current_run)
            versions = reduce_list(versionObjs)
            current_run = format_output(versions)

        success = format_output(versions) == results[index]
        if success:
            print('pass')
        else:
            print("Expected %s to be %s\n\tInstead got: %s\n" % (input_string,
                results[index], format_output(versions)))

    # Testing END

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        do_tests()
    else:
        if len(sys.argv) > 1:
            input_string = sys.argv[1]
        else:
            prompt = 'Enter Version String: '
            console = InteractiveConsole()
            input_string = console.raw_input(prompt=prompt)
        previous_run = ''
        current_run = input_string
        while current_run not in [previous_run, 'unsatisfiable']:
            previous_run = current_run
            versionObjs = organize_and_sort(current_run)
            versions = reduce_list(versionObjs)
            current_run = format_output(versions)
        print(current_run)

