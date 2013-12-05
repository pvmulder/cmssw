import FWCore.ParameterSet.Config as cms

process = cms.Process("CSVTrainer")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("RecoBTau.JetTagComputer.jetTagRecord_cfi")
process.load("RecoBTag.SecondaryVertex.combinedSecondaryVertexES_cfi")
#process.combinedSecondaryVertex.trackMultiplicityMin = cms.uint32(2)

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.Geometry_cff") #old one, to use for old releases
process.load("Configuration.Geometry.GeometryIdeal_cff") #new one
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string("START53_V26::All")

##To use the newest training!
#process.load("CondCore.DBCommon.CondDBSetup_cfi")
#process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
#       process.CondDBSetup,
#       timetype = cms.string('runnumber'),
#       toGet = cms.VPSet(cms.PSet(
#               record = cms.string('BTauGenericMVAJetTagComputerRcd'),
#               tag = cms.string('MVAJetTags_CMSSW_5_3_4')
#       )),
#       connect = cms.string("sqlite_file:MVAJetTags_withPFnoPU_Adding2HighPtBins.db"),
#       #connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
#       BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
#)
#process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")

#for Inclusive Vertex Finder
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')
process.load('RecoBTag/SecondaryVertex/inclusiveSecondaryVertexFinderTagInfos_cfi')

#define you jet ID
jetID = cms.InputTag("ak5PFJets")
JetCut=cms.string("neutralHadronEnergyFraction < 0.99 && neutralEmEnergyFraction < 0.99 && nConstituents > 1 && chargedHadronEnergyFraction > 0.0 && chargedMultiplicity > 0.0 && chargedEmEnergyFraction < 0.99")


#do the PFnoPU using PF2PAT
process.out = cms.OutputModule("PoolOutputModule",
                               outputCommands = cms.untracked.vstring('drop *'),
                               fileName = cms.untracked.string('EmptyFile.root')
                               )
process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix="PF2PAT"
usePF2PAT(process,runPF2PAT=True, jetAlgo="AK5", runOnMC=True, postfix=postfix, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), typeIMetCorrections=False
)
process.patJetCorrFactorsPF2PAT.payload = 'AK5PFchs'
process.patJetCorrFactorsPF2PAT.levels = cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])
process.pfPileUpPF2PAT.checkClosestZVertex = False
process.patJetsPF2PAT.discriminatorSources = cms.VInputTag(
        cms.InputTag("trackCountingHighEffBJetTagsAODPF2PAT")
)
process.btaggingJetTagsAODPF2PAT = cms.Sequence(getattr(process,"combinedSecondaryVertexBJetTagsAODPF2PAT") )
# top projections in PF2PAT:
getattr(process,"pfNoPileUp"+postfix).enable = True
#applyPostfix(process,"patJetCorrFactors",postfix).payload = cms.string('AK5PFchs')
#process.pfPileUpPF2PAT.Vertices = cms.InputTag('goodOfflinePrimaryVertices')
#process.pfPileUpPF2PAT.checkClosestZVertex = cms.bool(False)
process.selectedPatJetsPF2PAT.cut = JetCut
process.JECAlgo = cms.Sequence( getattr(process,"patPF2PATSequence"+postfix) )

newjetID=cms.InputTag("selectedPatJetsPF2PAT")

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = jetID # replaced by newjetID later
                                                  )

#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")

process.load("PhysicsTools.JetMCAlgos.CaloJetsMCFlavour_cfi")  
process.AK5byRef.jets = jetID # replaced by newjetID later

#do the matching
process.flavourSeq = cms.Sequence(
    process.myPartons *
    process.AK5Flavour
    )


#select good primary vertex
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

process.myak5JetTracksAssociatorAtVertex.jets = newjetID
process.AK5byRef.jets                         = newjetID

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.source = cms.Source("PoolSource",
#	fileNames = cms.untracked.vstring('file:testTagInfos.root')
	fileNames = cms.untracked.vstring(
#'/store/mc/Fall11/QCD_Pt-50to80_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00225C27-4744-E111-8583-003048C692E4.root',
#'/store/mc/Fall11/QCD_Pt-80to120_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00D668C4-5244-E111-A8F6-0025901D4936.root',
#'/store/mc/Fall11/QCD_Pt-120to170_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/023CE3AD-CF46-E111-90CB-003048C690A0.root',
#'/store/mc/Fall11/QCD_Pt-170to300_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0433579C-7644-E111-9D93-00215AD4D6C8.root',
#'/store/mc/Fall11/QCD_Pt-300to470_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00C128DE-923F-E111-AA76-003048C69312.root',
#'/store/mc/Fall11/QCD_Pt-470to600_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00CC4BA4-FC45-E111-A993-003048F0E80C.root',
#'/store/mc/Fall11/QCD_Pt-600to800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/000548D5-0A40-E111-A327-002481E0DA4E.root',
#'/store/mc/Fall11/QCD_Pt-800to1000_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0469BF65-8343-E111-8E43-003048F0E3B2.root',
#'/store/mc/Fall11/QCD_Pt-1000to1400_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/14151191-9043-E111-BA90-003048C690A0.root',
#'/store/mc/Fall11/QCD_Pt-1400to1800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0E10C938-1146-E111-95AC-0025901D4A58.root',
#'/store/mc/Fall11/QCD_Pt-1800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0C4D9605-2544-E111-B39F-003048D4DF80.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FED775BD-B8E1-E111-8ED5-003048C69036.root'
	)
)


process.combinedSVMVATrainer = cms.EDAnalyzer("JetTagMVAExtractor",
	variables = cms.untracked.VPSet(
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVRecoVertex"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","flightDistance2dSig","flightDistance3dSig","flightDistance2dVal","flightDistance3dVal","trackSumJetEtRatio","jetNSecondaryVertices","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","vertexFitProb","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVPseudoVertex"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),

		cms.untracked.PSet( label = cms.untracked.string("CombinedSVNoVertex"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity"
)) # no trackEtaRel!!!???!!!

	),
	ipTagInfos = cms.InputTag("impactParameterTagInfos"),
	#svTagInfos =cms.InputTag("secondaryVertexTagInfos"),
	svTagInfos =cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"),
	
	minimumTransverseMomentum = cms.double(15.0),
	maximumTransverseMomentum = cms.double(9999999.),
	useCategories = cms.bool(True),
        calibrationRecords = cms.vstring(
                'CombinedSVRecoVertex',
                'CombinedSVPseudoVertex',
                'CombinedSVNoVertex'),
	categoryVariableName = cms.string('vertexCategory'), # vertexCategory = Reco,Pseudo,No
	maximumPseudoRapidity = cms.double(2.5),
	signalFlavours = cms.vint32(5, 7),
	minimumPseudoRapidity = cms.double(0.0),
	jetTagComputer = cms.string('combinedSecondaryVertex'),
	jetFlavourMatching = cms.InputTag("AK5byValAlgo"),
	ignoreFlavours = cms.vint32(0)
)

process.p = cms.Path(
process.goodOfflinePrimaryVertices * 
process.JECAlgo * 
process.inclusiveVertexing * 
#process.inclusiveMergedVerticesFiltered * 
#process.bToCharmDecayVertexMerged * 
process.myak5JetTracksAssociatorAtVertex * 
process.impactParameterTagInfos * 
process.inclusiveSecondaryVertexFinderTagInfos *
process.flavourSeq * 
process.combinedSVMVATrainer 
)

 
