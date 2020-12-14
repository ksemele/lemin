# lemin visualiser

The purpose of lemin project is to find paths from start room to end room and to move ants by these paths with the least amount of steps.
Core version (parser, algorithm) writed with my teammate @cghael in C [link](https://github.com/cghael/21_school_Lemin)

The visualiser is a bonus for visual represent correct maps and solutions.
Writed in Python.

# How to run program?

If you use `<venv>` (I highly recommend do this) 

First, make new `<venv>`:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements.txt
(venv)$ ./main.py
```
  
After work don't remember exit venv:
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
# pictures
After start Visualiser open default `test.map`.
![Start Visualiser](https://github.com/ksemele/lemin/blob/main/pic/1.jpg)
You can open other map from `./maps/` by a `Open map` button.
Programm show you readed graph.
![Open test3.map](https://github.com/ksemele/lemin/blob/main/pic/2.jpg)
If you load solution by a `Open solution` you can clicking on a `Next step` button.
Programm visualise you every *step* sending ants in a graph.

>For all test maps i already loaded solutions in `./solutions` dir.

![Loaded test3.sol](https://github.com/ksemele/lemin/blob/main/pic/3.jpg)
In a console you may see all info in text.
