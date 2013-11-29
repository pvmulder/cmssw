#!/bin/bash

maindirec=/pnfs/iihe/cms/store/user/`whoami`/BtagExtractor_53X/NewVarsNewCat_modified1_tightTrackSel/

dirs_to_merge=(QCD_Pt-1000to1400_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-120to170_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v3_AODSIM QCD_Pt-1400to1800_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-15to30_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-30to50_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM QCD_Pt-470to600_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM QCD_Pt-50to80_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM QCD_Pt-600to800_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM QCD_Pt-800to1000_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM QCD_Pt-80to120_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v3_AODSIM)

#dirs_to_merge=( TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM )

homedirec=/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/CMSSW_5_3_4_patch1/src/CrabJobs_modified1_tightTrackSel/RootFiles

CAT=(CombinedSVRecoVertex CombinedSVPseudoVertex CombinedSVNoVertex)
FLAV=(B C DUSG)

mkdir $homedirec/QCD_training
cd $homedirec/QCD_training

for l in ${dirs_to_merge[@]} ;
do
	for k in ${CAT[@]} ;
	do
		for j in $( ls $maindirec/$l/${k}_B*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Bfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_C*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Cfiles.txt; done
		if [ $k=="CombinedSVNoVertex" ]
		then
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_D*); do
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_U*); do 
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_S*); do 
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_G*); do 
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt
			done
		else
			for j in $( ls $maindirec/$l/${k}_D*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_U*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_S*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_G*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}DUSGfiles.txt; done			
		fi
	done
done	

for k in ${CAT[@]} ;
do
	for i in ${FLAV[@]} ;
	do
#		echo cat ${k}${i}files.txt
		rootfiles=`cat ${k}${i}files.txt`
		hadd tmp.root $rootfiles
		mv tmp.root ${k}_${i}.root
	done
done
