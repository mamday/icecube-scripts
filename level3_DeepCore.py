from icecube import dataclasses
from icecube import icetray
from icecube.icetray import I3Units
from icecube import NoiseEngine
from icecube import DomTools 
from icecube import improvedLinefit
from icecube.DeepCore_Filter import DOMS
from icecube import SeededRTCleaning
from icecube import STTools
from icecube.STTools.seededRT.configuration_services import I3ClassicSeededRTConfigurationService

##############################
# Set up the service to behave as it did from the
# orignal SeededRTCleaning module
##############################

@icetray.traysegment
def DeepCoreCuts( tray, name, filterEvent=True, If = lambda f: True
                  ):

    # ##############################
    # These are defined from the level2_globals.py file
    # found in std-processing/ project. Explanation of
    # the SeededRT seed methods can be found at
    # http://wiki.icecube.wisc.edu/index.php/SLC_hit_cleaning
    #
    # TWOfflinePulsesDC: -4000ns to +5000ns
    # SRTTWOfflinePulsesDC: TW cleaned, R=150m, T=1000ns, max. iter. = 3, HLCcore, Threshold = 2
    # ##############################

    Pulses = "SRTTWOfflinePulsesDC"

    def PassedDCFilter(frame):
        if frame.Has("FilterMask"):
            if frame["FilterMask"].get("DeepCoreFilter_11").condition_passed:
                return True
            # end if()
        # end if()
        return False
    # end PassedDCFilter()
    
    tray.AddModule( PassedDCFilter, "DCCheck")

    
    def HasDCPulses(frame):
        if frame.Has("TWOfflinePulsesDC") and frame.Has("SRTTWOfflinePulsesDC"):
            return True
        else:
            return False
        # end if()
    # end HasDCPulses()

    tray.AddModule( HasDCPulses, "Check_DCPulses")

    
