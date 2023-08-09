import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var
#from PhysicsTools.NanoAOD.jetsAK4_CHS_cff import jetTable, jetCorrFactorsNano, updatedJets, finalJets, qgtagger, hfJetShowerShapeforNanoAOD
from PhysicsTools.NanoAOD.jetsAK4_Puppi_cff import jetPuppiTable, jetPuppiCorrFactorsNano, updatedJetsPuppi, updatedJetsPuppiWithUserData
from PhysicsTools.NanoAOD.jetsAK8_cff import fatJetTable, subJetTable
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
from PhysicsTools.PatAlgos.tools.helpers import addToProcessAndTask, getPatAlgosToolsTask

def update_jets_AK4(process):
    # Based on ``nanoAOD_addDeepInfo``
    # in https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nano_cff.py
    # DeepJet flav_names as found in
    # https://github.com/cms-sw/cmssw/blob/master/RecoBTag/ONNXRuntime/plugins/DeepFlavourONNXJetTagsProducer.cc#L86
    # and https://twiki.cern.ch/twiki/bin/view/CMS/DeepJet
    from RecoBTag.ONNXRuntime.pfParticleTransformerAK4_cff import _pfParticleTransformerAK4JetTagsAll as pfParticleTransformerAK4JetTagsAll
    from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK4_cff import _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsAll as pfParticleNetFromMiniAODAK4PuppiCentralJetTagsAll

    _btagDiscriminators = [    
        'pfDeepFlavourJetTags:probb',
        'pfDeepFlavourJetTags:probbb',
        'pfDeepFlavourJetTags:problepb',
        'pfDeepFlavourJetTags:probc',
        'pfDeepFlavourJetTags:probuds',
        'pfDeepFlavourJetTags:probg',
    ] + pfParticleTransformerAK4JetTagsAll \
        + pfParticleNetFromMiniAODAK4PuppiCentralJetTagsAll
    
    updateJetCollection(
        process,
        jetSource=cms.InputTag('slimmedJetsPuppi'),
        jetCorrections=('AK4PFPuppi',
                        cms.vstring(
                            ['L1FastJet', 'L2Relative', 'L3Absolute',
                             'L2L3Residual']), 'None'),
        btagDiscriminators=_btagDiscriminators,
        postfix='WithDeepInfo',
    )
    process.load("Configuration.StandardSequences.MagneticField_cff")
    process.jetPuppiCorrFactorsNano.src = "selectedUpdatedPatJetsWithDeepInfo"
    process.updatedJetsPuppi.jetSource = "selectedUpdatedPatJetsWithDeepInfo"
    
    
    process.updatedPatJetsTransientCorrectedWithDeepInfo.addTagInfos = cms.bool(True)
    
    
    return process


def update_jets_AK8(process):
    # Based on ``nanoAOD_addDeepInfoAK8``
    # in https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nano_cff.py
    # Care needs to be taken to make sure no discriminators from stock Nano are excluded -> would results in unfilled vars
    _btagDiscriminators = [
        'pfJetProbabilityBJetTags',
        'pfDeepCSVJetTags:probb',
        'pfDeepCSVJetTags:probc',
        'pfDeepCSVJetTags:probbb',
        'pfDeepCSVJetTags:probudsg',
        'pfMassIndependentDeepDoubleBvLJetTags:probHbb',
        'pfMassIndependentDeepDoubleCvLJetTags:probHcc',
        'pfMassIndependentDeepDoubleCvBJetTags:probHcc',
        'pfMassIndependentDeepDoubleBvLV2JetTags:probHbb',
        'pfMassIndependentDeepDoubleCvLV2JetTags:probHcc',
        'pfMassIndependentDeepDoubleCvBV2JetTags:probHcc',
        ]
    from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfParticleNetJetTagsAll as pfParticleNetJetTagsAll
    _btagDiscriminators += pfParticleNetJetTagsAll
    updateJetCollection(
        process,
        jetSource=cms.InputTag('slimmedJetsAK8'),
        pvSource=cms.InputTag('offlineSlimmedPrimaryVertices'),
        svSource=cms.InputTag('slimmedSecondaryVertices'),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi',
                        cms.vstring([
                            'L1FastJet', 'L2Relative', 'L3Absolute',
                            'L2L3Residual'
                        ]), 'None'),
        btagDiscriminators=_btagDiscriminators,
        postfix='AK8WithDeepInfo',
        # this should work but doesn't seem to enable the tag info with addTagInfos
        # btagInfos=['pfDeepDoubleXTagInfos'],
        printWarning=False)
    process.jetCorrFactorsAK8.src = "selectedUpdatedPatJetsAK8WithDeepInfo"
    process.updatedJetsAK8.jetSource = "selectedUpdatedPatJetsAK8WithDeepInfo"
    # add DeepDoubleX taginfos
    process.updatedPatJetsTransientCorrectedAK8WithDeepInfo.tagInfoSources.append(cms.InputTag("pfDeepDoubleXTagInfosAK8WithDeepInfo"))
    process.updatedPatJetsTransientCorrectedAK8WithDeepInfo.addTagInfos = cms.bool(True)
    return process


