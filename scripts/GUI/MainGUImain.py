#%%
#region Libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5 import uic
from form import Ui_Plethysmography
from config_form import Ui_Config
import sys
import os
import threading
import logging
import MainGui_thready
from multiprocessing import freeze_support

#endregion

#region Main
def main():
    root = os.path.dirname(os.path.abspath(__file__))        
    QDir.addSearchPath('resources', root)
    app = QApplication(sys.argv)
    window = MainGui_thready.Plethysmography()
    # app.aboutToQuit.connect(MainGui.Plethysmography.x_byutton)
    print(window.signals)
    print('GUI thread id',threading.get_ident()) 
    print("GUI process id",os.getpid())
    loop = QEventLoop(app)
    window.show()
    app.exec_()

    logging.basicConfig(
        level = logging.INFO,
        format = 'PID %(process)5s %(name)18s: %(message)s',
        stream = sys.stderr
    )

if __name__ == "__main__": 
    freeze_support()
    main()
#endregion
# %%

# for file in os.listdir(p):
#     print(file.split('_')[0])
    # print(p+file.replace("_.adicht",f"_{m.loc[(m['MUID']==file.split('_')[0]) & (m['Gas 2']=='10% O2'),'PlyUID'].iloc[0]}.adicht"))
    
#     # print(f"{file.split('_')[0]}: {m.loc[m['MUID']==file.split('_')[0],'PlyUID'].iloc[0]}")
#     try:
#         os.rename(p+file,p+file.replace(".txt",f"_{m.loc[m['MUID']==file.split('.')[0],'PlyUID'].iloc[0]}.txt"))
#     except:
#         pass

# rint(dc[dc['start'].isna()][['animal id','PLYUID']])

# for file in os.listdir(p):
#     print(file.split('_')[1])
#     print(f"{file.split('_')[0]}: {m.loc[m['MUID']==file.split('_')[0],'PlyUID'].iloc[0]}")
#     print(p+file.replace(f"{file.split('_')[1]}",f"_{m.loc[(m['MUID']==file.split('_')[0]) & (m['Gas 2']=='7% CO2'),'PlyUID'].iloc[0]}.adicht"))
#     # try:
