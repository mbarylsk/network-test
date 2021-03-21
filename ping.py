#
# Copyright (c) 2017-2021, Marcin Barylski
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
import time
import os

################################################################################
# Settings
################################################################################
# number of ping requests in single test case
n = 10
# exercised IP address
IP = 'www.facebook.com'
# command responsible for sending ICMP request 
ping_command = "ping -n " + str(n) + " " + IP
# number of iterations
max_iterations = 100000
# number of times without internet at all
no_internet = 0

################################################################################
# Global variables for results
################################################################################
list_checkpoints = []
list_loss = []
list_min = []
list_max = []
list_avg = []
list_no_inet = []

################################################################################
# Create result folder if required
################################################################################
results_folder_prefix = "Results/"
results_folder = results_folder_prefix + time.strftime('%a-%H-%M-%S')
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

################################################################################
# Gets decimal number from text lines array from line at index
#
# @param text - array of text lines
# @param index - index in text
#
# @output - decimal number
################################################################################
def get_number_from_text(text, index):
    return (int(text[index].decode("utf-8").replace('(', '').replace(',', '').replace('ms', '').replace('%', '')))

################################################################################
# Gets ping results data
#
# @param data - output of ping command
#
# @output - loss, min/max/avg response time values
################################################################################
def get_ping_results (data):

    loss_value = 100
    min_value = 0
    max_value = 0
    avg_value = 0
    j = 0
    while (j < len(data)):
        element = data[j].decode("utf-8")
        if element == "Lost":
            loss_value = get_number_from_text (data, j+3)
        if element == "Minimum":
            min_value = get_number_from_text (data, j+2)
        if element == "Maximum":
            max_value = get_number_from_text (data, j+2)
        if element == "Average":
            avg_value = get_number_from_text (data, j+2)
        j += 1
            
    return (loss_value, min_value, max_value, avg_value)

################################################################################
# Saves figures
#
# @output - figures in output directory
################################################################################
def save_figures ():
    global results_folder, list_checkpoints, list_min, list_max, list_avg, list_loss

    plt.figure(1)
    plt.plot(list_checkpoints, list_min, 'b-', ms=1)
    plt.plot(list_checkpoints, list_max, 'r-', ms=1)
    plt.plot(list_checkpoints, list_avg, 'g-', ms=1)
    blue_patch = mpatches.Patch(color='blue', label='min')
    red_patch = mpatches.Patch(color='red', label='max')
    green_patch = mpatches.Patch(color='green', label='avg')
    plt.legend(handles=[red_patch, blue_patch, green_patch], loc='upper right', bbox_to_anchor=(0.8, 0.8))
    plt.xlabel('Iteration')
    plt.ylabel('Time [ms]')
    plt.title('Ping maximum/minimum/average response time')
    plt.grid(True)
    plt.savefig(results_folder + "/f_ping_minmaxavg.png")

    plt.figure(2)
    plt.plot(list_checkpoints, list_loss, 'b-', ms=1)
    plt.xlabel('Iteration')
    plt.ylabel('%')
    plt.title('Ping reply loss rate [%]')
    plt.grid(True)
    plt.savefig(results_folder + "/f_ping_loss.png")

    plt.figure(3)
    plt.plot(list_checkpoints, list_no_inet, 'b-', ms=1)
    plt.xlabel('Iteration')
    plt.ylabel('%')
    plt.title('No internet at all')
    plt.grid(True)
    plt.savefig(results_folder + "/f_ping_no_inet.png")

i = 0
while (i < max_iterations):

    # run command
    (output, error) = subprocess.Popen(ping_command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True).communicate()
    try:
        # get results
        data = output.split()
        (loss_value, min_value, max_value, avg_value) = get_ping_results (data)

        # remember results
        list_checkpoints.append(i)
        list_loss.append(loss_value)
        list_min.append(min_value)
        list_avg.append(avg_value)
        list_max.append(max_value)

        if loss_value == 100:
            no_internet += 1
        else:
            no_internet = 0

    except:
        print ("Exception found for: ", data)
        no_internet += 1

    list_no_inet.append(no_internet)
        
    i += 1

    print ("Loss rate[%], min/max/avg res time [ms]: ", loss_value, min_value, max_value, avg_value)
    
    save_figures ()
