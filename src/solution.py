#!/usr/bin/env python

"""
Written by Chris Moultrie <chris@moultrie.org> @tebriel
Available on Github at https://github.com/tebriel/inefficientinequalities
This was a lot of fun, thanks.

Usage: python solution.py (will ask for input)
       python solution.py "[string]"
       python solution.py test
"""

import sys

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

        to_eval = "%s%s%s" % (current[VER], following[OP], following[VER])
        first = eval(to_eval)

        to_eval = "%s%s%s" % (following[VER], current[OP], current[VER])
        second = eval(to_eval)

        # If the second one is invalid, kill it
        if first and not second:
            copy.remove(following)
        # If the first one is invalid, kill it
        elif not first and second:
            copy.remove(current)
        # If neither are valid, kill both with fire
        elif not first and not second:
            copy.remove(current)
            copy.remove(following)

    return copy

def format_output(versions):
    """Reconstruct our new version string"""
    output = ''
    strings = []
    if len(versions) == 0:
        return "unsatisfiable"
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
    ]

    results = [
        ">=3.0 <5.0.1",
        "<3.0",
        ">3.1",
        ">=2.1 <4",
        "unsatisfiable",
        ">2.10",
        ">3.0.0",
    ]

    for index, input_string in enumerate(inputs):
        versionObjs = organize_and_sort(input_string)
        versions = reduce_list(versionObjs)
        success = format_output(versions) == results[index]
        if success:
            print 'pass'
        else:
            print "%s --------> %s" % (input_string, format_output(versions))
        
    # Testing END

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        do_tests()
    else:
        if len(sys.argv) > 1:
            input_string = sys.argv[1]
        else:
            input_string = raw_input('Enter Version String: ')
        versionObjs = organize_and_sort(input_string)
        versions = reduce_list(versionObjs)
        print format_output(versions)
        sys.exit(0)

