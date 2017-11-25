#!/usr/bin/env python
import subprocess
import time
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
NUMBER_RUN = 5
INSTANCES = ['gdb1', 'gdb10', 'val1A',
             'val4A', 'val7A', 'egl-e1-A', 'egl-s1-A']
TIME_LIMITS = ['10', '20', '30', '60', '90']
for i in range(NUMBER_RUN):
    seed = str(time.time())
    for instance in INSTANCES:
        for t in TIME_LIMITS:
            in_file = DIR_PATH + '/CARP_samples/%s.dat' % instance
            out_file = open('./output/%s-%s.txt' % (instance, t), 'a')
            # print(dir_path)
            command = ['python2', DIR_PATH + '/CARP_solver.py',
                       in_file, '-t', t, '-s', seed]
            process = subprocess.Popen(command, stdout=out_file)
            time_start = time.time()
            process.wait()
            time_end = time.time()
            print(instance,i, t, time_end - time_start)
