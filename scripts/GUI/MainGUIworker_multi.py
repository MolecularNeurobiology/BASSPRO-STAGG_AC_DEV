#%%
#region Libraries

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from form import Ui_Plethysmography
import csv
import subprocess
from subprocess import PIPE, Popen
import datetime
import time
import os
import json
import pyodbc
import threading
import multiprocessing
import concurrent.futures
from MainGui import *

import sys
from pathlib import Path, PurePath
import shutil
import pandas
import re
import importlib
import logging
import asyncio

#endregion

#region futurama
def futurama_py(Plethysmography):
    print('futurama_py thread id',threading.get_ident())
    print("futurama_py process id",os.getpid())
    futures = set()
    with concurrent.futures.ProcessPoolExecutor(max_workers=int(Plethysmography.parallel_combo.currentText())) as executor:
    # with concurrent.futures.ProcessPoolExecutor() as executor:
        print("futurama")
        for job in get_jobs_py(Plethysmography):
            future = executor.submit(go_py,job)
            futures.add(future)
        concurrent.futures.wait(futures)
        # summary = wait_for(futures)
        print("submission?")
    # return summary

def futurama_r(Plethysmography):
    print('futurama_r thread id',threading.get_ident())
    print("futurama_r process id",os.getpid())
    futures = set()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print("futurama")
        for job in get_jobs_r(Plethysmography):
            future = executor.submit(go_r,job)
            futures.add(future)
        concurrent.futures.wait(futures)
        # summary = wait_for(futures)
        print("submission?")

def futurama_stamp(Plethysmography):
    print('futurama_stamp thread id',threading.get_ident())
    print("futurama_stamp process id",os.getpid())
    futures = set()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print("futurama")
        for job in get_jobs_stamp(Plethysmography):
            future = executor.submit(go_stamp,job)
            futures.add(future)
        concurrent.futures.wait(futures)
        # summary = wait_for(futures)
        print("submission?")

#endregion
# def wait_for(futures):
#     results = []
#     for future in concurrent.futures.wait(futures):
#         err = future.exception()
#         if err is None:
#             results.append(future.result())
#         else:
#             raise err
#     return results

#region get_jobs
def get_jobs_py(Plethysmography):
    print('get_jobs_py thread id',threading.get_ident())
    print("get_jobs_py process id",os.getpid())
    for file_py in Plethysmography.signals:
        print(file_py)
        breathcaller_cmd = 'python -u "{module}" -i "{id}" -f "{signal}" -o "{output}" -a "{metadata}" -m "{manual}" -c "{auto}" -p "{basic}"'.format(
            module = Plethysmography.breathcaller_path,
            id = Plethysmography.input_dir_py,
            output = Plethysmography.output_dir_py,
            signal = os.path.basename(file_py),
            metadata = Plethysmography.metadata,
            manual = Plethysmography.mansections,
            # manual = "NONE", 
            auto = Plethysmography.autosections,
            # auto = "NONE",
            basic = Plethysmography.basicap
        )
        # breathcaller_cmd = 'python -u "{module}" -i "{id}" -f "{signal}" -o "{output}" -a "{metadata}" -m "{manual}" -p "{basic}"'.format(
        #     module = Plethysmography.breathcaller_path,
        #     id = Plethysmography.input_dir_py,
        #     output = Plethysmography.output_dir_py,
        #     signal = os.path.basename(file_py),
        #     metadata = Plethysmography.metadata,
        #     manual = Plethysmography.mansections,
        #     # manual = "", 
        #     # auto = Plethysmography.autosections,
        #     auto = "NONE",
        #     basic = Plethysmography.basicap
        # )
        yield breathcaller_cmd
        # this follows the example for the sake of my sanity but it's obviously redundant as is. However, if we have each signal file be its own job, we could approximate blah.

def get_jobs_r(Plethysmography):
    print('R env route')
    print('get_jobs_r thread id',threading.get_ident())
    print("get_jobs_r process id",os.getpid())
    
    # if os.path.basename(Plethysmography.input_dir_r).endswith("RData"):
    if all([r.endswith("RData") for r in Plethysmography.input_dir_r]):
        pipeline_des = os.path.join(Plethysmography.papr_dir, "Pipeline_env.R")
    elif any([r.endswith("RData") for r in Plethysmography.input_dir_r]):
        pipeline_des = os.path.join(Plethysmography.papr_dir, "Pipeline_env_multi.R")
    else:
        pipeline_des = os.path.join(Plethysmography.papr_dir, "Pipeline.R")
        Plethysmography.input_dir_r = os.path.dirname(Plethysmography.input_dir_r)
        
    papr_cmd='"{rscript}" "{pipeline}" -d "{d}" -J "{j}" -R "{r}" -G "{g}" -F "{f}" -O "{o}" -T "{t}" -S "{s}" -M "{m}" -B "{b}" -I "{i}"'.format(
            rscript = Plethysmography.gui_config['Dictionaries']['Paths']['rscript'],
            # pipeline = os.path.join(Plethysmography.papr_dir, "Pipeline.R"),
            pipeline = pipeline_des,
            d = Plethysmography.mothership,
            # j = os.path.join(Plethysmography.mothership, "JSON"),
            j = Plethysmography.input_dir_r,
            r = Plethysmography.variable_config,
            # r = Plethysmography.v.configs["variable_config"]["path"],
            # r = "C:/Users/atwit/Desktop/Mothership/R_config/variable_config.csv",
            # r = "D:/BCM/Man4_Monte Carlo/STAGG inputs/r_config.csv",
            # g = Plethysmography.v.configs["graph_config"]["path"],
            g = Plethysmography.graph_config,
            # g = "D:/BCM/Man4_Monte Carlo/STAGG inputs/g_config.csv",
            # f = "C:/Users/atwit/Desktop/Mothership/R_config/o_config.csv",
            f = Plethysmography.other_config,
            # f = Plethysmography.v.configs["other_config"]["path"],
            # o = "C:/Users/atwit/Desktop/PAPR/PAPR Output/STAGG_output/STAGG_output_20220124_160750",
            # o = os.path.join(self.mothership, "Output"),
            o = Plethysmography.output_dir_r,
            t = os.path.join(Plethysmography.papr_dir, "Data_import.R"),
            s = os.path.join(Plethysmography.papr_dir, "Statistical_analysis.R"),
            m = os.path.join(Plethysmography.papr_dir, "Graph_generator.R"),
            b = os.path.join(Plethysmography.papr_dir, "Optional_graphs.R"),
            i = Plethysmography.image_format
    )
    yield papr_cmd
    
      
