# lemin visualiser

The purpose of lemin project is to find paths from start room to end room and to move ants by these paths with the least amount of steps.
Core version (parser, algorithm) writed with my teammate @cghael in C [link](https://github.com/cghael/21_school_Lemin)

The visualiser is a bonus for visual represent correct maps and solutions.
Writed in Python.

# How to run program?

If you use <venv> (highly recommeded)
make new venv:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements.txt
(venv)$ ./main.py
```
  
after work don't remember exit venv:
```
(venv)$ deactivate
```

# map
Map is a file \*.map with a template:
```
# any comment, just skip
# first number is a number of ants in start vertex
10
# rooms - vertex of graph [name] [x_coord] [y_coord]
# ##start ##end - start, end vertexes
##start
a 10 10
##end
b 60 5
c 10 20
# links between vertexes
a-b
b-c
```
# solution
Solutions you can generate from our binary lem-in program.
Use -h to help:
```
$ ./lem-in -h
```
For generate solution file use this:
```
$ ./lem-in -of test.map
```
lem-in write solution to `test.sol`
Visualiser work only with correct data.
