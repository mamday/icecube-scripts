from icecube import icetray, dataclasses
from icecube import  santa, gulliver, linefit, jebclasses, tensor_of_inertia, dipolefit, cramer_rao, clast, lilliput

from icecube import gulliver_modules, improvedLinefit
from icecube.lilliput import *

from icecube import santa

from I3Tray import *
import sys, os

sys.path.append('/afs/ifh.de/user/y/yanezjua/i3modules/marius_modules')
sys.path.append('/afs/ifh.de/user/y/yanezjua/i3modules/tools')
sys.path.append('/afs/ifh.de/user/y/yanezjua/i3modules/veto-tools')
sys.path.append('/afs/ifh.de/user/y/yanezjua/i3modules/sebastian_modules')
sys.path.append('/afs/ifh.de/user/y/yanezjua/i3modules/jason_modules')

## Background rejection modules
from level3_DeepCore import DeepCoreCuts
from CorridorCut import CorridorCut
from FirstHLC import FirstHLC
from I3CutL7Module import I3CutL7Module

# Hit series stats module
from EnergyEstimator import NChQtot

# MC modules
from GetNuMu import Muon2Frame
from CorsikaStats import Shower2Muons
from IsCC import IsCC

# Energy estimation modules
from LowEnergySeed import LineFitSantaSeed
from MillipedeRange import RangeFromMillipede

# Miscellaneous
from FilterEvents import AddDCfilterInfo

#####
##### Oscillations wrapper
#####
from CalcWeightsTray import *
from collections import namedtuple
from icecube import  neutrinoflux

DatPart = namedtuple("DatPart", ("zen", "eTrunc", "eMuex", "eMill", "eTrumi"))
SimPart = namedtuple("SimPart", DatPart._fields + ("mcState", "mcType", "zenMC", "eMC", "eMuon", "oscProb"))

# Angles and masses from Fogli et al arXiv:1209.3023v2 (Normal, inverted)
#CalcWeights((1., 7.50e-5,  2.47e-3),         [(1,2,33.3),(1,3,8.6,300),(2,3,40.0)])
#CalcWeights((1., 7.50e-5, -2.43e-3+7.50e-5), [(1,2,33.3),(1,3,8.6,300),(2,3,40.0)])
# Angles and masses from Forero et al arXiv:1205.4018v4 (Normal, inverted)
#CalcWeights((1., 7.62e-5,  2.55e-3),         [(1,2,32.41),(1,3,8.98,144.),(2,3,44.85)])
#CalcWeights((1., 7.62e-5, -2.43e-3),         [(1,2,32.41),(1,3,9.06,-54.),(2,3,44.38)])

OsciInstance    = CalcWeights((1., 7.50e-5,  2.47e-3),         [(1,2,33.3),(1,3,8.6,300),(2,3,40.0)])
OsciInstanceIH  = CalcWeights((1., 7.50e-5, -2.43e-3+7.50e-5), [(1,2,33.3),(1,3,8.6,300),(2,3,40.0)])

