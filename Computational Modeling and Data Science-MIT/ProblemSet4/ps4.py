# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    numViruses = 100
    #numViruses_list = [100,350,600,850]
    maxPop = 1000
    #maxPop_list = [1000,1500,2000,2500]
    maxBirthProb = 0.1
    #maxBirthProb_list = [0.1,0.25,0.5,0.8]
    #clearProb = 0.05
    #clearProb_list = [0.05,0.2,0.5,0.8]
    resistances = {"guttagonol": False}
    mutProb = 0.005
    nTimeSteps_noDrug = [300,150,75,0]
    timesteps = 150
    nTimeSteps_withDrug = 150
    count = 1

    for timesteps in nTimeSteps_noDrug:
    #for clearProb in clearProb_list:
        result = []
        for _ in range(numTrials):            
            viruses = [ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)]*numViruses        
            patient = TreatedPatient(viruses,maxPop)
        
            for _ in range(timesteps):
                patient.update()        
            patient.addPrescription('guttagonol')
        
            for _ in range(nTimeSteps_withDrug):
                virusPop_final = patient.update()
            
            result.append(virusPop_final)
        pylab.subplot(2,2,count)
        pylab.hist(result,label=str(timesteps))
        pylab.title('Histogram plot for drug delayed')
        pylab.xlabel('Range of virus population')
        pylab.ylabel('No of trials per bin')
        pylab.legend()
        count += 1
    pylab.show()






#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    numViruses = 100
    #numViruses_list = [100,350,600,850]
    maxPop = 1000
    #maxPop_list = [1000,1500,2000,2500]
    maxBirthProb = 0.1
    #maxBirthProb_list = [0.1,0.25,0.5,0.8]
    clearProb = 0.05
    #clearProb_list = [0.05,0.2,0.5,0.8]
    resistances = {'guttagonol': False, 'grimpex': False}
    mutProb = 0.005

    nTimeSteps_noDrug = 150
    nTimeSteps_gutt = [300,150,75,0]
    nTimeSteps_grim = 150

    count = 1

    for timesteps in nTimeSteps_gutt:
    #for clearProb in clearProb_list:
        result = []
        for _ in range(numTrials):            
            viruses = [ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)]*numViruses        
            patient = TreatedPatient(viruses,maxPop)
        
            for _ in range(timesteps):
                patient.update()       

            patient.addPrescription('guttagonol')        
            for _ in range(timesteps):
                patient.update()

            patient.addPrescription('grimpex')        
            for _ in range(nTimeSteps_grim):
                virusPop_final = patient.update()            
            
            result.append(virusPop_final)

        pylab.subplot(2,2,count)
        pylab.hist(result,label=str(timesteps))
        pylab.title('Histogram plot for administrating 2 drugs separately')
        pylab.xlabel('Range of virus population')
        pylab.ylabel('No of trials per bin')
        pylab.legend()
        count += 1
    pylab.show()

#simulationDelayedTreatment(2)
simulationTwoDrugsDelayedTreatment(100)