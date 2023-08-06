#!/usr/bin/env python3
"""
Description:
    A test for AbstractVCFWorkflow

Examples:
    #2013.07.31 
    %s -I LiftPolymorphismCoordinates/folderReduceLiftOverVCF/
        -H -C 1 -j hcondor -l hcondor
        -D /u/home/p/polyacti/NetworkData/vervet/db/ -t /u/home/p/polyacti/NetworkData/vervet/db/
        -o dags/SameSiteConcordance/Method109_vs_3488_BWA_F99.sameSiteConcordance.xml
        --notToUseDBToInferVCFNoOfLoci
        --db_user yh -z localhost
"""
import sys, os, math
__doc__ = __doc__%(sys.argv[0])

from pegaflow.DAX3 import Executable, File, PFN
import pegaflow
from palos import ProcessOptions, PassingData
from palos.io.FastaFile import FastaFile
from . AbstractVCFWorkflow import AbstractVCFWorkflow

ParentClass = AbstractVCFWorkflow

class TestMapReduceVCFWorkflow(ParentClass):
    __doc__ = __doc__
    option_default_dict = ParentClass.option_default_dict.copy()
    #2012.9.25 no overlap and make the interval a lot smaller, (for VCF file)
    option_default_dict[('intervalOverlapSize', 1, int)][0] = 3
    option_default_dict[('intervalSize', 1, int)][0] = 10000
    option_default_dict[('max_walltime', 1, int)][0] = 1300	#under 23 hours
    
    def __init__(self,  **keywords):
        """
        """
        self.needSplitChrIntervalData = False
        ParentClass.__init__(self, **keywords)
        self.needSplitChrIntervalData = False
        
    def preReduce(self, outputDirPrefix="", passingData=None, transferOutput=True, **keywords):
        """
        """
        returnData = ParentClass.preReduce(self, outputDirPrefix=outputDirPrefix,\
            passingData=passingData, transferOutput=transferOutput, **keywords)
        
        self.statDirJob = self.addMkDirJob(outputDir="%sStat"%(outputDirPrefix))
        self.reduceStatDirJob = self.addMkDirJob(outputDir="%sReduceStat"%(outputDirPrefix))
        self.reduceEachVCFDirJob = self.addMkDirJob(outputDir="%sReduceEachVCF"%(outputDirPrefix))
        return returnData
    
    def mapEachInterval(self,
        VCFJobData=None, passingData=None, transferOutput=False, **keywords):
        """
        use VCFJobData
        
        #. extract flanking sequences from the input VCF (ref sequence file => contig ref sequence)
        #. blast them
        #. run FindSNPPositionOnNewRefFromFlankingBlastOutput.py
            #. where hit length match query length, and no of mismatches <=2 => good => infer new coordinates
        #. output a mapping file between old SNP and new SNP coordinates.
            #. reduce this thing by combining everything
        #. make a new VCF file based on the input split VCF file
            #. (replace contig ID , position with the new one's, remove the header part regarding chromosomes or replace it)
        """
        
        returnData = PassingData(no_of_jobs = 0)
        returnData.jobDataLs = []

        topOutputDirJob = passingData.topOutputDirJob
        mapDirJob = passingData.mapDirJob
        reduceOutputDirJob = passingData.reduceOutputDirJob
        
        intervalFileBasenamePrefix = passingData.intervalFileBasenamePrefix
        jobData = passingData.jobData
        VCFFile = VCFJobData.file
        
        splitVCFJob = passingData.mapEachVCFData.splitVCFJob
        chromosome = passingData.chromosome
        
        # a flanking sequence extraction job
        #noOfIndividuals
        realInputVolume = passingData.noOfIndividuals * passingData.span
        baseInputVolume = 600*2000	#600 individuals at 2000 sites
        #base is 200 individual X 2Mb region => 120 minutes
        walltime = self.scaleJobWalltimeOrMemoryBasedOnInput(
            realInputVolume=realInputVolume,
            baseInputVolume=baseInputVolume, baseJobPropertyValue=60,
            minJobPropertyValue=60, maxJobPropertyValue=1200).value
        #base is 4X, => 5000M
        job_max_memory = self.scaleJobWalltimeOrMemoryBasedOnInput(
            realInputVolume=realInputVolume,
            baseInputVolume=baseInputVolume, baseJobPropertyValue=4000,
            minJobPropertyValue=4000, maxJobPropertyValue=8000).value
        
        outputFnamePrefix = os.path.join(mapDirJob.output,
            '%s.sameSite.concordance'%(intervalFileBasenamePrefix))
        outputFile = File('%s.tsv'%(outputFnamePrefix))
        
        returnData.mapJob = self.addAbstractMapperLikeJob(
            executable=self.CalculateSameSiteConcordanceInVCF,
            inputF=VCFFile, outputF=outputFile,
            parentJobLs=[mapDirJob]+VCFJobData.jobLs,
            transferOutput=transferOutput,
            job_max_memory=job_max_memory,
            walltime=walltime)
        
        return returnData
    
    def reduceEachVCF(self, chromosome=None, passingData=None,
        mapEachIntervalDataLs=None,
        transferOutput=True, **keywords):
        """
        #. concatenate all the sub-VCFs into one
        """
        returnData = PassingData(no_of_jobs = 0)
        returnData.jobDataLs = []
        returnData.mapEachIntervalDataLs = mapEachIntervalDataLs
        
        #intervalJobLs = [pdata for pdata in mapEachIntervalDataLs]
        
        realInputVolume = passingData.jobData.file.noOfIndividuals * passingData.jobData.file.noOfLoci
        baseInputVolume = 200*20000
        walltime = self.scaleJobWalltimeOrMemoryBasedOnInput(
            realInputVolume=realInputVolume, \
            baseInputVolume=baseInputVolume, baseJobPropertyValue=60,
            minJobPropertyValue=60, maxJobPropertyValue=500).value
        job_max_memory = self.scaleJobWalltimeOrMemoryBasedOnInput(
            realInputVolume=realInputVolume,
            baseInputVolume=baseInputVolume, baseJobPropertyValue=5000,
            minJobPropertyValue=5000, maxJobPropertyValue=10000).value
        return returnData
    
    def reduce(self, passingData=None, reduceEachChromosomeDataLs=None,
        transferOutput=True, **keywords):
        """
        #. merge all output of input jobs (passingData.mapEachIntervalDataLsLs) into one big one
        
        """
        returnData = PassingData(no_of_jobs = 0)
        returnData.jobDataLs = []
        reduceOutputDirJob = passingData.reduceOutputDirJob
        
        realInputVolume = passingData.jobData.file.noOfIndividuals * passingData.jobData.file.noOfLoci
        baseInputVolume = 200*20000
        walltime = self.scaleJobWalltimeOrMemoryBasedOnInput(
            realInputVolume=realInputVolume,
            baseInputVolume=baseInputVolume, baseJobPropertyValue=60,
            minJobPropertyValue=60, maxJobPropertyValue=500).value
        job_max_memory = self.scaleJobWalltimeOrMemoryBasedOnInput(
            realInputVolume=realInputVolume,
            baseInputVolume=baseInputVolume, baseJobPropertyValue=5000,
            minJobPropertyValue=5000, maxJobPropertyValue=10000).value
        
        outputFile = File(os.path.join(reduceOutputDirJob.output, 'sameSiteConcordance.tsv'))
        reduceJob = self.addStatMergeJob(
            statMergeProgram=self.mergeSameHeaderTablesIntoOne,
            outputF=outputFile,
            parentJobLs=[reduceOutputDirJob],
            transferOutput=transferOutput,)
        returnData.jobDataLs.append(PassingData(jobLs=[reduceJob],
            file=reduceJob.output,
            fileLs=[reduceJob.output]))
        
        for mapEachIntervalDataLs in passingData.mapEachIntervalDataLsLs:
            for mapEachIntervalData in mapEachIntervalDataLs:
                self.addInputToMergeJob(reduceJob, \
                        parentJobLs=[mapEachIntervalData.mapJob])
        
        return returnData
                
    def setup_run(self):
        """
        """
        self.needSplitChrIntervalData = False
        pdata = ParentClass.setup_run(self)
        return self

if __name__ == '__main__':
    main_class = TestMapReduceVCFWorkflow
    po = ProcessOptions(sys.argv, main_class.option_default_dict, error_doc=main_class.__doc__)
    instance = main_class(**po.long_option2value)
    instance.run()