def I3NuOscillations(frame):
    mcPrim = frame['I3MCTree'].most_energetic_primary
    
    # Flux overhead
    fluxmodel = 'honda2006'

    oneWeight = frame['I3MCWeightDict']['OneWeight']*icetray.I3Units.GeV*icetray.I3Units.cm2*icetray.I3Units.sr
    nEvents   = frame['I3MCWeightDict']['NEvents']
    norm =  2.*oneWeight/nEvents      
    
    nu_pid    = [66, 68, 133]
    nubar_pid = [67, 69, 134]
    e_pid     = [66,67]
    mu_pid    = [68, 69]
    tau_pid   = [133, 134]
    
    if mcPrim.type.real in nu_pid:
        numu_particle  = dataclasses.I3Particle.ParticleType.NuMu
        nue_particle   = dataclasses.I3Particle.ParticleType.NuE
        nutau_particle = dataclasses.I3Particle.ParticleType.NuTau
        mcType = 1
    elif mcPrim.type.real in nubar_pid:         
        numu_particle  = dataclasses.I3Particle.ParticleType.NuMuBar
        nue_particle   = dataclasses.I3Particle.ParticleType.NuEBar
        nutau_particle = dataclasses.I3Particle.ParticleType.NuTauBar		
        mcType = -1
    else:
        print 'ERROR, what did you give as input?'
        exit()
        
    atmFlux_mu  = neutrinoflux.ConventionalNeutrinoFlux(fluxmodel + '_numu')
    numu_flux   = atmFlux_mu.getFlux(numu_particle, mcPrim.energy, cos(mcPrim.dir.theta))/(icetray.I3Units.GeV*icetray.I3Units.cm2*icetray.I3Units.s*icetray.I3Units.sr)
    atmFlux_e   = neutrinoflux.ConventionalNeutrinoFlux(fluxmodel + '_nue')
    nue_flux    = atmFlux_e.getFlux(nue_particle, mcPrim.energy, cos(mcPrim.dir.theta))/(icetray.I3Units.GeV*icetray.I3Units.cm2*icetray.I3Units.s*icetray.I3Units.sr)
    nutau_flux  = 0
    
    mcState     = [sqrt(nue_flux),sqrt(numu_flux),sqrt(nutau_flux)]
    
    # Actual calculation NH & IH
    p = SimPart(0.,0.,0.,0.,0., 
                mcState , mcType, mcPrim.dir.zenith,mcPrim.energy,0., -1.)
    pList = OsciInstance.CalcWeightPart([p])
    pListIH = OsciInstanceIH.CalcWeightPart([p])

    # Picking up the value for the MC type
    if mcPrim.type.real in e_pid:
        osc_index = 0
    elif mcPrim.type.real in mu_pid:
        osc_index = 1
    elif mcPrim.type.real in tau_pid:
        osc_index = 2
    else:
        print 'ERROR, what did you give as input?'
        exit()          
        
    frame.Put("AtmoFlux", dataclasses.I3Double(pList[0].oscProb[osc_index] * norm))
    frame.Put("AtmoFlux_IH", dataclasses.I3Double(pListIH[0].oscProb[osc_index]*norm))
    frame.Put("AtmoFlux_NoOsc", dataclasses.I3Double(norm * mcState[osc_index]**2))
    return True
#####