def update_jets_AK8_subjet(process):
    # Based on ``nanoAOD_addDeepInfoAK8``
    # in https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nano_cff.py
    # and https://github.com/alefisico/RecoBTag-PerformanceMeasurements/blob/10_2_X_boostedCommissioning/test/runBTagAnalyzer_cfg.py
    _btagDiscriminators = [
        'pfJetProbabilityBJetTags',
        'pfDeepCSVJetTags:probb',
        'pfDeepCSVJetTags:probc',
        'pfDeepCSVJetTags:probbb',
        'pfDeepCSVJetTags:probudsg',
        ]
    updateJetCollection(
        process,
        labelName='SoftDropSubjetsPF',
        jetSource=cms.InputTag("slimmedJetsAK8PFPuppiSoftDropPacked", "SubJets"),
        jetCorrections=('AK4PFPuppi',
                        ['L2Relative', 'L3Absolute'], 'None'),
        btagDiscriminators=list(_btagDiscriminators),
        explicitJTA=True,  # needed for subjet b tagging
        svClustering=False,  # needed for subjet b tagging (IMPORTANT: Needs to be set to False to disable ghost-association which does not work with slimmed jets)
        fatJets=cms.InputTag('slimmedJetsAK8'),  # needed for subjet b tagging
        rParam=0.8,  # needed for subjet b tagging
        sortByPt=False, # Don't change order (would mess with subJetIdx for FatJets)
        postfix='AK8SubjetsWithDeepInfo')

    process.subJetTable.src = 'selectedUpdatedPatJetsSoftDropSubjetsPFAK8SubjetsWithDeepInfo' 
    

    return process


def get_DeepJet_outputs():
    DeepJetOutputVars = cms.PSet(
        btagDeepFlavB_b=Var("bDiscriminator('pfDeepFlavourJetTags:probb')",
                            float,
                            doc="DeepJet b tag probability",
                            precision=10),
        btagDeepFlavB_bb=Var("bDiscriminator('pfDeepFlavourJetTags:probbb')",
                            float,
                            doc="DeepJet bb tag probability",
                            precision=10),
        btagDeepFlavB_lepb=Var("bDiscriminator('pfDeepFlavourJetTags:problepb')",
                            float,
                            doc="DeepJet lepb tag probability",
                            precision=10),
        btagDeepFlavC=Var("bDiscriminator('pfDeepFlavourJetTags:probc')",
                            float,
                            doc="DeepJet c tag probability",
                            precision=10),
        btagDeepFlavUDS=Var("bDiscriminator('pfDeepFlavourJetTags:probuds')",
                            float,
                            doc="DeepJet uds tag probability",
                            precision=10),
        btagDeepFlavG=Var("bDiscriminator('pfDeepFlavourJetTags:probg')",
                            float,
                            doc="DeepJet gluon tag probability",
                            precision=10),
        # discriminators are already part of jets_cff.py from NanoAOD and therefore not added here     
    )
    return DeepJetOutputVars


