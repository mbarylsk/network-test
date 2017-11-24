#
# Copyright (c) 2017, Marcin Barylski
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.
# 

import subprocess
import string
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.mlab as mlab
import numpy as np
import time
import os

list_checkpoints = []
list_loss = []
list_min = []
list_max = []
list_avg = []

n = 10
IP = 'www.google.com'
ping_command = "ping -n " + str(n) + " " + IP
base = (n-1)*6
max_iterations = 100000
results_folder = time.strftime('%a-%H-%M-%S')
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

def save_figures (directory):
    global list_checkpoints, list_min, list_max, list_avg, list_loss
    plt.figure(1)
    plt.plot(list_checkpoints, list_min, 'b-', ms=2)
    plt.plot(list_checkpoints, list_max, 'r-', ms=2)
    plt.plot(list_checkpoints, list_avg, 'g-', ms=2)
    blue_patch = mpatches.Patch(color='blue', label='min [ms]')
    red_patch = mpatches.Patch(color='red', label='max [ms]')
    green_patch = mpatches.Patch(color='green', label='avg [ms]')
    plt.legend(handles=[red_patch, blue_patch, green_patch], loc='upper right', bbox_to_anchor=(0.8, 0.8))
    plt.xlabel('Iteration')
    plt.ylabel('Time [ms]')
    plt.title('Max/Min/Avg response time')
    plt.grid(True)
    plt.savefig(directory + "/f_minmaxavf.png")

    plt.figure(2)
    plt.plot(list_checkpoints, list_loss, 'b-', ms=2)
    plt.xlabel('Iteration')
    plt.ylabel('%')
    plt.title('Loss rate')
    plt.grid(True)
    plt.savefig(directory + "/f_loss.png")

i = 1
while (i < max_iterations):

    (output, error) = subprocess.Popen(ping_command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True).communicate()
    try:
        data = output.split()
        j = 0
        while (j < len(data)):
            element = data[j].decode("utf-8")
            if element == "Lost":
                loss_value = data[j+3].decode("utf-8").replace('(', '').replace('%', '')
            if element == "Minimum":
                min_value = data[j+2].decode("utf-8").replace('(', '').replace(',', '').replace('ms', '')
            if element == "Maximum":
                max_value = data[j+2].decode("utf-8").replace('(', '').replace(',', '').replace('ms', '')
            if element == "Average":
                avg_value = data[j+2].decode("utf-8").replace('(', '').replace(',', '').replace('ms', '')
            j += 1

        list_checkpoints.append(i)
        list_loss.append(int(loss_value))
        list_min.append(int(min_value))
        list_avg.append(int(avg_value))
        list_max.append(int(max_value))
    except:
        print (data)
        
    i += 1
	
    print (loss_value, min_value, max_value, avg_value)
	
    save_figures (results_folder)
