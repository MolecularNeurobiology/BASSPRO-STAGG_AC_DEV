#%%
#region Libraries

import os
from pyclbr import Class
from queue import Queue
import subprocess
import threading
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal

#endregion


class WorkerSignals(QObject):
    """
    Chris Ward got the threading to work!
    
    Create signals used by the worker.

    Parameters
    --------
    QObject: class
        The WorkerSignals class inherits properties and methods from the QObject class.
    """
    finished = pyqtSignal(int)
    progress = pyqtSignal(int)
    

class Worker(QRunnable):
    """
    Chris Ward got the threading to work!

    The Worker class handles the threading and parallel processing for the main GUI.

    Parameters
    --------
    QRunnable: class
        The Worker class inherits the properties and methods from teh QRunnable class.
    """
    def __init__(self, path_to_script: str, i: int, worker_queue: Queue, pleth: Class):
        """
        Instantiate the Worker Class.

        Parameters
        ---------
        path_to_script: str
            The string yielded by get_jobs_py() or get_jobs_r() that is given to the command line to launch either BASSPRO or STAGG respectively.
        i: int
            The worker's number, determined by Plethysmography.counter.
        worker_queue: Queue
            A first-in, first-out queue constructor for safely exchanging information between threads.
        pleth: Class
            The Plethysmography Class.
        """
        super(Worker, self).__init__()
        self.path_to_script = path_to_script
        self.i = i
        self.worker_queue = worker_queue
        self.pleth = pleth
        self.signals = WorkerSignals()
        self.finished = self.signals.finished
        self.progress = self.signals.progress
    
    def run(self):
        """
        Use subprocess.Popen to run a seperate program in a new process.
        stdout will be captured by the variable self.echo and extracted below.
        
        """
        self.echo = subprocess.Popen(
            self.path_to_script,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
            )
        # Extract the stdout and feed it to the queue.
        # Emit signals whenever adding to the queue or finishing.
        running = 1
        while running == 1:
            line = self.echo.stdout.readline().decode('utf8')
            if self.echo.poll() is not None:
                running = 0
            elif line != '':
                self.worker_queue.put(line.strip())
                self.progress.emit(self.i)
        self.finished.emit(self.i)


#region get_jobs
def get_jobs_py(Plethysmography: Class):
    """
    Return the string fed to the command line to launch the BASSPRO module.

    Parameters
    --------
    Plethysmography: Class
        The Plethysmography Class.
    Plethysmography.signals: list
        The list of file paths of the user-selected .txt signal files that are analyzed by BASSPRO. Required input for BASSPRO.
    Plethysmography.breathcaller_path: str
        The path to the BASSPRO module script file. Required input for BASSPRO.
    Plethysmography.output_dir_py: str
        The path to the BASSPRO output directory. Required input for BASSPRO. This attribute is set as a file path to the timestamped BASSPRO_output_{time} folder within the BASSPRO_output directory within the user-selected directory self.mothership. It is not spawned until self.dir_checker() is called when BASSPRO is launched. Required input for BASSPRO.
    Plethysmography.metadata: str
        This attribute refers to the file path of the metadata file. Required input for BASSPRO.
    self.autosections: str
            This attribute refers to the file path of the automated BASSPRO settings file. Required input for BASSPRO.
    self.mansections: str
        This attribute refers to the file path of the manual BASSPRO settings file. Required input for BASSPRO.
    self.basicap: str
        This attribute refers to the file path of the basic BASSPRO settings file. Required input for BASSPRO.
    
    Returns
    --------
    output: breathcaller_cmd
        The string given to the command line to launch the BASSPRO module.
    """
    print('get_jobs_py thread id',threading.get_ident())
    print("get_jobs_py process id",os.getpid())
    for file_py in Plethysmography.signals:
        breathcaller_cmd = 'python -u "{module}" -i "{id}" -f "{signal}" -o "{output}" -a "{metadata}" -m "{manual}" -c "{auto}" -p "{basic}"'.format(
            # The path to the BASSPRO script:
            module = Plethysmography.breathcaller_path,
            # The path of the signal file's directory:
            id = os.path.dirname(file_py),
            # The path of the BASSPRO output directory as chosen by the user previously:
            output = Plethysmography.output_dir_py,
            # The basename of the signal file:
            signal = os.path.basename(file_py),
            # The path of the metadata file:
            metadata = Plethysmography.metadata,
            # The path of the manual settings file - if not selected, it's an empty string "":
            manual = Plethysmography.mansections,
            # The path of the automated settings file - if not selected, it's an empty string "":
            auto = Plethysmography.autosections,
            # The path of the basic settings file:
            basic = Plethysmography.basicap
        )
        yield breathcaller_cmd


