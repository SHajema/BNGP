Variant calling and analysis pipeline s1088987

Function:
This pipeline takes Illumina Paired-end read files plus a reference genome and executes a variant calling analysis on these files.
It does this by First making a Quality report of the raw Data, then trimming the reads based on quality and then performing a quality report on this trimmed data.
These trimmed reads are then mapped to a indexed reference genome, with the results being stored in a SAM file.
This file is then converted in a BAM file, which first gets sorted and then a Pileup file is created from this sorted BAM file.
This pileup file is then used to create a BCF file, which gets converted to a VCF file.
This VCF file is then used to create a consensus sequence and is further used to analyse the different mutations and indels in the samples.

Usage:
snakemake --snakefile Snakefile_s1088987
snakefile --snakefile Snakefile_s1088987 -d <Base output directory>

Example:
snakemake --snakefile Snakefile_s1088987
snakefile --snakefile Snakefile_s1088987 -d runkoen

Outputfiles of the Pipeline:
Files:                                                                 Description:

Results directory:
  Results/bngsa_nietinfected_1.QC                                      QC report of raw inputfile 1
  Results/bngsa_nietinfected_2.QC                                      QC report of raw inputfile 2
  Results/bngsa_nietinfected_1_trimmed.fastq                           The Trimmed results of the inputfile 1
  Results/bngsa_nietinfected_2_trimmed.fastq                           The Trimmed results of the inputfile 1
  Results/bngsa_nietinfected_1_trimmed.QC                              QC report of the trimmed inputfile 1
  Results/bngsa_nietinfected_2_trimmed.QC                              QC report of the trimmed inputfile 1
  Results/bngsa_consensus.fasta                                        The consensus file (in Fasta format) of the given inputfiles

Results/Genome directory:
  Results/Genome/bngsa_sample.[1-4].bt2                               Indexed reference Genome
  Results/Genome/bngsa_sample.rev.[1-2].bt2                           Indexed reference Genome


Results/Varients directory:
  Results/Variants/bngsa_sample.SAM                                   Aligned reads data in SAM format
  Results/Variants/bngsa_sample.BAM                                   Aligned reads data in BAM format
  Results/Variants/bngsa_sample_sorted.BAM                            Sorted variant of the BAM file
  Results/Variants/bngsa_sample.mpileup                               Pileup file with Variants compared to reference genome
  Results/Variants/bngsa_sample.BCF                                   Variant caller information in binary format
  Results/Variants/bngsa_sample.VCF                                   Variant caller information
  Results/Variants/bngsa_sample_Variants.txt                          File with details of the analysed variants present in the VCF file.
