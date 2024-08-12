#!/usr/bin/env python

import subprocess
import os,sys
import optparse
import argparse
import math
import random
import numpy as np

def gen_uniform_int_random_seeds_(low, high, size):
    np.random.seed()
    r = np.random.uniform(low=low, high=high, size=size)
    return [int(x) for x in r]

def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option(      '--nRuns'       ,    dest='nRuns'              , help='number of run, 0-indexed'     , default=-1 ,      type=int)
parser.add_option('-n', '--nEvts'       ,    dest='nEvts'              , help='number of events to generate' , default=100,      type=int)
#parser.add_option('-s', '--randomSeed'  ,    dest='randomSeed'         , help='random seed for generator process' , default=0,    type=int)
parser.add_option('-d', '--datatype'    ,    dest='datatype'           , help='data type or particle to shoot', default='h2h2ll')
parser.add_option('-o', '--out'         ,    dest='out'                , help='output directory'             , default=os.getcwd() )
parser.add_option('-e', '--eosout'         ,    dest='eosout'                , help='eos path to save root file to EOS',         default='')
parser.add_option('-E', '--eosin'         ,    dest='eosin'                , help='eos path to read input root file from EOS',         default='')
parser.add_option('-S', '--no-submit'   ,    action="store_true",  dest='nosubmit'           , help='Do not submit batch job.')
parser.add_option('-G', '--gridProxy',  action="store_true",  dest='gridProxy'           , help='initialise grid proxy')
parser.add_option('--skip-MGstep'   ,    action="store_true",  dest='skipMGStep'           , help='Skip first MG5 step: copy step1 file from eos.')
parser.add_option(      '--nbps'       , dest='nBPs'      , type=int,   help='Number of Benchmark Points', default=40)
parser.add_option( '--ecmList'         , dest='ecmList'        , type='string', help='list of sqrt(s)', action='callback',callback=get_comma_separated_args,default=[240,365])
parser.add_option( '--bpList'         , dest='bpList'        , type='string', help='list of benchmark points', action='callback',callback=get_comma_separated_args, default=[1,2])
parser.add_option('-T', '--teddy-grid'   ,    action="store_true",  dest='dogrid'           , help="Do Teddy's grid in mH,mA.")



(opt, args) = parser.parse_args()

# Read a CSV file into a NumPy array
data = np.loadtxt('MG5prod/Teddy/cards/input_arguments_test.txt', delimiter=',')

outDirSub='%s/%s/Teddy/%s'%(os.getcwd(),opt.out,opt.datatype)
for ecm in opt.ecmList:
    if opt.dogrid:
        for mH,mA in data:
            outDir='%s/ECM%d_MH%d_MA%d'%(outDirSub,int(ecm),int(mH),int(mA))
    else:    
        if opt.nBPs>0:
            for bpnum in range(1,opt.nBPs+1):
                outDir='%s/ECM%d_BP%d'%(outDirSub,int(ecm),bpnum)
        else:
            for bpnum in opt.bpList:
                outDir='%s/ECM%d_BP%d'%(outDirSub,int(ecm),int(bpnum))

    os.system('mkdir -p %s'%outDir)

eosDir='%s/%s'%(opt.eosout,opt.datatype)
eosDirIn='%s/%s'%(opt.eosin,opt.datatype)

eoscp='eos cp'
eosls='eos ls'
eosmk='eos mkdir'
if '/eos/user' in opt.eosin: 
    eoscp='cp'
if '/eos/user' in opt.eosout:
    eoscp='cp'
    eosls='ls'
    eosmk='mkdir'


#gen_kwargs = dict(low=0, high=100000, size=opt.nRuns)
#seeds = gen_uniform_int_random_seeds_(**gen_kwargs)

#To access PU files on the grid
#os.environ['X509_USER_PROXY'] = "%s/.gridproxy.pem"%(os.environ['HOME'])
#export X509_USER_PROXY=/afs/cern.ch/user/${USER:0:1}/${USER}/x509up_u${UID} # if you plan to run skims with HTCondor

#if (opt.gridProxy) :
#    os.system('voms-proxy-init --valid 168:00')

#os.system('voms-proxy-info')

#wrapper
#It has to be $(Step) for condor submit to understand ! 
#Could be also $Process if want unique identifier when submitting parallel jobs. 
#Step will go from 0 to nJobs-1 when doing > queue nJobs.
if opt.dogrid:
    labels=('ecm','mh','ma')
    tags=('ECM','MH','MA')
    outlabel='MH${MH}_MA${MA}'
    outTag='e${ECM}_mH${MH}_mA${MA}'
