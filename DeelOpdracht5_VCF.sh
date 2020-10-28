#!/usr/bin/env bash

usage() {
echo "Function: $0 script is used to create a BAM-, sorted BAM-, Pileup-, BCF- and VCF-File from a given SAM file."
echo "$0 usage:" && grep "[[:space:]].)\ #" $0 | sed 's/#//' | sed -r 's/([a-z])\)/-\1/';
echo ""
echo "Example:"
echo "$0 -r lclav_genome.fa -s bngsa_sample.SAM -b Results/Variants/bngsa_sample.BAM -t 4"
exit 0;
}
[ $# -eq 0 ] && usage

while getopts hr:s:b:t: flag
do
    case "${flag}" in
        r) # Specify the location of the reference Genome
          REF_GENOME=${OPTARG};;
        s) # Specify the location of the SAM file
          SAMFILE=${OPTARG};;
        b) # Specify the path + name of the output BAM file
          BAMFILE=${OPTARG};;
        t) # Specify the amount of threads to use
          threads=${OPTARG};;
        h | *) # Show help information
          usage
          exit 0
          ;;
    esac
done

BASENAME=${BAMFILE%.BAM}
SORTED_BAM=${BASENAME}'_sorted.BAM'
PILEUP=${BASENAME}'.mpileup'
BCF_FILE=${BASENAME}'.BCF'
VCF_FILE=${BASENAME}'.VCF'
GENOME_LOCATION=${BAMFILE%/*}'/'${REF_GENOME##*/}

echo ""
echo "Creating Pileup file at ${PILEUP}"
echo "Temporarily copying the reference genome since write permission is needed for BAM conversion and mpileup"

cp ${REF_GENOME} ${BAMFILE%/*}'/'

echo ""
echo "Creating BAM file from ${SAMFILE}"

samtools view --threads ${threads} -bT ${GENOME_LOCATION} ${SAMFILE} -o ${BAMFILE}

echo ""
echo "${BAMFILE} created!"

echo ""
echo "Creating sorted BAM file at ${SORTED_BAM}"

samtools sort --threads ${threads} ${BAMFILE} -o ${SORTED_BAM}

echo ""
echo "${SORTED_BAM} created!"

samtools mpileup -uf ${GENOME_LOCATION} ${SORTED_BAM} -o ${PILEUP}

echo "Pileup file created!"

echo ''
echo "Creating BCF file from ${PILEUP}"

bcftools call --threads ${threads} -mv -Ob ${PILEUP} -o ${BCF_FILE}

echo ''
echo 'BCF file created at ${BCF_FILE}'

bcftools convert --threads ${threads} -Ov ${BCF_FILE} -o ${VCF_FILE}

echo ''
echo 'VCF file created at ${VCF_FILE}'
echo ""
echo "Removing extra files:"

rm ${GENOME_LOCATION} ${GENOME_LOCATION}'.fai'