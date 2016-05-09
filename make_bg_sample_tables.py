#!/usr/bin/python

# needs localSetupPyAMI

import os, subprocess

susytoolsfile='/data/uclhc/uci/user/amete/analysis_n0222/SUSYTools/data/susy_crosssections_13TeV.txt'
xsecfile=open(susytoolsfile)

inputdir='/data/uclhc/uci/user/dantrim/n0222val/filelists'
grouplist=(
'diboson_sherpa',
'drellyan_sherpa',
'singletop',
'ttbar',
'wjets_sherpa',
'zjets_sherpa',
)

# Loop over each group
for group in grouplist:
    print ''
    print ''
    print '===================================================================='
    print 'Listing %s ...' % (group)
    print ''
    print ''
    # Get list of all samples in a given group
    samples=subprocess.Popen('ls  %s/%s'%(inputdir,group),shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Create, open and start filling the output
    os.system('mkdir -p output/')
    output=open('output/%s_samples_table.tex'%(group),'w')
    output.write('\\begin{table}[h]\n')
    output.write('\\begin{center}\n')
    output.write('\\resizebox{\\textwidth}{!}{\n')
    output.write('\\tiny\n')
    output.write('\\begin{tabular}{llllrr}\n')
    output.write('Sample name & $\sigma$ [pb] & $k$-Factor & $\epsilon_{\mathrm{filter}}$ & $N_{\mathrm{gen}}$ & $L_{\mathrm{equiv}}$ [fb$^{-1}$] \\\\ \n')
    # Loop over all samples in the group
    for sample in samples.stdout.readlines(): 
        gridname=sample.split('.SusyNt.')[0].split('.phys-susy.')[1]+str('.evgen.EVNT.')+sample.split('.SusyNt.')[1].split('_')[0]
        name=sample.split('.SusyNt.')[0].split('.mc15_13TeV.')[1]
        print 'Sample : %s'%(name)
        dsid=name.split('.')[0]
        xsec=0; kfac=0; eff=0; relUnc=0; nEvt=0;
        for line in xsecfile:
            if '#' in line : continue
            lineTokens=line.split()
            if len(lineTokens) == 0: continue
            if lineTokens[0]==dsid :
                xsec   = lineTokens[2]
                kfac   = lineTokens[3] 
                eff    = lineTokens[4] 
                relUnc = lineTokens[5]
                break 
        xsecfile.seek(0)
        #print '{:60s} & {:10s} & {:10s} & {:10s}'.format(name,xsec,kfac,eff)
        # Read Nevt from grid
        gridinfo=subprocess.Popen('ami show dataset info %s'%(gridname),shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for gridline in gridinfo.stdout.readlines():
            if 'totalEvents' in gridline:
                nEvt=gridline.split(':')[1].split('\n')[0]
                break
        # Write into file    
        output.write('%65s & %10s & %10s & %10s & %10s & %10s \\\\ \n' % (
            name.replace('_','\_'),
            xsec,
            kfac,
            eff,
            nEvt,
            str(int(float(nEvt)/float(xsec)/float(kfac)/float(eff)*0.001))
        ))
    # Finish writing into the file and close    
    output.write('\hline\n')
    output.write('\end{tabular}}\n')
    output.write('\end{center}\n')
    output.write('\caption{List of simulated samples of %s. The dataset ID, the generator  cross section $\sigma$, the $k$-Factor, the generator filter efficiency $\epsilon_{\mathrm{filter}}$, the total number of generated events $N_{\mathrm{gen}}$ and the equivalent luminosity ($L_{\mathrm{equiv}}$) calculated using $N_{\mathrm{gen}}$ are reported.}\n' % (group))
    output.write('\label{tab:BGSamples_%s}\n'%(group))
    output.write('\end{table}\n')
    output.close()