#    tray.AddSegment( NoiseEngine.WithCleaners, "NoiseEnginess",
#                     HitSeriesName = "OfflinePulses",
#                     )

    # #############################
    # The goal here is to reduce the noise events by looking
    # for events which have tightly time correlated hits in the
    # DC Fiducial volume.
    # #############################

    DOMList = DOMS.DOMS( "IC86EDC")
    
    tray.AddModule( "I3OMSelection<I3RecoPulseSeries>", "GenDCCFidPulses",
                    selectInverse  = True,
                    InputResponse  = "TWOfflinePulsesDC",
                    OutputResponse = "TWOfflinePulsesDCFid",
                    OmittedKeys    = DOMList.DeepCoreFiducialDOMs
                    )

    # #############################
    # Run the DCVeto using pulses instead
    # of launches. The IC2011 online veto
    # used DOMLaunches.
    # #############################

    tray.AddModule( "I3OMSelection<I3RecoPulseSeries>", "GenDCCFidPulses_0",
                    selectInverse     = True,
                    InputResponse     = "OfflinePulses",
                    OutputResponse    = "OfflinePulsesDCFid",
                    OutputOMSelection = "BadOM_DCFid_0",
                    OmittedKeys       = DOMList.DeepCoreFiducialDOMs
                    )

    tray.AddModule( "I3OMSelection<I3RecoPulseSeries>", "GenICVetoPulses_0",
                    selectInverse     = False,
                    InputResponse     = "OfflinePulses",
                    OutputResponse    = "OfflinePulsesICVeto",
                    OutputOMSelection = "BadOM_ICVeto_0",
                    OmittedKeys       = DOMList.DeepCoreFiducialDOMs
                    )

    tray.AddModule("I3DeepCoreVeto<I3RecoPulse>", "deepcore_filter_pulses",
                   InputFiducialHitSeries = "OfflinePulsesDCFid",
                   InputVetoHitSeries     = "OfflinePulsesICVeto",
                   DecisionName           = "DCFilterPulses",
                   MinHitsToVeto          = 2,
                   VetoChargeName         = "DCFilterPulses_VetoPE",
                   VetoHitsName           = "DCFilterPulses_VetoHits",
                   )

    # #############################
    # Runs an X microsecond dynamic time window cleaning over the
    # StaticTW cleaned recopulses in the DeepCore
    # fiducial region.
    # #############################

    tray.AddModule( "I3TimeWindowCleaning<I3RecoPulse>", "DynamicTimeWindow175", 
                    InputResponse  = "TWOfflinePulsesDCFid",
                    OutputResponse = "DCFidPulses_DTW175", 
                    TimeWindow     = 175,
                    )

    tray.AddModule( "I3TimeWindowCleaning<I3RecoPulse>", "DynamicTimeWindow200", 
                    InputResponse  = "TWOfflinePulsesDCFid",
                    OutputResponse = "DCFidPulses_DTW200", 
                    TimeWindow     = 200,
                    )

    tray.AddModule( "I3TimeWindowCleaning<I3RecoPulse>", "DynamicTimeWindow250", 
                    InputResponse  = "TWOfflinePulsesDCFid",
                    OutputResponse = "DCFidPulses_DTW250", 
                    TimeWindow     = 250,
                    )

    tray.AddModule( "I3TimeWindowCleaning<I3RecoPulse>", "DynamicTimeWindow300", 
                    InputResponse  = "TWOfflinePulsesDCFid",
                    OutputResponse = "DCFidPulses_DTW300", 
                    TimeWindow     = 300,
                    )

    # #############################
    # Put all the MicroCount variables
    # into a map for elegance
    # #############################

    def MicroCount(frame):

        MicroValuesHits = dataclasses.I3MapStringInt()
        MicroValuesPE   = dataclasses.I3MapStringDouble()

        DTWs = ["DTW175","DTW200", "DTW250", "DTW300"]
        for DTW in DTWs:
            totalCharge = 0
            if not frame.Has("DCFidPulses_" + DTW):
                MicroValuesHits["STW9000_" + DTW] = icetray.I3Int(0)
                MicroValuesPE["STW9000_" + DTW] = dataclasses.I3Double( totalCharge)
                continue
            # end if()
            
            for omkey in frame["DCFidPulses_" + DTW].apply(frame):
                for pulse in omkey[1]:
                    totalCharge += pulse.charge
                # end for()
            # end for()
            MicroValuesHits["STW9000_" + DTW] = len(frame["DCFidPulses_" + DTW].apply(frame))
            MicroValuesPE["STW9000_" + DTW] = totalCharge
        # end for()
        frame["MicroCountHits"] = MicroValuesHits
        frame["MicroCountPE"] = MicroValuesPE
        return
    # end MicroCount()

    # #############################
    # Add the MicroCount MapStringDouble object to the frame
    # #############################

    tray.AddModule( MicroCount, "MicroCount")

    # ##############################
    # Rewrite the QR_Box method from the
    # slc-veto project into python so I don't
    # have to faff about with a code review.
    # ##############################

    def CalculateC2QR6AndFirstHitVertexZ( frame, PulseSeries):

        totalCharge = 0
        timeCharge  = {}
        timeOMKey   = {}

        geometry = frame[ "I3Geometry"]
        vertexZ = -999
        firstHitTime = 1e6
        
        
        for omkey in frame[ PulseSeries].apply(frame):            
            for pulse in omkey[1]:
                timeCharge[pulse.time] = pulse.charge
                timeOMKey[pulse.time]  = omkey[0]
                totalCharge += pulse.charge
                if pulse.time < firstHitTime:
                    firstHitTime = pulse.time
                    vertexZ = geometry.omgeo[ omkey[0]].position.z
                # end if()                    
            # end for()
        # end for()

        frame[ "VertexGuessZ"] = dataclasses.I3Double( vertexZ)
        
        orderedTimeCharge = sorted(timeCharge.items())
        orderedTimeOMKey  = sorted(timeOMKey.items())
                
        redTimeCharge = orderedTimeCharge[2:]

        # Check to see whether there is at least one pulse
        # in the cleaned dataset. Normally this condition is
        # impossible to not satisfy,
        # but isolated HLC hits change the game.
        
        if len( redTimeCharge) < 1:
            print " In the limit that zero/zero goes to large zero in the \n denominator, C2QR6 will be zero."
            frame["C2QR6"] = dataclasses.I3Double(0)
            return
        # end if()
        
        totalCharge2 = 0
        C2QR6        = 0
        startTime    = redTimeCharge[0][0]
        
        for time, charge in redTimeCharge:
            if (time - startTime) < 600:
                C2QR6 += charge
            # end if()
            totalCharge2 += charge
        # end for()

        C2QR6 = C2QR6/totalCharge2

        if C2QR6 > 0:
            frame["C2QR6"] = dataclasses.I3Double(C2QR6)
        else:                
            print frame["I3EventHeader"].event_id + " has somehow received a negative value of C2QR6"
            print " value is :", C2QR6
            return
        # end if()

        return
    # end CalculateC2QR6AndFirstHitVertexZ

    # #############################
    # Actually add the C2QR6 and
    # position of the first hit from the cleaned
    # pulse series to the frame
    # ##############################

    tray.AddModule( CalculateC2QR6AndFirstHitVertexZ, "CalcC2QR6AndFirstHitVertexZ", PulseSeries = Pulses)

    # ##############################
    # Rewrite the NAbove method from the
    # slc-veto project into python so I don't
    # have to faff about with a code review.
    # ##############################

    def CalculateNAbove200( frame, PulseSeries, ConfigID):

        # Loop over all the triggers looking
        # for the times of all the selected triggers
        
        triggerTimes = []
        for trigger in frame[ "I3TriggerHierarchy"]:
            if trigger.key.config_id == ConfigID:
                triggerTimes.append( trigger.time)
            # end if()
        # end for()

        # Check that there is at least one of the
        # selected triggers.
        
        if len(triggerTimes) == 0:
            frame[ "NAbove200"] = icetray.I3Int( 0)
            return
        # end if()

        triggerTimes.sort()
        earliestTriggerTime = triggerTimes[0]

        chargeCounter = 0        
        geometry = frame[ "I3Geometry"]
        
        for omkey in frame[ PulseSeries]:
            if not geometry.omgeo[ omkey[0]].position.z > -200 * I3Units.m:
                continue
            # end if()
            for pulse in omkey[1]:
                if (pulse.time - earliestTriggerTime) < 0 and (pulse.time - earliestTriggerTime) > -2000:
                    chargeCounter += pulse.charge
                # end if()
            # end for()            
        # end for()

        frame[ "NAbove200"] = dataclasses.I3Double( chargeCounter)

        return
    # end CalculateNAbove200()
    
    # #############################
    # Actually add the NAbove200 variable
    # to the frame
    # ##############################

    tray.AddModule( CalculateNAbove200, "CalcNAbove200",
                    PulseSeries = "OfflinePulses",
                    ConfigID    = 1011)

    # #############################
    # Jacob Daughhetee has shown that a ratio of 
    # SRT cleaned hits within DC to outside of 
    # DC can be a good bkg identifier as well.
    # Run the standard L2 SRT cleaning.
    # #############################


    tray.AddModule( "I3OMSelection<I3RecoPulseSeries>", "GenDCCFidSRTPulses",
                    selectInverse     = True,
                    InputResponse     = Pulses,
                    OutputResponse    = "SRTTWOfflinePulsesDCFid",
                    OutputOMSelection = "BadOM1",
                    OmittedKeys       = DOMList.DeepCoreFiducialDOMs
                    )

    tray.AddModule( "I3OMSelection<I3RecoPulseSeries>", "GenICVetoSRTPulses",
                    selectInverse     = False,
                    InputResponse     = Pulses,
                    OutputResponse    = "SRTTWOfflinePulsesICVeto",
                    OutputOMSelection = "BadOM2",
                    OmittedKeys       = DOMList.DeepCoreFiducialDOMs
                    )

    # ##############################
    # Suggestion by the WIMP group to
    # look at the RT cluster size of pulses
    # in the IC Veto region
    # ##############################

    tray.AddModule( "I3StaticTWC<I3RecoPulseSeries>", "TWRTVetoPulses",
                    InputResponse    = "OfflinePulses",
                    OutputResponse   = "TWRTVetoSeries",
                    TriggerConfigIDs = [1011],
                    TriggerName      = "I3TriggerHierarchy",
                    WindowMinus      = 5000,               
                    WindowPlus       = 0,
                    )                    
    
    tray.AddModule( "I3OMSelection<I3RecoPulseSeries>", "GenRTVetoPulses",
                    selectInverse     = False,
                    InputResponse     = "TWRTVetoSeries",
                    OutputResponse    = "TWRTVetoSeries_ICVeto",
                    OutputOMSelection = "BadOM3",
                    OmittedKeys       = DOMList.DeepCoreFiducialDOMs
                    )

    classicSeededRTConfigService = I3ClassicSeededRTConfigurationService(
        useDustlayerCorrection  = False,
        dustlayerUpperZBoundary = 0*I3Units.m,
        dustlayerLowerZBoundary = -150*I3Units.m,
        icecubeRTTime           = 1000*I3Units.ns,
        icecubeRTRadius         = 250*I3Units.m
        )

    tray.AddModule("I3RTVeto_RecoPulse_Module", "RTVeto250",
                   STConfigService         = classicSeededRTConfigService,
                   InputHitSeriesMapName   = "TWRTVetoSeries_ICVeto",
                   OutputHitSeriesMapName  = "RTVetoSeries250",
                   Streams                 = [icetray.I3Frame.Physics]
                   )




    def CountRTVetoSeriesNChannel( frame):
        totalCharge = 0
        if frame.Has("RTVetoSeries250"):    
            for omkey in frame["RTVetoSeries250"]:
                for pulse in omkey[1]:
                    totalCharge += pulse.charge
                # end for()
            # end for()
        # end if()
        frame["RTVetoSeries250PE"] = dataclasses.I3Double( totalCharge)
        return
    # end CountRTVetoSeriesNChannel()


    tray.AddModule( CountRTVetoSeriesNChannel, "CountRTVetoSeries")

    # ##############################
    # Create a variable that gets pushed
    # to the frame that checks whether
    # the event passed the IC2011 LE L3
    # straight cuts and cleaning.
    # ##############################

    def passIC2011_LE_L3(frame):
        IC2011_LE_L3_FrameObjects = [ "DCFilterPulses_VetoPE",
                                      "MicroCountHits",
                                      "MicroCountPE",
                                      "NAbove200",
                                      "NoiseEngine_S3bool",
                                      "C2QR6",
                                      "RTVetoSeries250PE",
                                      "SRTTWOfflinePulsesDCFid",
                                      "SRTTWOfflinePulsesICVeto",
                                      "VertexGuessZ"
                                      ]

        frameObjects = frame.keys()
        matchingFrameObjects =  set(IC2011_LE_L3_FrameObjects).intersection( set(frameObjects))
        
        if len(matchingFrameObjects) == 10 and len(frame["SRTTWOfflinePulsesDCFid"]) > 0:

            # Count the number of SRT cleaned PEs in the DeepCore fiducial and
            # IceCube Veto region for use in the Ratio Cut variable. Also,
            # count the number of PE for hits satisying the DeepCore Filter
            # `speed of light' criteria.

            totalChargeFiducial = 0
            totalChargeVeto     = 0

            for omkey in frame["SRTTWOfflinePulsesDCFid"]:
                for pulse in omkey[1]:
                    totalChargeFiducial += pulse.charge
                # end for()
            # end for()
            for omkey in frame["SRTTWOfflinePulsesICVeto"]:
                for pulse in omkey[1]:
                    totalChargeVeto += pulse.charge
                # end for()
            # end for()

            LE_L3_Vars = dataclasses.I3MapStringDouble()
            LE_L3_Vars["NoiseEngine"]        = frame["NoiseEngine_S3bool"].value
            LE_L3_Vars["STW9000_DTW175PE"]   = frame["MicroCountPE"].get("STW9000_DTW175")
            LE_L3_Vars["STW9000_DTW200PE"]   = frame["MicroCountPE"].get("STW9000_DTW200")
            LE_L3_Vars["STW9000_DTW250PE"]   = frame["MicroCountPE"].get("STW9000_DTW250")
            LE_L3_Vars["STW9000_DTW300PE"]   = frame["MicroCountPE"].get("STW9000_DTW300")
            LE_L3_Vars["STW9000_DTW175Hits"] = frame["MicroCountHits"].get("STW9000_DTW175")
            LE_L3_Vars["STW9000_DTW200Hits"] = frame["MicroCountHits"].get("STW9000_DTW200")
            LE_L3_Vars["STW9000_DTW250Hits"] = frame["MicroCountHits"].get("STW9000_DTW250")
            LE_L3_Vars["STW9000_DTW300Hits"] = frame["MicroCountHits"].get("STW9000_DTW300")
            LE_L3_Vars["C2QR6"]              = frame["C2QR6"].value
            LE_L3_Vars["NAbove200PE"]        = frame["NAbove200"].value
            LE_L3_Vars["DCFiducialPE"]       = totalChargeFiducial
            LE_L3_Vars["ICVetoPE"]           = totalChargeVeto
            LE_L3_Vars["CausalVetoPE"]       = frame["DCFilterPulses_VetoPE"].value
            LE_L3_Vars["CausalVetoHits"]     = frame["DCFilterPulses_VetoHits"].value
            LE_L3_Vars["VertexGuessZ"]       = frame["VertexGuessZ"].value
            LE_L3_Vars["RTVeto250PE"]        = frame["RTVetoSeries250PE"].value

            frame["IC2011_LE_L3_Vars"] = LE_L3_Vars

            if frame["NoiseEngine_S3bool"].value and frame["MicroCountHits"].get("STW9000_DTW300") > 2 and frame["MicroCountPE"].get("STW9000_DTW300") > 2 and \
            frame["C2QR6"].value > 0.4 and frame["NAbove200"].value < 12 and totalChargeVeto*1.0/totalChargeFiducial < 1.5 and frame["VertexGuessZ"].value < -120 and \
            frame["DCFilterPulses_VetoPE"].value < 7.0 and ( (frame["RTVetoSeries250PE"].value < 4.0 and LE_L3_Vars["DCFiducialPE"] < 100) or \
            (frame["RTVetoSeries250PE"].value < 6.0 and LE_L3_Vars["DCFiducialPE"] >= 100 and LE_L3_Vars["DCFiducialPE"] < 150) or \
            (frame["RTVetoSeries250PE"].value < 10.0 and LE_L3_Vars["DCFiducialPE"] >= 150 and LE_L3_Vars["DCFiducialPE"] < 200) or (LE_L3_Vars["DCFiducialPE"] >= 200) ):
                frame["IC2011_LE_L3"] = icetray.I3Bool(True)
                return
            # end if()
        # end if()
        frame["IC2011_LE_L3"]  = icetray.I3Bool(False)
        return 
        
    # end def passIC2011_LE_L3()

    tray.AddModule( passIC2011_LE_L3, "LE_L3_pass")

    # ##############################
    # Remove the events
    # ##############################
    
    def Filterizer( frame):
        if frame.Has("IC2011_LE_L3"):
            if ( frame["IC2011_LE_L3"].value==1) :
                return True
        return False

    if filterEvent :
        tray.AddModule(Filterizer,"FilterL3")


    # #############################
    # Remove all the bad omselections created when
    # producing the MicroCount outputs
    # #############################

    tray.AddModule("Delete", "delete_badomselection",
                   Keys = ["BadOMSelection",
                           "BadOM1",
                           "BadOM2",
                           "BadOM3",
                           "BadOM_DCFid_0",
                           "BadOM_ICVeto_0",
                           "DCFidPulses_DTW175",
                           "DCFidPulses_DTW200",
                           "DCFidPulses_DTW250",
                           "DCFidPulses_DTW300",
                           ]
                   )


    return
