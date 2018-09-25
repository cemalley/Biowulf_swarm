# Create biowulf swarm scripts for trimmomatic, STAR, and htseq given sample names.

import os

samples = ['VJ3736_1_S16', 'VJ3736_2_S17', 'VJ3736_3_S18', 'VJ3736_4_S19', 'VJ3736_5_S20', 'VJ3736_6_S21']

# delete output files if they exist since I often rerun this script
try:
    os.remove('trim_swarm.sh')
    os.remove('STAR_swarm.sh')
    os.remove('htseq_swarm.sh')
except OSError:
    pass

for sample in samples:

    trim_command = 'java -jar $TRIMMOJAR PE -phred33 ' + sample + '_L004_R1_001.fastq.gz ' \
                   + sample + '_L004_R2_001.fastq.gz -baseout ' + sample + \
                   '.fastq.gz ILLUMINACLIP:/usr/local/apps/trimmomatic/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:30:10 LEADING:10 TRAILING:5 \
    MAXINFO:50:0.97 MINLEN:36' + "\n\n"

    print(trim_command, file=open('trim_swarm.sh', "a"))

    star_command = 'cd  /data/NCATS_ifx/data/mRNASeq/Vukasin \
      && mkdir -p bam/' + 'Sample_' + sample + ' \
      && STAR \
        --runThreadN $SLURM_CPUS_PER_TASK \
        --genomeDir /fdb/STAR_current/GENCODE/Gencode_human/release_27/genes-75 \
        --sjdbOverhang 75 \ --outSAMunmapped Within –-outFilterType BySJout \
        --outFilterMultimapNmax 20 --outFilterMismatchNmax 999 \
        --outFilterMismatchNoverLmax 0.04 --alignIntronMin 20 \
        --alignIntronMax 1000000 --alignMatesGapMax 1000000 \
        --alignSJoverhangMin 8 --alignSJDBoverhangMin 1 -- sjdbScore 1 \
        --readFilesIn /data/NCATS_ifx/data/mRNASeq/Vukasin/' + sample + '_1P.fastq.gz /data/NCATS_ifx/data/mRNASeq/Vukasin/'\
                   + sample + '_2P.fastq.gz \
        --readFilesCommand zcat \
        --outSAMtype BAM SortedByCoordinate \
        --outFileNamePrefix bam/' + 'Sample_' + sample + '/' + '_hg38' + "\n\n"

    print(star_command, file=open('STAR_swarm.sh', "a"))

    htseq_command = 'htseq-count -f bam -r pos -s no -t exon -m union /data/NCATS_ifx/data/mRNASeq/Vukasin/bam/' + sample + '_hg38Aligned.sortedByCoord.out.bam /fdb/GENCODE/Gencode_human/release_27/gencode.v27.annotation.gtf > /data/NCATS_ifx/data/mRNASeq/Vukasin/htseq/' + sample + '_htseq_counts.txt' + "\n\n"

    print(htseq_command, file=open('htseq_swarm.sh', "a"))

