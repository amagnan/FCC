import os
import numpy as np

# Name of the process
#run_prefix = 'Teddy/h2h2ll'
run_prefix = 'Teddy/h2h2llvv'
# This defines the processes and multiparticles needed for the proc_card
# put a \n in between each line
defines = 'define l+ = e+ mu+ ta+ \ndefine l- = e- mu- ta- \ndefine vl = ve vm vt \ndefine vl~ = ve~ vm~ vt~'
#process = 'e+ e- > h2 h2 l+ l-'
process = 'e+ e- > h2 h2 l+ l- vl vl~'
ebeam = [120,182.5]
modelpath = '/afs/cern.ch/work/a/amagnan/FCC/MG5prod/InertDoublet_UFO/'

# Now create the folder for it
try:
    os.mkdir(run_prefix)
except:
    pass


files = ['_proc_card.dat', '_run_card.dat', '_extramodels.dat']


def replaceInFile(file, modelpath,defines, process, run_name, eperbeam):
    file = file.replace("<MODEL>", modelpath)
    file = file.replace("<DEFINE>", defines)
    file = file.replace("<PROCESS>", process)
    file = file.replace("<RUN_NAME>", run_name)
    file = file.replace("<EBEAM>", str(eperbeam))
    return file

def readFile(filename):
    with open(filename, 'r') as f:
        file = f.read()
    return file

def saveFile(file, filename):
    with open(filename, 'w') as f:
        f.write(file)

# Read a CSV file into a NumPy array
data = np.loadtxt('Teddy/cards/input_arguments.txt', delimiter=',')
#print(data)

for eperbeam in ebeam:
    ECM = int(eperbeam*2)
    print(f'ECM = {ECM} GeV')
    for mH,mA in data:
        MH = int(mH)
        MA = int(mA)
        print(f'mH = {MH}, mA = {MA}')
        run_name = f'ECM{ECM}_MH{MH}_MA{MA}'
        run_directory = f"{run_prefix}/{run_name}"
        try:
            os.mkdir(run_directory)
        except:
            pass

        for template_filename in files:
            file = readFile(template_filename)
            
            file = replaceInFile(file, modelpath, defines, process, run_name, eperbeam)
            os.system('cp Teddy/cards/mH%d/idm_dilepton_mH%d_mA%d/idm_dilepton_mH%d_mA%d_customizecards.dat %s/new_customizecards.dat'%(MH,MH,MA,MH,MA,run_directory)) 
            filename = f'new{template_filename}'
            file_dir = f'{run_directory}/{filename}'
            saveFile(file, file_dir)

