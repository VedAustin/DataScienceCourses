# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

''' 
Begin helper code
'''
#from ps3b_precompiled_27 import *    

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        clearRandom = random.random()
        if clearRandom < self.clearProb:
            #print 'C',clearRandom,self.clearProb
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        BirthProb = random.random()
        reproduceProb = self.maxBirthProb * (1 - popDensity)
        #print reproduceProb
        if BirthProb < (reproduceProb):
            #print 'Reproducing',BirthProb
            childVirus = SimpleVirus(self.maxBirthProb,self.clearProb)
            return childVirus
        else:
            raise NoChildException()



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        viruses = self.getViruses()
        newVirus = []
        #print self.getTotalPop(),'--'
        self.viruses = [virus for virus in viruses if not virus.doesClear()]        
        popDensity = float(self.getTotalPop())/self.getMaxPop()
        #count_yes = 0
        #count_no = 0
        #print self.getTotalPop()
        for virus in self.viruses:
            try:
                newVirus.append(virus.reproduce(popDensity))
                #count_yes += 1
            except NoChildException:
                #count_no += 1
                pass
        
        self.viruses+=newVirus         
        #print count_yes,count_no,len(newVirus),self.getTotalPop()
        return self.getTotalPop()



#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    nTimeSteps = 300
    sumTimestep = [0]*nTimeSteps
    for i in range(numTrials):
        viruses = [SimpleVirus(maxBirthProb,clearProb)]*numViruses        
        patient = Patient(viruses,maxPop)
        
        timestepSize = [patient.update() for j in range(nTimeSteps)]
        sumTimestep = [x + y for x,y in zip(sumTimestep,timestepSize)]    
        #print sumTimestep
    #timestepSizeArray = numpy.array(timestepSize)
    #timestepSizeArray = timestepSizeArray.reshape((numTrials,300))
    #timestepSizeMean = timestepSizeArray.mean(axis = 0)
    timestepSizeMean = [float(val)/numTrials for val in sumTimestep]
    
    pylab.plot(range(nTimeSteps),timestepSizeMean)
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus population')
    pylab.legend('')
    pylab.show()



#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self,maxBirthProb,clearProb)
        self.resistances = resistances
        self.mutProb = mutProb
        
    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        resistances = self.getResistances()
        if drug in resistances:
            return resistances[drug]
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns 
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        reproducable = True
        for drug in activeDrugs:
            reproducable *= self.isResistantTo(drug)
        #print reproducable
        if not reproducable:
            raise NoChildException()
        else:
            reproduceProb = random.random()
            #print reproduceProb,self.maxBirthProb*(1-popDensity),'Check'
            if reproduceProb < (self.maxBirthProb*(1-popDensity)):
                #if not activeDrugs:
                    #activeDrugs = [drug for drug in self.getResistances()]
                resistances = self.getResistances()
                for drug,resistance in resistances.items():
                    if random.random()<=self.getMutProb():
                        #resistance = self.isResistantTo(drug)
                        if resistance == True:
                            newResistance = False
                        else:
                            newResistance = True                        
                        self.resistances[drug] = newResistance                    
                    else:
                        pass
                                        
                offSpringVirus = ResistantVirus(self.maxBirthProb,self.clearProb,self.resistances,self.mutProb)
                return offSpringVirus
            else:
                raise NoChildException()

            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.postcondition = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.getPrescriptions():
            self.postcondition.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.postcondition


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count = 0
        viruses = self.getViruses()
        for virus in viruses:
            resistance = 1
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    resistance *=1
                else:
                    resistance*=0
            if resistance == 1 and drugResist:
                count += 1
                
        return count
        

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus par ticles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        viruses = self.getViruses()
        newVirus = []
        self.viruses = [virus for virus in viruses if not virus.doesClear()]        

        popDensity = float(self.getTotalPop())/self.getMaxPop()

        for virus in self.viruses:
            try:
                newVirus.append(virus.reproduce(popDensity,self.getPrescriptions()))
            except NoChildException:
                pass       
        self.viruses+=newVirus         

        return self.getTotalPop()

        



#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    nTimeSteps_noDrug = 150
    nTimeSteps_withDrug = 150
    sumTimestep_nodrug_tot = [(0,0)]*nTimeSteps_noDrug
    sumTimestep_withdrug_tot = [(0,0)]*nTimeSteps_withDrug

    for i in range(numTrials):
        result = []
        viruses = [ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)]*numViruses        
        patient = TreatedPatient(viruses,maxPop)
        
        timestepSize_nodrug = [(patient.update(),patient.getResistPop(['guttagonol'])) for j in range(nTimeSteps_noDrug)]
        #print sumTimestep_nodrug_tot
        for ta, tb in zip(sumTimestep_nodrug_tot, timestepSize_nodrug):
            t = tuple(a+b for a,b in zip(ta,tb))
            result.append(t)
        sumTimestep_nodrug_tot = result
        #print timestepSize_nodrug, result
                
        patient.addPrescription('guttagonol')
        
        result = []
        timestepSize_withdrug = [(patient.update(),patient.getResistPop(['guttagonol'])) for j in range(nTimeSteps_withDrug)]      
        for ta, tb in zip(sumTimestep_withdrug_tot, timestepSize_withdrug):
            t = tuple(a+b for a,b in zip(ta,tb))
            result.append(t)
        sumTimestep_withdrug_tot = result    
        
    merge_tot_pop = [x[0] for x in sumTimestep_nodrug_tot] + [x[0] for x in sumTimestep_withdrug_tot]
    merge_tot_pop_mean = [float(val)/numTrials for val in merge_tot_pop]
    
    merge_res_pop = [x[1] for x in sumTimestep_nodrug_tot] + [x[1] for x in sumTimestep_withdrug_tot]
    merge_res_pop_mean = [float(val)/numTrials for val in merge_res_pop]

    pylab.plot(range(nTimeSteps*2),merge_tot_pop_mean,label='Total pop')
    pylab.figure()
    pylab.plot(range(nTimeSteps*2),merge_res_pop_mean,label='Resistance pop')
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus population')
    pylab.legend()
    pylab.show()




#simulationWithoutDrug(100, 1000, 0.1, 0.05, 100)
simulationWithDrug(100, 1000, 0.1, 0.05, {"guttagonol": False}, 0.005, 5)