def get_jobs_r(Plethysmography: Class):
    """
    Return the string fed to the command line to launch the STAGG module.

    Parameters
    --------
    Plethysmography: Class
        The Plethysmography Class.
    Plethysmography.rscript_des: str
        This attribute refers to the file path to the Rscript.exe of the user's device or of R-Portable. Required input for STAGG.
    Plethysmography.pipeline_des: str
        This attribute is set as the file path to one of two scripts that launch STAGG. If self.stagg_list has a .RData file in it, then self.pipeline_des refers to the file path for Pipeline_env_multi.R. If self.stagg_list consists entirely of JSON files, then self.pipeline_des refers to the file path for Pipeline.R. Required input for STAGG.
    Plethysmography.papr_dir: str
        This attribute refers to the directory path of the STAGG module script files. Required input for STAGG.
    Plethysmography.mothership: str
        This attribute refers to the user-selected output directory path. Required input for STAGG.
    Plethysmography.input_dir_r: str
        If self.stagg_list contains the file paths of less than 200 files, be they of the same directory or multiple directories, then this attribute is set as a string consisting of the file names joined by ", " (STAGG doesn't like brackets). This attribute is set as the directory path of the first file in self.stagg_list if self.stagg_list contains the file paths of more than 200 files from the same directory. If self.stagg_list contains the file paths of more than 200 files from multiple directories, then the user is asked to consolidate their files into one directory because STAGG can't do that. Required input for STAGG.
    Plethysmography.variable_config: str
        This attribute refers to the file path of one of the STAGG settings file, a .csv file named with the prefix "variable_config". Required input for STAGG.
    Plethysmography.graph_config: str
        This attribute refers to the file path of one of the STAGG settings file, a .csv file named with the prefix "graph_config". Required input for STAGG.
    Plethysmography.other_config: str
        This attribute refers to the file path of one of the STAGG settings file, a .csv file named with the prefix "other_config". Required input for STAGG.
    Plethysmography.output_dir_r: str
        The path to the STAGG output directory. Required input for STAGG. This attribute is set as a file path to the timestamped STAGG_output_{time} folder within the STAGG_output directory within the user-selected directory self.mothership. It is not spawned until self.dir_checker() is called when STAGG is launched. Required input for STAGG.
    Plethysmography.image_format: str
        This attribute is set as either ".svg" or ".jpeg" depending on which RadioButton the user checked in the main GUI before launching STAGG. The ".svg" button is checked by default. Required input for STAGG.

    Returns
    --------
    output: papr_cmd
        The string given to the command line to launch the STAGG module.
    """
    print('get_jobs_r thread id',threading.get_ident())
    print("get_jobs_r process id",os.getpid())
    papr_cmd='"{rscript}" "{pipeline}" -d "{d}" -J "{j}" -R "{r}" -G "{g}" -F "{f}" -O "{o}" -T "{t}" -S "{s}" -M "{m}" -B "{b}" -I "{i}"'.format(
            # The path to the local R executable file:
            rscript = Plethysmography.rscript_des,
            # The path to the STAGG script:
            pipeline = Plethysmography.pipeline_des,
            # The path to the STAGG scripts directory:
            # summary = Plethysmography.papr_dir,
            # The path to the output directory chosen by the user:
            d = Plethysmography.mothership,
            # This variable is either a list typed as string of JSON file paths produced as BASSPRO output, a list typed as string of JSON file paths produced as BASSPRO output and an .RData file path produced as STAGG output, a list typed as string containing a single path of an .RData file, or a string that is the path to a single directory containing JSON files produced as BASSPRO output.
            j = Plethysmography.input_dir_r,
            # The path to the variable_config.csv file:
            r = Plethysmography.variable_config,
            # The path to the graph_config.csv file:
            g = Plethysmography.graph_config,
            # The path to the other_config.csv file:
            f = Plethysmography.other_config,
            # The path to the directory for STAGG output:
            o = Plethysmography.output_dir_r,
            # The paths to the STAGG scripts:
            t = os.path.join(Plethysmography.papr_dir, "Data_import_multi.R"),
            s = os.path.join(Plethysmography.papr_dir, "Statistical_analysis.R"),
            m = os.path.join(Plethysmography.papr_dir, "Graph_generator.R"),
            b = os.path.join(Plethysmography.papr_dir, "Optional_graphs.R"),
            # A string, either ".jpeg" or ".svg", indicating the format of the image output from STAGG:
            i = Plethysmography.image_format
    )
    yield papr_cmd


#endregion
