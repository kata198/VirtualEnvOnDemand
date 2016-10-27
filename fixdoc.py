#!/usr/bin/env python

import os
import glob
import sys

import VirtualEnvOnDemand

if __name__ == '__main__':
    VirtualEnvOnDemand.enableOnDemandImporter()
    import AdvancedHTMLParser
    VirtualEnvOnDemand.toggleOnDemandImporter(False)


if __name__ == '__main__':

    # Ensure we are in the main package directory
    myDir = os.path.dirname(__file__)
    if myDir != '.':
        os.chdir(myDir)

    # Chdir to doc directory


    failedToParse = {}

#    import pdb; pdb.set_trace()
    for fname in glob.glob('doc/*.html'):

        if fname[4:] in ('index.html', 'exceptions.html'):
            continue

        try:
            parser = AdvancedHTMLParser.AdvancedHTMLParser(fname)
        except Exception as e:
            failedToParse[fname] = e
            continue

        try:
            badLink = parser.getElementsCustomFilter( lambda x : bool(x.getAttribute('href', '').startswith('file:/')))[0]
            parent = badLink.parentNode
            
            brNodeIdx = parent.children.index(badLink) - 1
            indexLinkIdx = brNodeIdx - 1

            brNode = parent.children[brNodeIdx]
            indexLink = parent.children[indexLinkIdx]

            parent.removeChild(badLink)
            parent.removeChild(brNode)

            indexLink.setAttribute('href', 'VirtualEnvOnDemand.html')
        except Exception as e:
            continue
 #           raise e
            #sys.stderr.write('Got exception
            #pass
        with open(fname, 'wt') as f:
            f.write(parser.getHTML())
