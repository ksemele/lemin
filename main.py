#!/usr/bin/env python3
import os
import sys
from sys import argv
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from termcolor import colored, cprint  # цветной cprint https://pypi.org/project/termcolor/


class GrafixStruct:
    def __init__(self, data):
        # grafix part
        self.root = Tk()
        self.fig = plt.figure(1, figsize=(5, 5), dpi=200, edgecolor='w', tight_layout=True)
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=self.root)
        if data != 0:
            self.pos = nx.spring_layout(data.graph)
        self.width = 1020
        self.height = 1060


class ParsedData:
    def __init__(self, graph, start_name, end_name):
        self.graph = graph
        self.coords = []
        self.start_name = start_name
        self.end_name = end_name
        self.curr_node = 0
        self.solution_loaded = False
        self.solution = []
        self.curr_ants = []
        self.g_ants = nx.Graph()
        self.ants = 0
        self.start_ants = 0
        self.end_ants = 0

    def save_coords(self, curr_name, x, y):
        tmp_node = {}
        tmp_node['name'] = curr_name
        tmp_node['x'] = int(x)
        tmp_node['y'] = int(y)
        self.coords.append(tmp_node)

    def ft_init_graph(self, map, grafix):
        ft_print_func_name('init graph')
        g = nx.Graph()
        # open file
        if map == 'not map':
            cprint(map)
        if map != 'not map':
            cprint("open map: " + map)
            try:
                file = open(map)
            except FileNotFoundError:
                return
            for line in file:
                if line[0] != '#':
                    self.start_ants = int(line)
                    break
            self.ants = self.start_ants
            cprint("ANTS: ", end=' ', color='red')
            print(self.start_ants)  # todo del
            rooms = []
            check_start = 0
            check_end = 0
            for line in file:
                # check & save start, end
                if check_start == 1:
                    self.start_name = line.split().pop(0)
                    cprint("start name: ", end=' ', color='blue')
                    print(self.start_name)  # todo del
                    check_start = 0
                if check_end == 1:
                    self.end_name = line.split().pop(0)
                    cprint("end name: ", end=' ', color='green')
                    print(self.end_name)  # todo del
                    check_end = 0
                if line == '##start\n':
                    check_start = 1
                elif line == '##end\n':
                    check_end = 1
                if ' ' not in line and line[0] != '#':  # filter edges (links)
                    break
                if line[0] != '#':
                    rooms.append(line.split())
            file = open(map)
            edges = []
            for line in file:
                if line[0] != '#' and '-' in line:
                    line = ' '.join(line.split())  # remove '\n' for correctly splitting
                    edges.append(line.split(sep='-'))
            # END parsing
        # fill Graph from list && fill all node_names
            room_names = rooms.copy()
            for i in range(len(room_names)):
                curr_node = room_names.pop()
                curr_name = curr_node.pop(0)
                self.graph.add_node(curr_name)
                y = curr_node.pop()
                x = curr_node.pop()
                self.save_coords(curr_name, x, y)
            self.graph.add_edges_from(edges)  # fill all edges
            grafix.pos = nx.spring_layout(self.graph)
            for each in self.coords:
                grafix.pos[each['name']] = each['x'], each['y']  # fill XY coords from data
            self.solution_loaded = False


def ft_print_func_name(name):
    cprint("func:", 'cyan', end=" ")
    cprint("{}\n".format(name), 'green')


def ft_parse_solution(data):
    ft_print_func_name('parse_solution')
    try:
        file = open(data.solution)
    except FileNotFoundError:
        print('no solution loaded')
        data.solution_loaded = False
        return
    data.solution_loaded = True
    data.curr_ants.clear()
    data.curr_ants = file.read().rstrip().split('\n')
    data.curr_ants.reverse()


def ft_open_solution(data, grafix):
    # new_solution
    ft_print_func_name('open_solution')
    grafix.root.attributes("-topmost", False)
    data.solution_loaded = True
    data.solution = askopenfilename()
    if data.solution == "":
        print("you don't load solution!")
        data.solution_loaded = False
        return
    ft_parse_solution(data)


def ft_open_map(data, grafix):
    ft_print_func_name('open_map')
    if data.graph:
        data.graph.clear()
    grafix.root.attributes("-topmost", False)
    new_map = askopenfilename()  # open new *.map
    if new_map == "":
        print("you don't open map!")
        return
    grafix.fig.clf()  # clear figure
    data.ft_init_graph(new_map, grafix)
    data.solution_loaded = False
    ft_embed_graph(data, grafix)


