# nano-run3-utils

This repository provides a recipe to integrate the Run 3 taggers using MiniAODv3 as inputs.

Since NanoAODv11 (run on `12_6_X`) does not include the Run 3 taggers, this recipe runs on MiniAODv3 in `13_0_X` to have them included. It will mimic the condition in NanoAODv12.

It does the following:
 - Re-run Puppi v17 on MiniAODv3, and recluster AK4 Puppi and AK8 jets. The recipe is sourced from [JME slides](https://indico.cern.ch/event/1263032/contributions/5450886/attachments/2671840/4631769/230622_Nurfikri_XPOGWorkshop_JME.pdf)
 - Infer the Run 3 taggers for AK4 Puppi jets (including the new DeepJet, ParticleNetAK4, RobustParticleTransformerAK4) and store the output scores to NanoAOD.

## Setup

```bash
cmsrel CMSSW_13_0_11
cd CMSSW_13_0_11/src
cmsenv

git clone https://github.com/colizz/nano-run3-utils PhysicsTools/NanoRun3Utils

scram b -j8
```

Then, append the following customised configuration in the `cmsDriver` command:

```bash
# for MC, add:
--customise="PhysicsTools/NanoRun3Utils/puppiJetMETReclustering_cff.nanoPuppiReclusterCustomize_MC" \
--customise="PhysicsTools/NanoRun3Utils/addRun3Taggers_cff.nanoAddRun3TaggersCustomize_MC"
```

```bash
# for dataMC, add:
--customise="PhysicsTools/NanoRun3Utils/puppiJetMETReclustering_cff.nanoPuppiReclusterCustomize_Data" \
--customise="PhysicsTools/NanoRun3Utils/addRun3Taggers_cff.nanoAddRun3TaggersCustomize_Data"
```

Below shows four examples to run on the MiniAODv3 sample, for both data (rerecoCDE and promptFG) and MC (preEE and postEE), according to the [PdmV recommandation](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis).

<details>
    
```
cmsDriver.py nano_data_2022CDE --data --eventcontent NANOAOD --datatier NANOAOD --step NANO \
--conditions 124X_dataRun3_v15   --era Run3,run3_nanoAOD_124 \
--customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)" --nThreads 4 \
-n -1 --filein "/store/data/Run2022C/BTagMu/MINIAOD/27Jun2023-v2/80000/000213fb-0712-4a0f-b015-e2334144b2a8.root" --fileout file:nano_data2022CDE.root \
--customise="PhysicsTools/NanoRun3Utils/puppiJetMETReclustering_cff.nanoPuppiReclusterCustomize_Data" \
--customise="PhysicsTools/NanoRun3Utils/addRun3Taggers_cff.nanoAddRun3TaggersCustomize_Data"  --no_exec
```

```
cmsDriver.py nano_data_2022FG --data --eventcontent NANOAOD --datatier NANOAOD --step NANO \
--conditions 124X_dataRun3_PromptAnalysis_v2   --era Run3,run3_nanoAOD_124 \
--customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)" --nThreads 4 \
-n 20 --filein "/store/data/Run2022F/Muon/MINIAOD/PromptReco-v1/000/360/381/00000/0736ad9a-2b1d-4375-9493-9e7e01538978.root" --fileout file:nano_data2022FG.root \
--customise="PhysicsTools/NanoRun3Utils/puppiJetMETReclustering_cff.nanoPuppiReclusterCustomize_Data" \
--customise="PhysicsTools/NanoRun3Utils/addRun3Taggers_cff.nanoAddRun3TaggersCustomize_Data"  --no_exec
```

```    
cmsDriver.py nano_mc_Run3 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --step NANO \
--conditions 126X_mcRun3_2022_realistic_v2   --era Run3,run3_nanoAOD_124 \
--customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)" --nThreads 4 \
-n -1 --filein "/store/mc/Run3Summer22MiniAODv3/QCD_PT-15to20_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_v12-v1/30000/8590bc1e-abd3-4be4-a068-16f4cb6b4994.root" --fileout file:nano_mcRun3.root \
--customise="PhysicsTools/NanoRun3Utils/puppiJetMETReclustering_cff.nanoPuppiReclusterCustomize_MC" \
--customise="PhysicsTools/NanoRun3Utils/addRun3Taggers_cff.nanoAddRun3TaggersCustomize_MC"  --no_exec
```

```    
cmsDriver.py nano_mc_Run3_EE --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --step NANO \
--conditions 126X_mcRun3_2022_realistic_postEE_v4   --era Run3,run3_nanoAOD_124 \
--customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)" --nThreads 4 \
-n -1 --filein "/store/mc/Run3Summer22EEMiniAODv3/QCD_PT-80to120_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v1/2550000/eddaff63-eb30-4155-afdc-3db5b07105b8.root" --fileout file:nano_mcRun3_EE.root \
--customise="PhysicsTools/NanoRun3Utils/puppiJetMETReclustering_cff.nanoPuppiReclusterCustomize_MC" \
--customise="PhysicsTools/NanoRun3Utils/addRun3Taggers_cff.nanoAddRun3TaggersCustomize_MC"  --no_exec
```
    
</details>

-----

Note: this recipe is modified from [PFNano in the specific 13_0_X branch](https://github.com/cms-jet/PFNano/tree/13_0_7_from124MiniAOD).