def get_jobs_stamp(Plethysmography):
    print('get_jobs_stamp thread id',threading.get_ident())
    print("get_jobs_stamp process id",os.getpid())
    for file_st in Plethysmography.signals:
        print(file_st)
        stamp_cmd = 'python -u "{stamper}" --s "{signal}" --n "{need}"'.format(
            stamper = Plethysmography.gui_config['Dictionaries']['Paths']['timestamper'],
            # stamper = "C:/Users/atwit/Desktop/Plethysmography/Plethysmography_trim/stimestamp.py",
            signal = file_st,
            need = Plethysmography.gui_config['Dictionaries']['Timestamps'][1])
        yield stamp_cmd

#endregion

#region update_progress
def update_Rprogress():
        # self.go_r()
        print("update_Rprogress is happening")
        print('update_Rprogress thread id', int(QThread.currentThreadId()))
        print("update_Rprogress process id",os.getpid())
        self.completed = 0
        for i in range(101):
            self.completed = i
            self.hangar.append(str(self.completed))
            QApplication.processEvents()
            time.sleep(0.1)
            self.progressBar_r.setValue(self.completed)

#endregion

#region go
def go_py(breathcaller_cmd):
    tic=datetime.datetime.now()
    print(tic)
    print("going?")
    print('go_py thread id', int(QThread.currentThreadId()))
    print("go_py process id",os.getpid())
    # Ui_MiniPleth.mini_hangar.append("Breathcaller command: "+breathcaller_cmd)
    print(breathcaller_cmd)

    py_proc=subprocess.Popen(breathcaller_cmd, stdout= subprocess.PIPE)

    while True:
        output = py_proc.stdout.readline().decode('utf8')
        if output=='' and py_proc.poll() is not None:
            break
        if output!='': 
            print(output.strip())
        #     for line in output.strip():
        #         self.completed += 1
        # if 'PROGRESS:' in output.strip():
        #     current_progress=self.parse_progress(output.strip())
        #     print('***  {percent_complete}  |  {time_remaining}  |  {estimated_total_time}  |  {current_file_no}  |  {total_file_no}  ********'.format(**current_progress))
        #     # self.completed = float(current_progress['percent_complete'])
    
    toc=datetime.datetime.now()
    print(toc)
    print(toc-tic)
    Ui_Plethysmography.hangar.append(toc-tic)
    return py_proc

def go_r(papr_cmd):
    tic=datetime.datetime.now()
    print(tic)
    print("going?")
    print('go_r thread id', int(QThread.currentThreadId()))
    print("go_r process id",os.getpid())
    print(papr_cmd)

    r_proc=subprocess.Popen(papr_cmd, stdout= subprocess.PIPE)

    while True:
        output = r_proc.stdout.readline().decode('utf8')
        if output=='' and r_proc.poll() is not None:
            break
        if output!='': 
            print(output.strip())
        #     for line in output.strip():
        #         self.completed += 1
        # if 'PROGRESS:' in output.strip():
        #     current_progress=self.parse_progress(output.strip())
        #     print('***  {percent_complete}  |  {time_remaining}  |  {estimated_total_time}  |  {current_file_no}  |  {total_file_no}  ********'.format(**current_progress))
        #     # self.completed = float(current_progress['percent_complete'])
    
    toc=datetime.datetime.now()
    print(toc)
    print(toc-tic)
    Ui_Plethysmography.hangar.append(toc-tic)
    return r_proc

def go_stamp(stamp_cmd):
    tic=datetime.datetime.now()
    print(tic)
    print('go_stamp thread id', int(QThread.currentThreadId()))
    print("go_stamp process id",os.getpid())
    print(stamp_cmd)

    stamp_proc = subprocess.Popen(stamp_cmd, stdout = subprocess.PIPE)

    while True:
        output = stamp_proc.stdout.readline().decode('utf8')
        if output == '' and stamp_proc.poll() is not None:
            break
        if output != '':
            print(output.strip())
    
    toc=datetime.datetime.now()
    print(toc)
    print(toc-tic)
    return stamp_proc

#endregion