else:
    labels=('ecm','bpnum')
    tags=('ECM','BP')
    outlabel='BP${BP}'
    outTag='e${ECM}_bp${BP}'

scriptFile = open('%s/runJob.sh'%(outDirSub), 'w')
scriptFile.write('#!/bin/bash\n')
scriptFile.write('echo "- STARTING of runJob: " >> runJob.log\n')
if opt.dogrid:
    scriptFile.write('ARGS=`getopt -o "" -l ",ecm:,mh:,ma:" -n "getopts_${0}" -- "$@"`\n')
else:
    scriptFile.write('ARGS=`getopt -o "" -l ",ecm:,bpnum:" -n "getopts_${0}" -- "$@"`\n')
scriptFile.write('echo "-- Parsing arguments : " ${ARGS} >> runJob.log\n')
scriptFile.write('eval set -- "$ARGS"\n')
scriptFile.write('while true; do\n')
scriptFile.write('case "$1" in\n')
for l,t in zip(labels, tags):
    scriptFile.write('--'+l+')\n')
    scriptFile.write('if [ -n "$2" ]; then\n')
    scriptFile.write('{}="${{2}}";\n'.format(t))
    scriptFile.write('echo "'+l+': ${'+t+'}" >> runJob.log;\n')
    scriptFile.write('fi\n')
    scriptFile.write('shift 2;;\n')
scriptFile.write('--)\n')
scriptFile.write('shift\n')
scriptFile.write('break;;\n')
scriptFile.write('esac\n')
scriptFile.write('done\n\n')

scriptFile.write('localdir=`pwd`\n')
scriptFile.write('echo "Job local dir: ${localdir}"\n')
scriptFile.write('export HOME=%s\n'%(os.environ['HOME']))

scriptFile.write('cd {}/\n'.format(os.getcwd()))
scriptFile.write('source {}/setup.sh\n'.format(os.getcwd()))
scriptFile.write('cd $localdir\n')
if not opt.skipMGStep:
    scriptFile.write('mg5_aMC %s/ECM${ECM}_%s/new_proc_card.dat\n'%(outDirSub,outlabel))
    scriptFile.write('cp %s/ECM${ECM}_%s/new_run_card.dat ECM${ECM}_%s/Cards/run_card.dat\n'%(outDirSub,outlabel,outlabel))

    scriptFile.write('rm ECM${ECM}_%s/me_inputcard.dat\n'%outlabel) 
    scriptFile.write('echo \"multi_run %d run_output\">>ECM${ECM}_%s/me_inputcard.dat\n'%(opt.nRuns,outlabel))
    #scriptFile.write('echo "pythia=ON" >> ECM${ECM}_%s/me_inputcard.dat\n')
    #scriptFile.write('echo "delphes=ON" >> ECM${ECM}_%s/me_inputcard.dat\n')
    #scriptFile.write('echo "%s/%s/pythia8_hadronisation.dat" >> ECM${ECM}_%s/me_inputcard.dat\n'%(os.getcwd(),opt.out))
    #scriptFile.write('echo "%s/%s/card_IDEA.tcl" >> ECM${ECM}_%s/me_inputcard.dat\n'%(os.getcwd(),opt.out))
#MG5prod/Teddy/cards/mH50/idm_dilepton_mH50_mA100/idm_dilepton_mH50_mA100_customizecards.dat
    scriptFile.write('cat %s/ECM${ECM}_%s/new_customizecards.dat >> ECM${ECM}_%s/me_inputcard.dat\n'%(outDirSub,outlabel,outlabel))
    scriptFile.write('echo \"set ptl 0.5\">>ECM${ECM}_%s/me_inputcard.dat\n'%(outlabel)) 
    scriptFile.write('echo \"set sde_strategy 1\">>ECM${ECM}_%s/me_inputcard.dat\n'%(outlabel)) 
    scriptFile.write('echo \"set nevents %d\">>ECM${ECM}_%s/me_inputcard.dat\n'%(opt.nEvts,outlabel)) 
    scriptFile.write('./ECM${ECM}_%s/bin/madevent ECM${ECM}_%s/me_inputcard.dat\n'%(outlabel,outlabel)) 
    scriptFile.write('gunzip ECM${ECM}_%s/Events/run_output/unweighted_events.lhe.gz\n'%outlabel) 
    scriptFile.write('sed \"s!<LHEFILE>!ECM${ECM}_%s/Events/run_output/unweighted_events.lhe!g\" %s/%s/p8_lhereader.cmd | sed "s!<NEVTS>!%d!g" > ECM${ECM}_%s/lhereader.cmd\n'%(outlabel,os.getcwd(),opt.out,opt.nEvts*opt.nRuns,outlabel))
    #scriptFile.write('k4run %s/%s/pythia.py -n %d --out.filename ECM${ECM}_%s/EDM4HEPevents.root --Pythia8.PythiaInterface.pythiacard ECM${ECM}_%s/lhereader.cmd | tee ECM${ECM}_%s/lhereader.log\n'%(os.getcwd(),opt.out,opt.nEvts*opt.nRuns)) 
    scriptFile.write('DelphesPythia8_EDM4HEP %s/%s/card_IDEA_winter2023.tcl %s/%s/edm4hep_IDEA_winter2023.tcl ECM${ECM}_%s/lhereader.cmd ECM${ECM}_%s/Delphes_EDM4HEPevents.root | tee ECM${ECM}_%s/DelphesP8.log\n'%(os.getcwd(),opt.out,os.getcwd(),opt.out,outlabel,outlabel,outlabel))
