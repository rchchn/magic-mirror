# -*- coding: utf-8 -*-
import logging


##########################################################################################
###############################################
#Initialization and environment configuration stuff:
import os, sys, imp
#­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­
# The following definitions set the folder structure for the host application.
# This allows the host application to import modules and panels
# while also keeping a folder structure.
#­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­
def get_main_dir():
    if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):# new py2exe OR old py2exe OR tools/freeze
        return os.path.dirname(sys.executable)
        return os.path.dirname(sys.argv[0])
base = get_main_dir()

#sys.path += [os.path.join(base,'_L3_Common_Library', 'uut'),
#             os.path.join(base,'_L3_Common_Library', 'labdevice')]

if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    sys.path.insert(0,base)
#­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­
# The following definitions set the folder structure for the host application.
# This allows the host application to import modules and panels
# while also keeping a folder structure.
#­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

def SetUpLoggingEnvironment(name='log'):
    '''set up the logging module to log the output'''
    global log
    formatter = logging.Formatter(fmt='[%(levelname)s - %(filename)s:%(lineno)d] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    fileHandler = logging.FileHandler("LOGFILE" , 'a+')
    fileHandler.setFormatter(formatter)
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.addHandler(fileHandler)
    #return log

SetUpLoggingEnvironment(__name__)
