# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
'''
    utils - Some general-purpose utility functions
'''

import re

__all__ = ('cmp_version', )

# Yes, cmp is DA BOMB. What a huge mistake removing it from the language!!
try:
    cmp
except NameError:
    def cmp(a, b):
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0

# ALPHA_OR_NUM_RE - groups of letters OR numbers
ALPHA_OR_NUM_RE = re.compile('([a-zA-Z]+)|([0-9]+)')

# The following method is slightly-modified from my Public Domain project, cmp_version
#   https://pypi.python.org/pypi/cmp_version
# This is copied so as to retain the "all you need is virtualenv and this module" promise.
def cmp_version(version1, version2):
    '''
        cmp_version - Compare version1 and version2.
            Returns cmp-style (C-style), i.e. < 0 if lefthand (version1) is less, 0 if equal, > 0 if righthand (version2) is greater.

        @param version1 <str> - String of a version
        @param version2 <str> - String of a version

        @return <int> -
            -1 if version1 is < version2
             0 if version1 is = version2
             1 if version1 is > version2
'''

    version1 = str(version1)
    version2 = str(version2)

    if version1 == version2:
        return 0

    # Pad left or right if we have empty blocks
    if version1.startswith('.'):
        version1 = '0' + version1
    if version1.endswith('.'):
        version1 = version1 + '0'

    if version2.startswith('.'):
        version2 = '0' + version2
    if version2.endswith('.'):
        version2 = version2 + '0'

    # Consider dots as separating "blocks", i.e. major/minor/patch/subpatch/monkey-finger, whatever.
    version1Split = version1.split('.')
    version2Split = version2.split('.')

    version1Len = len(version1Split)
    version2Len = len(version2Split)

    # Ensure we have the same number of blocks in both versions, by padding '0' blocks on the end of the shorter.
    #   This ensures that "1.2" is equal to "1.2.0", and greatly simplifies the comparison loop below otherwise.
    while version1Len < version2Len:
        version1Split += ['0']
        version1Len += 1
    while version2Len < version1Len:
        version2Split += ['0']
        version2Len += 1

    # See if the padding has made these equal
    if version1Split == version2Split:
        return 0

    # Go through each block (they have same len at this point)
    for i in range(version1Len):
        try:
            # Try to compare this block as an integer. If both are integers, but different,
            #  we have our answer.
            cmpRes = cmp(int(version1Split[i]), int(version2Split[i]))
            if cmpRes != 0:
                return cmpRes
        except ValueError:
            # Some sort of letter in here

            #  So split up the sub-blocks of letters OR numbers for comparison

            # Note, we don't try to pad here. 
            #  i.e. "1.2a" < "1.2a0".
            # This is subjective. I personaly think this is correct the way it is.
            try1 = ALPHA_OR_NUM_RE.findall(version1Split[i])
            try1Len = len(try1)
            try2 = ALPHA_OR_NUM_RE.findall(version2Split[i])
            try2Len = len(try2)

            # Go block-by-block. Each block is a set of contiguous numbers or letters.
            #   Letters are greater than numbers.
            for j in range(len(try1)):
                
                if j >= try2Len:
                    return 1

                testSet1 = try1[j]
                testSet2 = try2[j]

                res1 = cmp(testSet1[0], testSet2[0])
                if res1 != 0:
                    return res1

                res2 = 0 
                if testSet1[1].isdigit():
                    if testSet2[1].isdigit():
                        res2 = cmp(int(testSet1[1]), int(testSet2[1]))
                    else:
                        return 1
                else:
                    if testSet2[1].isdigit():
                        return 1
                if res2 != 0:
                    return res2

            if try2Len > try1Len:
                return -1

    # Equal !
    return 0


def writeStrToFile(filename, contents):
    '''
        writeStrToFile - Writes some data to a provided filename.

        @param filename <str> - A path to a file
        @param contents <str> - The contents to write to the file, replacing any previous contents.

        @return <None/Exception> - None if all goes well, otherwise the Exception raised
    '''

    try:
        with open(filename, 'wt') as f:
            f.write(contents)
    except Exception as e:
        return e

    return None
