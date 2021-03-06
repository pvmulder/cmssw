#!/bin/sh

castorDir=/castor/cern.ch/user/p/pjanot/CMSSW300pre6/
cmsswDir=/afs/cern.ch/user/p/pjanot/scratch0/CMSSW_3_0_0_pre6/src

for ((energy=0; energy<=8; energy++));
  do
  case $energy in
      0)
	  ptmin=20
	  ptmax=30
	  ;;
      1)
	  ptmin=30
	  ptmax=50
	  ;;
      2)
	  ptmin=50
	  ptmax=80
	  ;;
      3)
	  ptmin=80
	  ptmax=120
	  ;;
      4)
	  ptmin=120
	  ptmax=160
	  ;;
      5)
	  ptmin=160
	  ptmax=250
	  ;;
      6)
	  ptmin=250
	  ptmax=350
	  ;;
      7)
	  ptmin=350
	  ptmax=500
	  ;;
      8)
	  ptmin=500
	  ptmax=700
	  ;;
    esac
	
    name="QCDDiJet_"$ptmin"_"$ptmax"_Fast"
    displayfilename="display_"${name}".root"
    aodfilename="aod_"${name}".root"
    recofilename="reco_"${name}".root"
    echo $name
    
    seed1=$(( ($job+1) + 143123*($energy+1) ))
    sed -e "s/==BINLOW==/${ptmin}/" -e "s/==BINHIGH==/${ptmax}/" QCDFastSim_cfg.py > tmp_cfg
    
#Start to write the script
    cat > job_${name}.sh << EOF

#!/bin/sh
cd $cmsswDir
eval \`scramv1 runtime -sh\`
cd -
#commande pour decoder le .cfg
cat > TEST_cfg.py << "EOF"
EOF
    
#Ajoute le .cfg au script
cat  tmp_cfg>> job_${name}.sh

# On poursuit le script
echo "EOF" >> job_${name}.sh
cat >> job_${name}.sh << EOF
cmsRun TEST_cfg.py >& log


rfcp display.root $castorDir$displayfilename
rfcp aod.root $castorDir$aodfilename
rfcp reco.root $castorDir$recofilename

EOF
echo "Save files : "$castorDir$displayfilename", "$castorDir$aodfilename", "$castorDir$recofilename
chmod 755 job_${name}.sh
bsub -q cmst3 -J $name $PWD/job_${name}.sh


done

