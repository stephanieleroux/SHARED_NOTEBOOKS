#!/bin/bash
#SBATCH --job-name=estats
#SBATCH -e estats.e%j
#SBATCH -o estats.o%j
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --time=05:00:00           
#SBATCH -A fortran
#SBATCH --mem=5000                 # memory = 5Gb

# Purpose: compute the ensemble statistics from the IMHOTEP ensemble based on the cdftool cdfenstat

EXP="ES"
CONFCASE="eORCA025.L75-IMHOTEP.${EXP}"
typ="gridTsurf"


# directory where the MEDWEST60 ensembles are archived on jean zay
DATADIR=/gpfsstore/rech/cli/rcli002/eORCA025.L75/${CONFCASE}

# directory where the ensemble stats outputs will be archived
OUTDIR=/gpfsstore/rech/cli/commun/IMHOTEP/ENSTATS_1m/${EXP}/

# go to the output directory
cd $OUTDIR

# loop on years and months
for yyyy in  {1980..2018}; do
for mm in {01..12}; do
# list of files (all members of the ensemble for a given date
for g in  "${DATADIR}.???-S/1m/${yyyy}/${CONFCASE}.???_y${yyyy}m${mm}.1m_${typ}.nc" ; do

    # check if output file does not exist yet
    if [ ! -f ${OUTDIR}/ESTATS_${CONFCASE}_y${yyyy}_${typ}.nc ]; then
    
    # compute the ensemble stats using cdfenstat
    cdfenstat -l ${g} -o ${OUTDIR}/ESTATS_${CONFCASE}_y${yyyy}m${mm}_${typ}.nc  -nc4
    #echo $g
    fi

done
done
done

