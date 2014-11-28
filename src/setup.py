from distutils.core import setup, Extension
 
module1 = Extension('pyble', sources = ['pyblemodule.c'])
 
setup (name = 'pi-restble',
        version = '1.0',
        description = 'The RestFul api for BLE Pi-Gateway',
        ext_modules = [module1])
