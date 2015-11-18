#!/bin/sh

pydoc -w `echo VirtualEnvOnDemand/*.py | sed 's/.py//g' | sed 's|/__init__||g' | tr '/' '.'`
mv *.html doc/