else:
    scriptFile.write('mkdir -p ECM${ECM}_%s\n'%outlabel)
    scriptFile.write('%s %s/LHEevents_%s.lhe.gz ECM${ECM}_%s/LHEevents.lhe.gz\n'%(eoscp,eosDirIn,outTag,outlabel))
    scriptFile.write('gunzip ECM${ECM}_%s/LHEevents.lhe.gz\n'%outlabel) 
    scriptFile.write('sed \"s!<LHEFILE>!ECM${ECM}_%s/LHEevents.lhe!g\" %s/%s/p8_lhereader.cmd | sed "s!<NEVTS>!%d!g" > ECM${ECM}_%s/lhereader.cmd\n'%(outlabel,os.getcwd(),opt.out,opt.nEvts*opt.nRuns,outlabel))
    scriptFile.write('DelphesPythia8_EDM4HEP %s/%s/card_IDEA_winter2023.tcl %s/%s/edm4hep_IDEA_winter2023.tcl ECM${ECM}_%s/lhereader.cmd ECM${ECM}_%s/Delphes_EDM4HEPevents.root | tee ECM${ECM}_%s/DelphesP8.log\n'%(os.getcwd(),opt.out,os.getcwd(),opt.out,outlabel,outlabel,outlabel))


#scriptFile.write('\n') 
#scriptFile.write('\n') 
#scriptFile.write('\n') 
#scriptFile.write('\n') 



scriptFile.write('echo "--Local directory is " $localdir >> runJob.log\n')
#scriptFile.write('voms-proxy-info >> runJob.log\n')
scriptFile.write('echo home=$HOME >> runJob.log\n')
scriptFile.write('echo path=$PATH >> runJob.log\n')
scriptFile.write('echo ldlibpath=$LD_LIBRARY_PATH >> runJob.log\n')
scriptFile.write('ls -ltrh * >> runJob.log\n')
if not opt.skipMGStep:
    scriptFile.write('gzip ECM${ECM}_%s/Events/run_output/unweighted_events.lhe\n'%outlabel) 
    scriptFile.write('mv ECM${ECM}_%s/Events/run_output/unweighted_events.lhe.gz ECM${ECM}_%s/LHEevents.lhe.gz\n'%(outlabel,outlabel)) 
if len(opt.eosout)>0:
    scriptFile.write('%s -p %s\n'%(eosmk,eosDir))
    if not opt.skipMGStep:
        scriptFile.write('for outfile in LHEevents.lhe.gz Delphes_EDM4HEPevents.root; do\n')
    else:
        scriptFile.write('for outfile in Delphes_EDM4HEPevents.root; do\n')
    scriptFile.write('ext=${outfile#*.}\n')
    scriptFile.write('base=${outfile%%.*}\n')
    scriptFile.write('%s ECM${ECM}_%s/${outfile} %s/${base}_%s.${ext}\n'%(eoscp,outlabel,eosDir,outTag))
    scriptFile.write('if (( "$?" != "0" )); then\n')
    scriptFile.write('echo " --- Problem with copy of ${outfile} file to EOS. Keeping locally." >> runJob.log\n')
    scriptFile.write('cp ECM${ECM}_%s/${outfile} %s/ECM${ECM}_%s/.\n'%(outlabel,outDirSub,outlabel))
    scriptFile.write('else\n')
    scriptFile.write('eossize=`%s -l %s/${base}_%s.${ext} | awk \'{print $5}\'`\n'%(eosls,eosDir,outTag))
    scriptFile.write('localsize=`ls -l ECM${ECM}_%s/${outfile} | awk \'{print $5}\'`\n'%outlabel)
    scriptFile.write('if [ $eossize != $localsize ]; then\n')
    scriptFile.write('echo " --- Copy of ${outfile} file to eos failed. Localsize = $localsize, eossize = $eossize. Keeping locally..." >> runJob.log\n')
    scriptFile.write('cp ECM${ECM}_%s/${outfile} %s/ECM${ECM}_%s/.\n'%(outlabel,outDirSub,outlabel))
    scriptFile.write('else\n')
    scriptFile.write('echo " --- Size check done: Localsize = $localsize, eossize = $eossize" >> runJob.log\n')
    scriptFile.write('echo " --- File ${outfile} successfully copied to EOS: %s/${base}_%s.${ext}" >> runJob.log\n'%(eosDir,outTag))
    scriptFile.write('fi\n')
    scriptFile.write('fi\n')
    scriptFile.write('done\n')

