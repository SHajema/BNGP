rule QC:
    input: "/exports/bngp_data/reads/bngsa_nietinfected_1.fastq"
    shell:
        "echo 'hallo'"


rule Trimmer:
    input: "/exports/bngp_data/reads/bngsa_nietinfected_1.fastq"
    output: "Results/bngsa_nietinfected_1_trimmed.fastq"
    shell:
	"time python"