def ft_embed_graph(data, grafix):
    grafix.root.tk_setPalette('gray60')
    w = (grafix.root.winfo_screenwidth() // 2) - grafix.width // 2
    h = (grafix.root.winfo_screenheight() // 2) - grafix.height // 2
    grafix.root.attributes("-topmost", True)  # lift root to top of all windows
    grafix.root.geometry('1020x1060+{}+{}'.format(w, h))  # create window with shift
    grafix.root.title("lemin visualiser v 0.3")
    # draw graph
    nx.draw_networkx_nodes(data.graph, grafix.pos,  node_color="gray", node_size=150)
    nx.draw_networkx_nodes(data.graph, grafix.pos, nodelist=[data.start_name], node_color='b', node_size=230)
    nx.draw_networkx_nodes(data.graph, grafix.pos, nodelist=[data.end_name], node_color='g', node_size=230)
    ant_patch = mpatches.Patch(color='red', label='Ants')
    start_patch = mpatches.Patch(color='b', label='Start')
    end_patch = mpatches.Patch(color='g', label='End')
    plt.legend(handles=[ant_patch, start_patch, end_patch])
    nx.draw_networkx_labels(data.graph, grafix.pos, font_size=8, font_color='k')
    nx.draw_networkx_edges(data.graph, grafix.pos, edge_color='gray')
    grafix.canvas = FigureCanvasTkAgg(figure=grafix.fig, master=grafix.root)
    grafix.canvas.draw()
    grafix.canvas.get_tk_widget().grid(row=1, columnspan=3, padx=10, pady=10)


if __name__ == '__main__':
    sys.stderr.close()
    # init graph
    grafix = GrafixStruct(0)
    g = nx.Graph()
    data = ParsedData(g, 0, 0)
    if len(argv) == 2:
        data.ft_init_graph(argv[1], grafix)
    else:
        data.ft_init_graph('./test.map', grafix)
    grafix.root.tk_setPalette('gray60')
    w = (grafix.root.winfo_screenwidth() // 2) - grafix.width // 2
    h = (grafix.root.winfo_screenheight() // 2) - grafix.height // 2
    grafix.root.attributes("-topmost", True)  # lift root to top of all windows
    grafix.root.geometry('1020x1060+{}+{}'.format(w, h))  # create window with shift
    grafix.root.title("lemin visualiser v 0.3")
    # draw graph
    nx.draw_networkx_nodes(data.graph, grafix.pos, node_color="gray", node_size=150)
    nx.draw_networkx_nodes(data.graph, grafix.pos, nodelist=[data.start_name], node_color='b', node_size=230)
    nx.draw_networkx_nodes(data.graph, grafix.pos, nodelist=[data.end_name], node_color='g', node_size=230)
    ant_patch = mpatches.Patch(color='red', label='Ants')
    start_patch = mpatches.Patch(color='b', label='Start')
    end_patch = mpatches.Patch(color='g', label='End')
    plt.legend(handles=[ant_patch, start_patch, end_patch])
    nx.draw_networkx_labels(data.graph, grafix.pos, font_size=8, font_color='k')
    nx.draw_networkx_edges(data.graph, grafix.pos, edge_color='gray')
    # buttons
    Button(text="Open map", width=10, command=lambda: ft_open_map(data, grafix)).grid(row=0, column=0, padx=5, pady=5)
    Button(text="Open solution", width=10, command=lambda: ft_open_solution(data, grafix)).grid(row=0, column=1, padx=5, pady=5)


    def ft_next_step(data, grafix):  # idk why, but this is work correctly
        if not data.solution_loaded:
            cprint('need open solution file!')
        else:
            cprint('opened solution: ', end=' ', color='yellow')
            print(data.solution)
            data.g_ants.clear()
            if data.curr_ants:
                ants = data.curr_ants.pop().split(' ')
                data.ants = len(ants)
                for each in ants:
                    each = ''.join(each).split('-')[-1:]
                    for ant in each:
                        if ant == data.end_name:
                            data.end_ants += 1
                            data.ants -= 1
                        data.g_ants.add_node(ant)
                print('CURR', ants)  # todo del
            else:
                print('ants end (:')
                data.solution_loaded = False
            # draw graph
            nx.draw_networkx_nodes(data.graph, grafix.pos, node_color="gray", node_size=150)
            nx.draw_networkx_labels(data.graph, grafix.pos, font_size=8, font_color='k')
            nx.draw_networkx_edges(data.graph, grafix.pos, edge_color='gray')
            nx.draw_networkx_nodes(data.g_ants, grafix.pos, node_color="r", node_size=60)
            if data.start_ants - data.ants - data.end_ants > 0:
                nx.draw_networkx_nodes(data.graph, grafix.pos,
                                            nodelist=[data.start_name], node_color="r", node_size=60)
            grafix.canvas.draw()

    Button(text="Next step", width=10, command=lambda: ft_next_step(data, grafix)).grid(row=0, column=2, padx=5, pady=0)
    # end buttons
    grafix.canvas = FigureCanvasTkAgg(figure=grafix.fig, master=grafix.root)
    grafix.canvas.draw()
    grafix.canvas.get_tk_widget().grid(row=2, columnspan=3, padx=10, pady=10)
    grafix.root.update()
    grafix.root.mainloop()
    cprint("\nEND working visualiser.\nhave a nice day! :)\n", 'magenta')
