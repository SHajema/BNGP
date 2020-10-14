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
        "python DeelOpdracht1.py -i {input} -t {THREADS} -c {CHUNKS} -o {output}"

rule Trimmer_step1:
    input:
        "/exports/bngp_data/reads/bngsa_nietinfected_{sample}.fastq"
    output:
        "Results/bngsa_nietinfected_{sample}_good.fastq",
        "Results/bngsa_nietinfected_{sample}_bad.fastq"
    shell:
	    "python Deelopdracht2.py -i  {input} -t {THREADS} -c {CHUNKS} -o Results/bngsa_nietinfected_{sample}.fastq"

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
	    "python RemoveReads.py -i {input.bad1} {input.bad2}"

rule QC_Trim:
    input:
        "Results/bngsa_nietinfected_{sample}_trimmed.fastq"
    output:
        "Results/bngsa_nietinfected_{sample}_trimmed.QC"
    shell:
        "python DeelOpdracht1.py -i {input} -t {THREADS} -c {CHUNKS} -o {output}"