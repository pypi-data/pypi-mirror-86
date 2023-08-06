#-------------------------------------------------------------------------------------
import glob
import os
from pathlib import Path

def ClearDir(path='./'):
    '''brief:
            Removes all files from a directory.
        params (see default values for examples):
            path - The source directory of the images to turn into a gif. 
                   Must include preceding ./, should not include ending /
        example call:
            ClearDir('./kmeans/images')'''
    print("Delete files from " + path + " y/n?")
    if(input() == 'y'):
        files = glob.glob(path + '/*')
        for f in files:
            os.remove(f)

#-------------------------------------------------------------------------------------
import cellbell
import time
def play_sound(self, etype, value, tb, tb_offset=None):
    %ding
    time.sleep(.25)
    %ding
    self.showtraceback((etype, value, tb), tb_offset=tb_offset)
def ActivateCellFailChime():
    '''brief:
            Plays a ding if the cell execution fails. Only works for Jupyter Notebook.
        example call:
            CellFailChime()'''
    get_ipython().set_custom_exc((Exception,), play_sound)

#-------------------------------------------------------------------------------------
from IPython.display import Audio, display
class VarPrinter:
     def __init__(self, ip):
         self.ip = ip
     def post_run_cell(self, result):
        if result.error_in_exec != None:
            print('womp womp')
        else:
            display(Audio(url='http://www.sa-matra.net/sounds/starwars/XWing-Laser.wav', autoplay=True))
            time.sleep(0.5)
def load_ipython_extension(ip):
    vp = VarPrinter(ip)
    ip.events.register("post_run_cell", vp.post_run_cell)

def ActivateCellDoneChime():
  '''brief:
          Plays a ding when a cell is complete. Kind of buggy with a failed cell.
        example call:
            CellDoneChime()'''
    load_ipython_extension(get_ipython())