else:
    if not opt.skipMGStep:
        scriptFile.write('cp ECM${ECM}_%s/LHEevents.lhe.gz %s/ECM${ECM}_%s/.\n'%(outlabel,outDirSub,outlabel))
    scriptFile.write('cp ECM${ECM}_%s/Delphes_EDM4HEPevents.root %s/ECM${ECM}_%s/.\n'%(outlabel,outDirSub,outlabel))


scriptFile.write('cp runJob.log %s/ECM${ECM}_%s/.\n'%(outDirSub,outlabel))
scriptFile.write('cp ECM${ECM}_%s/*.html %s/ECM${ECM}_%s/.\n'%(outlabel,outDirSub,outlabel))
#scriptFile.write('cp ECM${ECM}_%s/lhereader.log %s/ECM${ECM}_%s/.\n'%(outDirSub))
scriptFile.write('cp ECM${ECM}_%s/DelphesP8.log %s/ECM${ECM}_%s/.\n'%(outlabel,outDirSub,outlabel))
scriptFile.write('echo "All done"\n')
scriptFile.close()

#print('Getting proxy')
#subprocess.check_output(['voms-proxy-info','-path'])

#proxyPath=os.popen('voms-proxy-info -path')
#proxyPath=proxyPath.readline().strip()

#submit
condorFile = open('%s/condorSubmitProd.sub'%(outDirSub), 'w')
#condorFile.write('x509userproxy = $ENV(X509_USER_PROXY)\n')
#condorFile.write('use_x509userproxy = True\n')
condorFile.write('universe = vanilla\n')
condorFile.write('+JobFlavour = "nextweek"\n')
condorFile.write('Executable = %s/runJob.sh\n'%outDirSub)
if opt.dogrid:
    condorFile.write('Arguments = --ecm $(ECM) --mh $(MH) --ma $(MA)\n')
    condorlab='MH$(MH)_MA$(MA)'

else:
    condorFile.write('Arguments = --ecm $(ECM) --bpnum $(BP)\n')
    condorlab='BP$(BP)'

condorFile.write('Output = %s/ECM$(ECM)_%s/condor.out\n'%(outDirSub,condorlab))
condorFile.write('Error  = %s/ECM$(ECM)_%s/condor.err\n'%(outDirSub,condorlab))
condorFile.write('Log    = %s/ECM$(ECM)_%s/condor.log\n'%(outDirSub,condorlab))

if opt.dogrid:
    condorFile.write('Queue 1 ECM, MH, MA from (\n')
    for ecm in opt.ecmList:
        for mh,ma in data:
            condorFile.write('{}, {}, {}\n'.format(ecm,int(mh),int(ma)))
else:
    condorFile.write('Queue 1 ECM, BP from (\n')
    for ecm in opt.ecmList:
        if opt.nBPs>0:
            for bpnum in range(1,opt.nBPs+1):
                condorFile.write('{}, {}\n'.format(ecm,bpnum))
        else:
            for bpnum in opt.bpList:
                condorFile.write('{}, {}\n'.format(ecm,bpnum))

condorFile.write(')')

condorFile.close()

os.system('chmod u+rwx %s/runJob.sh'%outDirSub)
if opt.nosubmit : os.system('echo condor_submit %s/condorSubmitProd.sub'%(outDirSub)) 
else: 
    os.system('echo submitting job %s'%(outDirSub))
    os.system('condor_submit %s/condorSubmitProd.sub'%(outDirSub))

