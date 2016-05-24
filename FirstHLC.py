from icecube import icetray, dataclasses
from numpy import array, sum
import os

class FirstHLC(icetray.I3ConditionalModule):
    def __init__(self, context):
        icetray.I3ConditionalModule.__init__(self, context)

        self.AddParameter('InputPulseSeries',
                          'Pulse series that will be used for hit search',
                          'OfflinePulses')
        self.AddParameter('Vertex',
                          'Vertex in I3Particle container',
                          'FirstHLCvertex')
        self.AddParameter('EarlySLC',
                          'Name for count of early SLC hits',
                          'EarlySLC_')
        self.AddOutBox('OutBox')

    def Configure(self):
        self.input_pulses = self.GetParameter('InputPulseSeries')
        self.vertex       = self.GetParameter('Vertex')
        self.earlyslc     = self.GetParameter('EarlySLC') + self.input_pulses

    def Physics(self, frame):
        geometry = frame['I3Geometry']

        if not frame.Has(self.input_pulses):
            print 'No pulse series with name: ' + self.input_pulses
            self.PushFrame(frame)
            return True        

        if type(frame[self.input_pulses]) == dataclasses.I3RecoPulseSeriesMap:
            hit_map = frame.Get(self.input_pulses)
        elif type(frame[self.input_pulses]) == dataclasses.I3RecoPulseSeriesMapMask:
            hit_map = frame[self.input_pulses].apply(frame)

        all_times = array([10.E5]*len(hit_map))

        # Find the earliest HLC!
        earliest_om = None
        earliest_time = 10.E9

        for index, one_dom in enumerate(hit_map):
            all_times[index] = one_dom[1][0].time
            for one_hit in one_dom[1]:
                if one_hit.flags & dataclasses.I3RecoPulse.PulseFlags.LC:
                    if one_hit.time < earliest_time:
                        earliest_om = one_dom[0]
                        earliest_time = one_hit.time

                    
        early_hits = dataclasses.I3Double(1.*sum(all_times < earliest_time))


        frame[self.earlyslc]  = early_hits

        myvertex = dataclasses.I3Particle()
        myvertex.pos.x = geometry.omgeo[earliest_om].position.x
        myvertex.pos.y = geometry.omgeo[earliest_om].position.y
        myvertex.pos.z = geometry.omgeo[earliest_om].position.z
        myvertex.time  = earliest_time
        frame[self.vertex] = myvertex

        self.PushFrame(frame)
        return True


 
