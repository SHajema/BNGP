import os

SAMPLES = ["/exports/bngp_data/reads/bngsa_nietinfected_1.fastq", "/exports/bngp_data/reads/bngsa_nietinfected_2.fastq"]
SCRIPTS = "/exports/bngp_home/BNGP/"
REFGEN = "/exports/bngp_data/refgenome/lclav_genome.fa"
THREADS = 4
CHUNKS = 3_000_000


rule all:
    input:
        expand("Results/bngsa_nietinfected_{sample}.QC", sample = ['1', '2']),
        expand("Results/bngsa_nietinfected_{sample}_trimmed.fastq", sample = ['1', '2']),
        expand("Results/bngsa_nietinfected_{sample}_trimmed.QC", sample = ['1', '2']),
        "Results/Genome/Ref_Genome_Aligned.SAM"

rule QC_no_Trim:
    input:
        "/exports/bngp_data/reads/bngsa_nietinfected_{sample}.fastq",
    output:
        "Results/bngsa_nietinfected_{sample}.QC",
    shell:
        "python {SCRIPTS}DeelOpdracht1.py -i {input} -t {THREADS} -c {CHUNKS} -o {output}"

rule Trimmer_step1:
    input:
        "/exports/bngp_data/reads/bngsa_nietinfected_{sample}.fastq",
    output:
        "Results/bngsa_nietinfected_{sample}_good.fastq",
        "Results/bngsa_nietinfected_{sample}_bad.fastq",
    shell:
	    "python {SCRIPTS}DeelOpdracht2.py -i {input} -t {THREADS} -c {CHUNKS} -o Results/bngsa_nietinfected_{wildcards.sample}.fastq"

rule Trimmer_step2:
    input:
        good1 = "Results/bngsa_nietinfected_1_good.fastq",
        bad1 = "Results/bngsa_nietinfected_1_bad.fastq",
        good2 = "Results/bngsa_nietinfected_2_good.fastq",
        bad2 = "Results/bngsa_nietinfected_2_bad.fastq",
    output:
        "Results/bngsa_nietinfected_1_trimmed.fastq",
        "Results/bngsa_nietinfected_2_trimmed.fastq",
    shell:
	    "python {SCRIPTS}RemoveReads.py -i {input.bad1} {input.bad2}"

rule QC_Trim:
    input:
        "Results/bngsa_nietinfected_{sample}_trimmed.fastq",
    output:
        "Results/bngsa_nietinfected_{sample}_trimmed.QC",
    shell:
        "python {SCRIPTS}DeelOpdracht1.py -i {input} -t {THREADS} -c {CHUNKS} -o {output}"

rule IndexAlign:
    input:
        r1 = "Results/bngsa_nietinfected_1_trimmed.fastq",
        r2 = "Results/bngsa_nietinfected_2_trimmed.fastq",
    output:
        "Results/Variants/bngsa_sample.SAM"
    shell:
        "bash {SCRIPTS}DeelOpdracht4.sh -r {REFGEN} -d Results/Variants/bngsa_sample -t {THREADS} -1 {input.r1} -2 {input.r2}"

rule VCF_creation:
    input:
        "Results/Variants/bngsa_sample.SAM"
    output:
        a="Results/Variants/bngsa_sample.BAM",
        b="Results/Variants/bngsa_sample.BCF",
        c="Results/Variants/bngsa_sample.VCF",
        d="Results/Variants/bngsa_sample.mpileup",
        e="Results/Variants/bngsa_sample_sorted.BAM",
    shell:
        'bash {SCRIPTS}DeelOpdracht5_VCF.sh  -r {REFGEN} -s {input} -b {output.a} -t {THREADS}'

rule Consensus_creation:
    input:
        "Results/Variants/bngsa_sample.VCF"
    output:
        "Results/bngsa_consensus.fasta"
    shell:
        'bash {SCRIPTS}DeelOpdracht5_Consensus.sh  -r {REFGEN} -v {input} -f {output} -t {THREADS}'