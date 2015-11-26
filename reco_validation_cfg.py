import FWCore.ParameterSet.Config as cms

process = cms.Process("validation")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQMServices.Core.DQM_cfg")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'ERROR'

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff") 
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string("76X_mcRun2_asymptotic_Queue")
# 76X_mcRun2_asymptotic_v1

# DQM include
process.load("Configuration.EventContent.EventContent_cff")
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

# write DQM file
process.DQMoutput = cms.OutputModule("PoolOutputModule",
  splitLevel = cms.untracked.int32(0),
  outputCommands = process.DQMEventContent.outputCommands,
  fileName = cms.untracked.string('DQMfile2.root'),
  #fileName = cms.untracked.string('DQMfile.root'),
  dataset = cms.untracked.PSet(
    filterName = cms.untracked.string(''),
    dataTier = cms.untracked.string('')
  )
)

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *

#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("ak4JetTracksAssociatorExplicit")

# for the PU ID
# Select GenJets with Pt>8 GeV
process.ak4GenJetsMCPUJetID = cms.EDFilter("GenJetSelector",
    src    = cms.InputTag("ak4GenJets"),
    cut    = cms.string('pt > 8.0'),
    filter = cms.bool(False)             # in case no GenJets pass the selection, do not filter events, just produce an empty GenJet collection
)

# Match selected GenJets to RecoJets
process.ak4PFJetsGenJetMatchMCPUJetID = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR
    src                   = cms.InputTag("ak4PFJetsCHS"),           # RECO jets (any View<Jet> is ok)
    matched               = cms.InputTag("ak4GenJetsMCPUJetID"), # GEN jets  (must be GenJetCollection)
    mcPdgId               = cms.vint32(),                        # N/A
    mcStatus              = cms.vint32(),                        # N/A
    checkCharge           = cms.bool(False),                     # N/A
    maxDeltaR             = cms.double(0.25),                    # Minimum deltaR for the match
    resolveAmbiguities    = cms.bool(True),                      # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(False),
)

#for the flavour matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK4PFJetsMCFlavourInfos_cfi import ak4JetFlavourInfos
process.jetFlavourInfosAK4PFJets = ak4JetFlavourInfos.clone()
process.jetFlavourInfosAK4PFJets.jets = cms.InputTag("ak4PFJetsCHS")

from RecoBTag.Configuration.RecoBTag_cff import *

#standard validation tools
from DQMOffline.RecoB.bTagCommon_cff import*
process.load("DQMOffline.RecoB.bTagCommon_cff")

from Validation.RecoB.bTagAnalysis_cfi import *
process.load("Validation.RecoB.bTagAnalysis_cfi")
process.bTagValidation.jetMCSrc = 'jetFlavourInfosAK4PFJets'
process.bTagValidation.JECsourceMC = 'ak4PFCHSL1FastL2L3'
process.bTagValidation.genJetsMatched = 'ak4PFJetsGenJetMatchMCPUJetID'
#process.bTagValidation.allHistograms = True 
#process.bTagValidation.fastMC = True
process.bTagValidation.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagValidation.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4)
process.bTagValidation.doPUid = cms.bool(True)
process.bTagValidation.doJEC = cms.bool(False)
process.bTagValidation.flavPlots = cms.string("alldusg")

process.bTagValidation.tagConfig = cms.VPSet(
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("ghostTrackBJetTags"),
            folder = cms.string("GTtrk")
		),
		cms.PSet(
	    bTagGhostTrackAnalysisBlock,
	    type = cms.string('GenericMVA'),
#	    ipTagInfos= cms.InputTag("impactParameterTagInfos"),
	    ipTagInfos= cms.InputTag("impactParameterTagInfos"),
	    svTagInfos=cms.InputTag("ghostTrackVertexTagInfos"),
	    label = cms.InputTag("ghostTrackComputer"),
	    folder=cms.string("GTtrk_vars"),
		),
		cms.PSet(
            bTagGenericAnalysisBlock,
            label = cms.InputTag("pfGhostTrackBJetTags"),
            folder = cms.string("GTpf")
		),
		cms.PSet(
	    bTagGhostTrackAnalysisBlock,
	    type = cms.string('GenericMVA'),
#	    ipTagInfos= cms.InputTag("impactParameterTagInfos"),
	    ipTagInfos= cms.InputTag("pfImpactParameterTagInfos"),
	    svTagInfos=cms.InputTag("pfGhostTrackVertexTagInfos"),
	    label = cms.InputTag("candidateGhostTrackComputer"),
	    folder=cms.string("GTpf_Vars"),
		),
	)
	
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)


process.btagDQM = cms.Path(
process.ak4GenJetsMCPUJetID *
process.ak4PFJetsGenJetMatchMCPUJetID *
process.ak4JetTracksAssociatorExplicit * 
process.selectedHadronsAndPartons *
process.jetFlavourInfosAK4PFJets *
impactParameterTagInfos *
ghostTrackVertexTagInfos *
ghostTrackBJetTags *
pfImpactParameterTagInfos *
pfGhostTrackVertexTagInfos *
pfGhostTrackBJetTags *
process.bTagValidation
)

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(
  process.btagDQM,
  process.endjob_step,
  process.DQMoutput_step
)

process.PoolSource.fileNames = [
#'root://cms-xrd-global.cern.ch//store/relval/CMSSW_7_4_0_pre9/RelValTTbar_13/GEN-SIM-RECO/PU50ns_MCRUN2_74_V6-v1/00000/82C64875-E9D3-E411-8C2F-003048FFCC1E.root'
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/000470E0-3B75-E411-8B90-00266CFFA604.root'
]
