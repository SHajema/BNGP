SAMPLES = ["/exports/bngp_data/reads/bngsa_nietinfected_1.fastq", "/exports/bngp_data/reads/bngsa_nietinfected_2.fastq"]


rule all:
    input:
        expand("/exports/bngp_data/reads/bngsa_nietinfected_{sample}.fastq", sample=[1, 2])

rule QC_no_Trim:
    input:
        "/exports/bngp_data/reads/bngsa_nietinfected_{sample}.fastq"
    output:
        "bngsa_nietinfected_{sample}.QC"
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
        rules.Trimmer.output
    output:
        "Results/bngsa_nietinfected_{sample}_trimmed.qc"