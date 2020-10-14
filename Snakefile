SAMPLES = ["/exports/bngp_data/reads/bngsa_nietinfected_1.fastq", "/exports/bngp_data/reads/bngsa_nietinfected_2.fastq"]
THREADS = 4
CHUNKS = 3_000_000

rule all:
    input:
        expand("Results/bngsa_nietinfected_{sample}.QC", sample = ['1', '2']),
        expand("Results/bngsa_nietinfected_{sample}_trimmed.fastq", sample = ['1', '2']),
        expand("Results/bngsa_nietinfected_{sample}_trimmed.QC", sample = ['1', '2']),

rule QC_no_Trim:
    input:
        "/exports/bngp_data/reads/bngsa_nietinfected_{sample}.fastq"
    output:
        "Results/bngsa_nietinfected_{sample}.QC"
    shell:
        "echo 'hallo'"

rule Trimmer:
    input:
        "/exports/bngp_data/reads/bngsa_nietinfected_{sample}.fastq"
    output:
        "Results/bngsa_nietinfected_{sample}_trimmed.fastq"
    shell:
	    "time python"

rule QC_Trim:
    input:
        "Results/bngsa_nietinfected_{sample}_trimmed.fastq"
    output:
        "Results/bngsa_nietinfected_{sample}_trimmed.qc"