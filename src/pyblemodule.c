#include <Python.h>
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/prctl.h>
#include <unistd.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

 
static PyObject*
le_set_scan_parameters(PyObject* self, PyObject* args)
{
	const char* name;
	
	 if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;
 
    printf("le_set_scan_parameters %s!\n", name);
 
	
	Py_RETURN_NONE;
}

static PyObject*
le_set_scan_enable(PyObject* self, PyObject* args)
{
	const char* name;
	
	 if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;

    printf("le_set_scan_enable %s!\n", name);
 	
	Py_RETURN_NONE;
}


static PyObject*
le_set_advertise_data(PyObject* self, PyObject* args)
{
	const char* name;
	
	 if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;
     printf("le_set_advertise_data %s!\n", name);
 
	
	Py_RETURN_NONE;
}

static PyObject*
le_set_advertise_scan_response_data(PyObject* self, PyObject* args)
{
	const char* name;
	
	 if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;

    printf("le_set_advertise_scan_response_data %s!\n", name);
 
	Py_RETURN_NONE;
}

static PyObject*
le_set_advertise_enable(PyObject* self, PyObject* args)
{
	const char* name;
	
	 if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;
 
	printf("le_set_advertise_enable %s!\n", name);
 
	Py_RETURN_NONE;
}

static PyMethodDef PyBleMethods[] =
{
    {"le_set_advertise_enable", le_set_advertise_enable, METH_VARARGS, "Greet somebody."},
    {"le_set_advertise_scan_response_data", le_set_advertise_scan_response_data, METH_VARARGS, "Greet somebody."},
 	{"le_set_advertise_data", le_set_advertise_data, METH_VARARGS, "Greet somebody."},
	{"le_set_scan_enable", le_set_scan_enable, METH_VARARGS, "Greet somebody."},
	{"le_set_scan_parameters", le_set_scan_parameters, METH_VARARGS, "Greet somebody."},
	{NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
inithello(void)
{
     (void) Py_InitModule("pyble", PyBleMethods);
}
