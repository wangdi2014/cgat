import os, sys, re, types, itertools
import IOTools
from SphinxReport.Tracker import *
from SphinxReport.odict import OrderedDict as odict

##################################################################################
class trackSummary( SingleTableTrackerRows ):
    table = "genelist_stats"

##################################################################################
class orthologyGroupCounts( TrackerSQL ):

    mPattern = "ortholog_groups_with_feature"

    def __call__(self, track, slice = None ):
        statement = '''SELECT species_count , count(set_id) as genes
                       FROM ortholog_groups_with_feature
                       GROUP BY species_count
                       UNION
                       select 0 as species_count, a.groups-b.with_feature as genes from 
                       (select count(distinct set_id) as groups from ortholog_groups) a,
                       (select count(set_id) as with_feature from ortholog_groups_with_feature) b
                       ORDER BY species_count desc;'''
        return self.getAll( statement )

##################################################################################
class conservedGenesAllSpecies( TrackerSQL ):

    mPattern = "ortholog_groups_with_feature"

    def __call__(self, track, slice = None ):
        statement = '''SELECT set_id, gene_names
                       FROM ortholog_groups_with_feature
                       WHERE species_count=6;'''
        return self.getAll( statement )

##################################################################################
class pairwiseHeatmap( Tracker ):

    def getTracks(self):
        return [ "ortholog_pairs_with_feature.matrix", ]
        
    def __call__(self, track, slice = None ):
        fn = "ortholog_pairs_with_feature.matrix"
        if not os.path.exists( fn ): 
            return
            
        x = IOTools.openFile( fn )
        matrix, rownames, colnames = IOTools.readMatrix( x )
        return odict( (('matrix', matrix),
                       ('rows', rownames),
                       ('columns', colnames)) )

##################################################################################
class pairwiseTable( Tracker ):

    def getTracks(self):
        return [ "ortholog_pairs_with_feature.matrix", ]
        
    def __call__(self, track, slice = None ):
        fn = "ortholog_pairs_with_feature.matrix"
        if not os.path.exists( fn ): 
            return
            
        x = open( fn )
        data = odict()
        for line in x:
            temp = line.split()
            name = temp[0]
            scores = temp[1:]
            data[name] = scores
        return data
                       
##################################################################################
class threewayVenn( TrackerSQL ):

    mPattern = "triple_ortholog_stats"

    def __call__(self, track, slice = None ):
        statement = '''SELECT species_list, conserved_nmis
                       FROM triple_ortholog_stats'''
        return self.getAll( statement )
                
