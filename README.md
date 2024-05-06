# PyTeRor

A refactoring tool which detects and combines code clones in pytest test suites through parametrization using pytest's parametrize decorator. Clones are detected using the NiCad clone detector, which is a prerequisite installation. PyTeRor focuses on refactoring Type 2 code clones. 

## Installation 

1. clone repository

2. Install requirements (pip install -r requirements.txt).

3. Install nicad.

4. Copy file 'python.grm' into txl sub-directory in nicad directory. E.g. 'sudo cp python.grm /usr/local/lib/nicad6/txl/python.grm'

5. Run makefile in nicad directory.

5. Copy file 'type2_abstracted.cfg' into config sub-directory in nicad directory. E.g. 'sudo cp type2_abstracted.cfg /usr/local/lib/nicad6/config/type2_abstracted.cfg'. 

Runs with python 3.10 <=



