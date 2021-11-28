# SICXE-Assembler
Assembler for the SIC XE, which has absolutely nothing to do with automatic succotash whatever that is.
# Usage
You must have python installed. To run the code, simply run 

> python SICXE_ASM.py

Ensure you have the input files in the same directory as the python script. The default names for the input files are "in.txt" and "in_set.txt". These names can be changed inside the script.

The instruction set file should contain each instruction, its format and its opcode all separated by spaces, with each instruction on a separate line.

The input file should contain a SIC or SIC/XE code. Each line is an instruction, and each instruction is in the form of 

> Label Instruction Address

In the case of a label or address not existing, replace them with at least one space.
# Result
After running the code, the following files should be generated: "out.txt", "symbTable.txt", "litTable.txt".
