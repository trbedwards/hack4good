Run On Sun
==========

Install PyEphem, package for performing astronomy calculations.

Install FreeGLUT, open source alternative to the OpenGL Utility Toolkit: yum install freeglut-devel

Run main.py, replacing the argument for heightMap = numpy.load with an Esri grid and specifying a desired date and time.

Compile resulting C file: gcc current.c -lglut -lGLU -lGU

Control camera direction with arrow keys, 'a' to move forwards and 's' to move backwards.