def get_ParticleNetAK4_outputs():
    ParticleNetAK4OutputVars = cms.PSet(
        # default discriminants
        btagPNetB = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll'):-1",
                            float,
                            doc="ParticleNet b vs. udscg",
                            precision=10),
        btagPNetCvL = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsL')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsL'):-1",
                            float,
                            doc="ParticleNet c vs. udsg",
                            precision=10),
        btagPNetCvB = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsB')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsB'):-1",
                            float,
                            doc="ParticleNet c vs. b",
                            precision=10),
        btagPNetQvG = Var("?abs(eta())<2.5?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:QvsG'):bDiscriminator('pfParticleNetFromMiniAODAK4PuppiForwardDiscriminatorsJetTags:QvsG')",
                            float,
                            doc="ParticleNet q (udsbc) vs. g",
                            precision=10),
        btagPNetTauVJet = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:TauVsJet')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:TauVsJet'):-1",
                            float,
                            doc="ParticleNet tau vs. jet",
                            precision=10),
        PNetRegPtRawCorr = Var("?abs(eta())<2.5?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptcorr'):bDiscriminator('pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptcorr')",
                            float,
                            doc="ParticleNet universal flavor-aware visible pT regression (no neutrinos), correction relative to raw jet pT",
                            precision=10),
        PNetRegPtRawCorrNeutrino = Var("?abs(eta())<2.5?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptnu'):bDiscriminator('pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptnu')",
                            float,
                            doc="ParticleNet universal flavor-aware pT regression neutrino correction, relative to visible. To apply full regression, multiply raw jet pT by both PNetRegPtRawCorr and PNetRegPtRawCorrNeutrino.",
                            precision=10),
        PNetRegPtRawRes = Var("?abs(eta())<2.5?0.5*(bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptreshigh')-bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:ptreslow')):0.5*(bDiscriminator('pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptreshigh')-bDiscriminator('pfParticleNetFromMiniAODAK4PuppiForwardJetTags:ptreslow'))",
                            float,
                            doc="ParticleNet universal flavor-aware jet pT resolution estimator, (q84 - q16)/2",
                            precision=10),
        # raw scores
        btagPNetProbB = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probb')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probb'):-1",
                            float,
                            doc="ParticleNet b tag probability",
                            precision=10),
        btagPNetProbC = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probc')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probc'):-1",
                            float,
                            doc="ParticleNet c tag probability",
                            precision=10),
        btagPNetProbUDS = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probuds')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probuds'):-1",
                            float,
                            doc="ParticleNet uds tag probability",
                            precision=10),
        btagPNetProbG = Var("?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probg')>0?bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralJetTags:probg'):-1",
                            float,
                            doc="ParticleNet gluon tag probability",
                            precision=10),
    )

    return ParticleNetAK4OutputVars


