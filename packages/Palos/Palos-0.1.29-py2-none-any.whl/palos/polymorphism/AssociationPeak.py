"""
2012.12.15 data structure for AssociationPeak in PyTablesMatrixFile format 
"""
import sys, os
import csv
import tables
from tables import UInt64Col, Float64Col, StringCol
import numpy
from palos.utils import PassingData, PassingDataList
from palos.ProcessOptions import ProcessOptions
from palos.io.YHPyTables import YHTable, YHFile, castPyTablesRowIntoPassingData

class AssociationPeakTable(tables.IsDescription):
	id = UInt64Col(pos=0)
	chromosome = StringCol(64, pos=1)	#64 byte-long
	start = UInt64Col(pos=2)
	stop = UInt64Col(pos=3)
	start_locus_id = UInt64Col(pos=4)
	stop_locus_id = UInt64Col(pos=5)
	no_of_loci = UInt64Col(pos=6)
	peak_locus_id = UInt64Col(pos=7)
	peak_score = Float64Col(pos=8)

class AssociationPeakTableFile(YHFile):

	"""
	usage examples:
	
		peakFile = AssociationPeakTableFile(self.outputFname, mode='w')
		peakFile.addAttributeDict(attributeDict)
		peakFile.appendAssociationPeak(association_peak_ls=association_peak_ls)
		
		#for read-only
		peakFile = AssociationPeakTableFile(inputFname, mode='r', peakPadding=0)
		rbDict = peakFile.associationPeakRBDict
	"""
	def __init__(self, inputFname=None, mode='r', \
				tableName='association_peak', groupNamePrefix='group', tableNamePrefix='table',\
				filters=None, peakPadding=0, expectedrows=50000, autoRead=True, autoWrite=True, \
				**keywords):
		
		self.peakPadding = peakPadding
		self.associationPeakRBDict = None
		YHFile.__init__(self, path=inputFname, mode=mode, \
				tableName=tableName, groupNamePrefix=groupNamePrefix, tableNamePrefix=tableNamePrefix,\
				rowDefinition=AssociationPeakTable, filters=filters, expectedrows=expectedrows,\
				autoRead=autoRead, autoWrite=autoWrite,\
				debug=0, report=0)
		
		self.associationPeakTable = self.getTableObject(tableName=self.tableName)

	def _readInData(self, tableName=None, tableObject=None):
		"""
		2012.11.12
			similar to Stock_250kDB.constructRBDictFromResultPeak(), but from HDF5MatrixFile-like file
		"""
		YHFile._readInData(self, tableName=tableName, tableObject=tableObject)
		
		from palos.algorithm.RBTree import RBDict
		from palos.polymorphism.CNV import CNVCompare, CNVSegmentBinarySearchTreeKey, get_overlap_ratio
		if tableObject is None:
			tableObject = self.getTableObject(tableName=tableName)
		sys.stderr.write("Constructing association-peak RBDict from HDF5 file %s, (peakPadding=%s) ..."%(self.inputFname, self.peakPadding))
		associationPeakRBDict = RBDict()
		associationPeakRBDict.result_id = None	#2012.6.22
		associationPeakRBDict.peakPadding = self.peakPadding
		associationPeakRBDict.HDF5AttributeNameLs = []
		
		for attributeName, value in self.getAttributes().items():
			associationPeakRBDict.HDF5AttributeNameLs.append(attributeName)
			setattr(associationPeakRBDict, attributeName, value)
		
		counter = 0
		real_counter = 0
		for row in tableObject:
			if not row['chromosome']:	#empty chromosome, which happens when inputFname contains no valid peaks, but the default null peak (only one).
				continue
			counter += 1
			segmentKey = CNVSegmentBinarySearchTreeKey(chromosome=row['chromosome'], \
							span_ls=[max(1, row['start'] - self.peakPadding), row['stop'] + self.peakPadding], \
							min_reciprocal_overlap=1, result_peak_id=None)
							#2010-8-17 overlapping keys are regarded as separate instances as long as they are not identical.
			if segmentKey not in associationPeakRBDict:
				associationPeakRBDict[segmentKey] = []
			else:
				sys.stderr.write("Warning: segmentKey of %s already in associationPeakRBDict with this row: %s.\n"%\
								(row, associationPeakRBDict[segmentKey][0]))
			associationPeakRBDict[segmentKey].append(castPyTablesRowIntoPassingData(row))	#row is a pointer to the current row.
		sys.stderr.write("%s peaks in %s spans.\n"%(counter, len(associationPeakRBDict)))
		
		self.associationPeakRBDict = associationPeakRBDict
		return self.associationPeakRBDict
	
	def appendAssociationPeak(self, association_peak_ls=None):
		"""
		2012.11.20
		"""
		sys.stderr.write("Dumping %s association peaks into %s ..."%(len(association_peak_ls), self.inputFname))
		#each number below is counting bytes, not bits
		cellList = []
		#2012.11.28 sort it
		association_peak_ls.sort()
		for association_peak in association_peak_ls:
			dataTuple = (association_peak.chromosome, association_peak.start, association_peak.stop, \
						association_peak.start_locus_id, association_peak.stop_locus_id, \
						association_peak.no_of_loci,\
						association_peak.peak_locus_id, association_peak.peak_score)
			self.associationPeakTable.writeOneCell(dataTuple)
		self.flush()
		sys.stderr.write(" \n")
	
