import FWCore.ParameterSet.Config as cms

process = cms.Process("L1SKIM")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100000
#process.MessageLogger.categories.append('L1GtTrigReport')
#process.MessageLogger.categories.append('HLTrigReport')

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

#process.load(INPUTFILELIST)
process.source = cms.Source("PoolSource",fileNames =cms.untracked.vstring(
    '/store/mc/Summer11/QCD_Pt-1800_TuneZ2_7TeV_pythia6/AODSIM/PU_S3_START42_V11-v2/0000/04C728A6-927D-E011-8313-00304867915A.root'
    ))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )

##################### digi-2-raw plus L1 emulation #########################
process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration/StandardSequences/GeometryExtended_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('TrackingTools/TrackAssociator/DetIdAssociatorESProducer_cff')

#################### Conditions and L1 menu ################################

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'START42_V13G::All'

process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF      = cms.uint32(4) ,
                                           maxAbsZ          = cms.double(20.0),
                                           maxd0            = cms.double(10.0)
                                           )

process.load("Calibration.IsolatedParticles.isolatedGenParticles_cfi")
process.isolatedGenParticles.GenSrc            = "Dummy"
process.isolatedGenParticles.UseHepMC          = False
process.isolatedGenParticles.Verbosity         = 0

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('IsoGenParticles.root')
                                   )


# define an EndPath to analyze all other path results
process.hltTrigReport = cms.EDAnalyzer( 'HLTrigReport',
      #HLTriggerResults = cms.InputTag( 'TriggerResults','','REDIGI36X')
      HLTriggerResults = cms.InputTag( 'TriggerResults','','HLT') 
)

process.load("L1Trigger.GlobalTriggerAnalyzer.l1GtTrigReport_cfi")
process.l1GtTrigReport.L1GtRecordInputTag = 'gtDigis'
process.l1GtTrigReport.PrintVerbosity = 0
#=============================================================================

process.p1 = cms.Path(process.primaryVertexFilter*process.isolatedGenParticles)
#process.p1 = cms.Path( process.isotracksGen )
