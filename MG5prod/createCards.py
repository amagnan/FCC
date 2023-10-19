import os

# Name of the process
#run_prefix = 'h2h2ll'
run_prefix = 'h2h2llvv'
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


# Params in the form: MH, MA, MHPM, Lam2, Lam345
BP_params = [[72.77, 107.803, 114.639, 1.44513, -0.00440723], 
            [65, 71.525, 112.85, 0.779115, 0.0004], 
            [67.07, 73.222, 96.73, 0, 0.00738], 
            [73.68, 100.112, 145.728, 2.08602, -0.00440723], 
            [72.14, 109.548, 154.761, 0.0125664, -0.00234], 
            [76.55, 134.563, 174.367, 1.94779, 0.0044], 
            [70.91, 148.664, 175.89, 0.439823, 0.0058], 
            [56.78, 166.22, 178.24, 0.502655, 0.00338], 
            [76.69, 154.579, 163.045, 3.92071, 0.0096],
            [58.31, 171.148, 172.96, 0.540354, 0.00762], 
            [99.65, 138.484, 181.321, 2.46301, 0.0532], 
            [71.03, 165.604, 175.971, 0.339292, 0.00596],
            [71.03, 217.656, 218.738, 0.766549, 0.00214], 
            [71.33, 203.796, 229.092, 1.03044, -0.00122], 
            [147, 194.647, 197.403, 0.387, -0.018], 
            [165.8, 190.082, 195.999, 2.7675, -0.004], 
            [191.8, 198.376, 199.721, 1.5075, 0.008], 
            [57.475, 288.031, 299.536, 0.929911, 0.00192], 
            [71.42, 247.224, 258.382, 1.04301, -0.0032],
            [62.69, 162.397, 190.822, 2.63894, 0.0056],
            [176, 291.36, 311.96, 1.4895, -0.1035],
            [557, 562.316, 565.417, 4.0455, -0.1385],
            [560, 616.32, 633.48, 3.3795, -0.0895],
            [571, 676.534, 682.54, 1.98, -0.471],
            [671, 688.108, 688.437, 1.377, -0.1455],
            [713, 716.444, 723.045, 2.88, 0.2885],
            [807, 813.369, 818.001, 3.6675, 0.299],
            [933, 939.968, 943.787, 2.9745, -0.2435],
            [935, 986.22, 987.975, 2.484, -0.5795],
            [990, 992.36, 998.12, 3.3345, -0.040],
            [250.5, 265.49, 287.226, 3.90814, -0.150071],
            [286.05, 294.617, 332.457, 3.29239, 0.112124],
            [336, 353.264, 360.568, 2.48814, -0.106372],
            [326.55, 331.938, 381.773, 0.0251327, -0.0626727],
            [357.6, 399.998, 402.568, 2.06088, -0.237469],
            [387.75, 406.118, 413.464, 0.816814, -0.208336],
            [430.95, 433.226, 440.624, 3.00336, 0.082991],
            [428.25, 453.979, 459.696, 3.87044, -0.281168],
            [467.85, 488.604, 492.329, 4.12177, -0.252036],
            [505.2, 516.58, 543.794, 2.53841, -0.354]]

files = ['_proc_card.dat', '_run_card.dat', '_customizecards.dat', '_extramodels.dat']


def replaceInFile(file, modelpath,defines, process, run_name, params, eperbeam):
    file = file.replace("<MODEL>", modelpath)
    file = file.replace("<DEFINE>", defines)
    file = file.replace("<PROCESS>", process)
    file = file.replace("<RUN_NAME>", run_name)
    file = file.replace("<MH2>", str(params[0]))
    file = file.replace("<MH3>", str(params[1]))
    file = file.replace("<MHPM>", str(params[2]))
    file = file.replace("<LAM2>", str(params[3]/2))
    file = file.replace("<LAML>", str(params[4]/2))
    file = file.replace("<EBEAM>", str(eperbeam))
    return file

def readFile(filename):
    with open(filename, 'r') as f:
        file = f.read()
    return file

def saveFile(file, filename):
    with open(filename, 'w') as f:
        f.write(file)


for eperbeam in ebeam:
    ECM = int(eperbeam*2)
    print(f'ECM = {ECM} GeV')
    for BP_num, params in enumerate(BP_params):
        BP_num += 1
        print(f'BP = {BP_num}')
        run_name = f'ECM{ECM}_BP{BP_num}'
        run_directory = f"{run_prefix}/{run_name}"
        try:
            os.mkdir(run_directory)
        except:
            pass

        for template_filename in files:
            file = readFile(template_filename)
            
            file = replaceInFile(file, modelpath, defines, process, run_name, params, eperbeam)

            filename = f'new{template_filename}'
            file_dir = f'{run_directory}/{filename}'
            saveFile(file, file_dir)
    
