#!/usr/bin/env python

# Import our venv.py
import venv


# These imports require packages which shouldn't exist without
#  our virtualenv being created

if __name__ == '__main__':
    import AdvancedHTMLParser
    print ( "%s version=%s" %(str(AdvancedHTMLParser), str(AdvancedHTMLParser.__version__) ) )
    import cachebust
    print ( "%s version=%s" %(str(cachebust), str(cachebust.__version__) ) )