@icetray.traysegment
def Level3_JP( tray, name,
               If           = lambda f: True,
               base_pulses  = 'OfflinePulses',
               srt_pulses   = 'SRTTWOfflinePulsesDC',
               twc_pulses   = 'TWOfflinePulsesDC',
               santa_pulses = 'SANTA_DirectPulses',
               spe_fit      = 'SPEFit2_DC',
               linefit      = 'LineFit_DC',
               filtername   = 'DeepCoreFilter_11',
               datatype     = '',
               ):
    

    tray.AddModule(AddDCfilterInfo, 'adding_filter_info',
                   FilterTag = filtername
                   )

    ##############################
    ##############################
    ## Official L3
    ##############################
    ##############################    
    
    tray.AddSegment(DeepCoreCuts, 'DCcuts',
                    If = If)
    
    ##############################
    ##############################
    ## Check if some reconstructions are in the frame
    ##############################
    ##############################
    
    def SANTAinFrame(frame):
        if frame.Has('SANTA_FitResultsZenith') or frame.Has('SANTA_FitResultsZenith_MS'):
            return True
        else:
            return False


    ##############################
    ##############################
    ## MC information
    ##############################
    ##############################

    tray.AddModule(Shower2Muons,'CORSIKA',
                   If = If)
    tray.AddModule(IsCC, 'IsChargedCurrent',
                   If = If)
    tray.AddModule(Muon2Frame, 'getMuons',
                   If = If)

    ## Neutrino flux and oscillations from Marius
    if datatype == 'nu':
        ###
        # Marius' modules
        ###
        tray.AddModule(I3NuOscillations, "MariusOscillations")


    ##############################
    ##############################
    ## JP reconstruction and event selection
    ##############################
    ##############################


    ## Containment
    tray.AddModule(FirstHLC, 'FirstHLCmodule',
                   InputPulseSeries = srt_pulses,
                   If = If
                   )

    # NCh / Nstr / Qtot counters
    # HLCs
    tray.AddModule(NChQtot, 'SimpleEnergyEstimators_HLC_OfflinePulses',
                   InputPulseSeries = base_pulses,
                   NChOutput        = 'HLC_NCh_',
                   QOutput          = 'HLC_Qtot_',
                   NStringOutput    = 'HLC_NStr_',
                   HLConly          = True,
                   If               = If
                   )

    tray.AddModule(NChQtot, 'SimpleEnergyEstimators_DCHLC_OfflinePulses',
                   InputPulseSeries = base_pulses,
                   NChOutput        = 'HLC_DC_NCh_',
                   QOutput          = 'HLC_DC_Qtot_',
                   NStringOutput    = 'HLC_DC_NStr_',
                   Volume           = 'Reduced_DC',
                   HLConly          = True,
                   If               = If
                   )
    # SRT
    tray.AddModule(NChQtot, 'SimpleEnergyEstimators_SRT',
                   InputPulseSeries = srt_pulses,
                   If = If
                   )

    tray.AddModule(NChQtot, 'SimpleEnergyEstimators_DCSRT',
                   InputPulseSeries = base_pulses,
                   NChOutput        = 'DC_NCh_',
                   QOutput          = 'DC_Qtot_',
                   NStringOutput    = 'DC_NStr_',
                   Volume           = 'Reduced_DC',
                   If               = If
                   )


    # SANTA reconstruction
    tray.AddSegment(santa.SANTA_segment, 'SANTA_standard',
                    InputPulseSeries  = base_pulses,
                    OutputPulseSeries = santa_pulses,
                    LoopLevels        = 5.,
                    AmplitudeCut_HS   = 1.,
                    TimeDelay         = 20. * icetray.I3Units.ns,
                    DC_only           = False,
                    LFname            = 'LineFit_SANTA',
                    FitResultsZenith  = 'SANTA_FitResultsZenith',
                    FitResultsCascade = 'SANTA_FitResultsCascade',
                    Interactive       = False,
                    Debugging         = False,
                    santa_suffix      = '',     # Use if the fit is done more than once,
                    StrongFitQuality  = False,
                    If                = If
                    )

    # SANTA length
    tray.AddModule(santa.SANTA_SimpleRangeFit, 'SANTA_fit1',
                   InputPulseSeries = santa_pulses,
                   ZenithFit        = 'SANTA_FitResultsZenith'
                   )
                   
    tray.AddModule(santa.SANTA_SimpleRangeFit, 'SANTA_fit2',
                   InputPulseSeries = santa_pulses,
                   ZenithFit        = 'SANTA_FitResultsZenith_MS'
                   )

    tray.AddModule(santa.SANTA_RangeFit, 'SANTA_fit3',
                   InputPulseSeries = santa_pulses,
                   ZenithFit        = 'SANTA_FitResultsZenith'
                   )


    tray.AddModule(NChQtot, 'SimpleEnergyEstimators_SANTA',
                   InputPulseSeries = santa_pulses,
                   If = If
                   )    

    
    # Corridor cut
    tray.AddModule(CorridorCut, 'MyCorridor',
                   InputPulseSeries = base_pulses,
                   SANTAFit         = 'SANTA_FitResultsZenith',
                   If               = If
                   )

    ## Sebastian's L7
    tray.AddModule(I3CutL7Module, 'L7_Euler',
                   If = If)



    return True




    # This part so far is doing NOTHING
    '''
    tray.AddModule(SANTA_ExpandDirectPulses, 'expanding',
                   SANTAPulseSeries = 'SANTA_DirectPulses'+santa_index,
                   OutputPulseSeries = 'SANTA_DirectPulsesExpanded',
                   If = If)

    tray.AddModule("I3LineFit", "LineFit_SANTA_Expanded")(
        ("InputRecoPulses",     'SANTA_DirectPulsesExpanded'),
        ("LeadingEdge",         "FLE"),
        ("Name",                "LineFit_SANTA_Expanded"),
        ('If', If)
        )
    '''

    '''
    # Creating the SEED FOR SPE. The seed is either the MultiString fit or the combination of SANTA and LineFit
    tray.AddModule(LineFitSantaSeed, 'CreateTheSeed')(
        ('MultiStringFit', 'SANTA_Meike_zenith_MS'),
        ('ParticleReco',  'LineFit_SANTA'),
        ('SANTAreco'   ,  'SANTA_Meike_zenith'),
        ('OutputSeedName', 'MixedSeed'),
        ('If', If)
        )

    #--------------------------------------------------
    # Services to Peform Track Reconstructions
    #--------------------------------------------------

    # Simple Parameterization
    tray.AddService("I3SimpleParametrizationFactory", "SimpleTrack2")(
        ("StepX",          20 * I3Units.m),                         # ! Set to 1/50 the size of the detector
        ("StepY",          20 * I3Units.m),                         # ! Set to 1/50 the size of the detector
        ("StepZ",          20 * I3Units.m),                         # ! Set to 1/50 the size of the detector
        ("StepZenith",     0.1 * I3Units.radian),                   # ! Set to 1/30 the size of the detector
        ("StepAzimuth",    0.2 * I3Units.radian),                   # ! Set to 1/30 the size of the detector
        ("BoundsX",        [-2000*I3Units.m, +2000*I3Units.m ]),    # ! Set bounds to twice the size of the detector
        ("BoundsY",        [-2000*I3Units.m, +2000*I3Units.m ]),    # ! Set bounds to twice the size of the detector
        ("BoundsZ",        [-2000*I3Units.m, +2000*I3Units.m ]),    # ! Set bounds to twice the size of the detector
        )

    # Gulliver Minimization Service
    tray.AddService("I3GulliverMinuitFactory", "Minuit2")(
        ("MaxIterations",  1000),     # ! Only need 1000 iterations
        ("Tolerance",      0.01),     # ! Set tolerance to 0.01
        )

    # Pandel Service for SPE1
    tray.AddService("I3GulliverIPDFPandelFactory", "SPEPandel2")(
        ("InputReadout",        'SANTA_DirectPulses'),              # ! Use pulses given to this function as arg
        #("NoiseProbability",    noiserate*I3Units.hertz),   # ! Added a little noise term (prob/ns)
        )

    # Seed Service using Linefit
    tray.AddService("I3BasicSeedServiceFactory", "LineFitSeed2")(
        ("InputReadout",        'SANTA_DirectPulses'),              # ! Use pulses given to this function as arg
        ("FirstGuesses",        [ "MixedSeed" ]),           # ! Use LineFit
        ("TimeShiftType",       "TFirst"),                  # ! Use TFirst for vertex correction
        )

    # SPE4
    tray.AddModule("I3IterativeFitter", "MillipedeTrackSeed")(
        ("LogLikelihood",       "SPEPandel2"),        # ! Name of likelihood service
        ("Minimizer",           "Minuit2"),           # ! Name of minimizer service
        ("NIterations",         2),                         # ! Only run 4 iterations (32 default)
        ("Parametrization",     "SimpleTrack2"),      # ! Name of track parametrization service
        ("RandomService",       "SOBOL"),                   # ! Name of randomizer service
        ("SeedService",         "LineFitSeed2"), # ! Name of seed service
        ('If', If)
        )
    '''