def get_ParticleTransformerAK4_outputs():
    ParticleTransformerAK4OutputVars = cms.PSet(
        btagRobustParTAK4B = Var("bDiscriminator('pfParticleTransformerAK4JetTags:probb')+bDiscriminator('pfParticleTransformerAK4JetTags:probbb')+bDiscriminator('pfParticleTransformerAK4JetTags:problepb')",
                            float,
                            doc="Negative RobustParTAK4 b+bb+lepb tag discriminator",
                            precision=10),
        btagRobustParTAK4CvL = Var("?(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds')+bDiscriminator('pfParticleTransformerAK4JetTags:probg'))>0?bDiscriminator('pfParticleTransformerAK4JetTags:probc')/(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds')+bDiscriminator('pfParticleTransformerAK4JetTags:probg')):-1",
                            float,
                            doc="Negative RobustParTAK4 c vs uds+g discriminator",
                            precision=10),
        btagRobustParTAK4CvB = Var("?(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probb')+bDiscriminator('pfParticleTransformerAK4JetTags:probbb')+bDiscriminator('pfParticleTransformerAK4JetTags:problepb'))>0?bDiscriminator('pfParticleTransformerAK4JetTags:probc')/(bDiscriminator('pfParticleTransformerAK4JetTags:probc')+bDiscriminator('pfParticleTransformerAK4JetTags:probb')+bDiscriminator('pfParticleTransformerAK4JetTags:probbb')+bDiscriminator('pfParticleTransformerAK4JetTags:problepb')):-1",
                            float,
                            doc="Negative RobustParTAK4 c vs b+bb+lepb discriminator",
                            precision=10),
        btagRobustParTAK4QG = Var("?(bDiscriminator('pfParticleTransformerAK4JetTags:probg')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds'))>0?bDiscriminator('pfParticleTransformerAK4JetTags:probg')/(bDiscriminator('pfParticleTransformerAK4JetTags:probg')+bDiscriminator('pfParticleTransformerAK4JetTags:probuds')):-1",
                            float,
                            doc="Negative RobustParTAK4 g vs uds discriminator",
                            precision=10),        
        btagRobustParTAK4B_b=Var("bDiscriminator('pfParticleTransformerAK4JetTags:probb')",
                            float,
                            doc="RobustParTAK4 b tag probability",
                            precision=10),
        btagRobustParTAK4B_bb=Var("bDiscriminator('pfParticleTransformerAK4JetTags:probbb')",
                            float,
                            doc="RobustParTAK4 bb tag probability",
                            precision=10),
        btagRobustParTAK4B_lepb=Var("bDiscriminator('pfParticleTransformerAK4JetTags:problepb')",
                            float,
                            doc="RobustParTAK4 lepb tag probability",
                            precision=10),
        btagRobustParTAK4C=Var("bDiscriminator('pfParticleTransformerAK4JetTags:probc')",
                            float,
                            doc="RobustParTAK4 c tag probability",
                            precision=10),
        btagRobustParTAK4UDS=Var("bDiscriminator('pfParticleTransformerAK4JetTags:probuds')",
                            float,
                            doc="RobustParTAK4 uds tag probability",
                            precision=10),
        btagRobustParTAK4G=Var("bDiscriminator('pfParticleTransformerAK4JetTags:probg')",
                            float,
                            doc="RobustParTAK4 gluon tag probability",
                            precision=10),
    )

    return ParticleTransformerAK4OutputVars


def add_run3_taggers(process, runOnMC=False):

    update_jets_AK4(process)
    update_jets_AK8(process)
    update_jets_AK8_subjet(process)

    process.customizeJetTask = cms.Task()
    process.schedule.associate(process.customizeJetTask)

    # AK4
    process.customJetExtTable = cms.EDProducer(
        "SimpleCandidateFlatTableProducer",
        src=jetPuppiTable.src,
        cut=jetPuppiTable.cut,
        name=jetPuppiTable.name,
        doc=jetPuppiTable.doc,
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(True),  # this is the extension table for Jets
        variables=cms.PSet(
            get_DeepJet_outputs(),
            get_ParticleNetAK4_outputs(),
            get_ParticleTransformerAK4_outputs(),
        ))

    # disable the ParT branches in default jetPuppi table
    from PhysicsTools.NanoAOD.nano_eras_cff import run3_nanoAOD_122, run3_nanoAOD_124
    (run3_nanoAOD_122 | run3_nanoAOD_124).toModify(
        process.jetPuppiTable.variables,
        btagRobustParTAK4B = None,
        btagRobustParTAK4CvL = None,
        btagRobustParTAK4CvB = None,
        btagRobustParTAK4QG = None,
    )

    process.customizeJetTask.add(process.customJetExtTable)

    return process


def nanoAddRun3TaggersCustomize_MC(process):
    return add_run3_taggers(process, runOnMC=True)

def nanoAddRun3TaggersCustomize_Data(process):
    return add_run3_taggers(process, runOnMC=False)
