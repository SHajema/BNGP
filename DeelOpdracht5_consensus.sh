#!/usr/bin/env bash

usage() {
echo "$0 script is used to index the reference Genome and the Align reads onto that indexed Genome."
echo "$0 usage:" && grep "[[:space:]].)\ #" $0 | sed 's/#//' | sed -r 's/([a-z])\)/-\1/';
echo ""
echo "Example:"
echo "$0 -r <path to reference genome> -d <path to directory + basename> -t <number of threads as integer> -1 <path to Read1 file> -2 <path to Read2 file>"
exit 0;
}
[ $# -eq 0 ] && usage

while getopts hr:v:f:t: flag
do
    case "${flag}" in
        r) # Specify the location of the reference genome
          REF_GENOME=${OPTARG};;
        v) # Specify the location of the VCF file
          VCF_FILE=${OPTARG};;
        f) # Specify the path of the fasta output name
          FASTA_FILE=${OPTARG};;
        t) # Specify the amount of threads to use
          threads=${OPTARG};;
        h | *) # Show help information
          usage
          exit 0
          ;;
    esac
done

GZ_FILE=${VCF_FILE}'.gz'


echo ""
echo "bgzipping VCF file at ${GZ_FILE}"

bgzip --threads ${threads} -c ${VCF_FILE} > ${GZ_FILE}

echo ""
echo "Gunzipped file located at: ${GZ_FILE}"
echo "Creating bcftools index for: ${GZ_FILE}"

bcftools index ${GZ_FILE}

echo "Creating a consensus sequence from VCF file"

bcftools consensus -f ${REF_GENOME} ${GZ_FILE} -o ${FASTA_FILE}

echo ""
echo "Consensus fasta created at: ${FASTA_FILE}"
echo ""
echo "Removing extra files"

rm ${GZ_FILE} ${GZ_FILE}'.csi' ${}