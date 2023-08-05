# AUTOGENERATED! DO NOT EDIT! File to edit: 17_nanopolish.ipynb (unless otherwise specified).

__all__ = ['Nanopolish']

# Cell

import os
from ..base import Base, modify_cmd



# Cell

class Nanopolish(Base):
    def __init__(self, software, fd):
        super(Nanopolish, self).__init__(software)
        self._default = fd
        if '/' in software:
            bin = os.path.dirname(software) + '/'
        else:
            bin = ''

        self._calculate_methylation_frequency=bin + 'calculate_methylation_frequency.py'

    @modify_cmd
    def cmd_version(self):
        '''
        :return:
        '''
        return 'echo {repr} ;{software} --version'.format(
            repr=self.__repr__(),
            software=self._software
        )

    @modify_cmd
    def cmd_call_methylation(self,fastq,bam,reference,prefix):
        '''

        '''

        return r'''
{software} {call_methylation} \
        -r {fastq} \
        -b {bam} \
        -g {reference} > {prefix}_methylation_calls.tsv

{calculate_methylation_frequency} {prefix}_methylation_calls.tsv > {prefix}_methylation_frequency.tsv
        '''.format(
            software=self._software,
            call_methylation=self._default['call_methylation'],
            calculate_methylation_frequency=self._calculate_methylation_frequency,
            **locals()
        )

    @modify_cmd
    def cmd_polya(self,fastq,bam,reference,output):
        '''

        '''
        return r'''
{software} {polya} \
        -r {fastq} \
        -b {bam} \
        -g {refernece} > {output}
        '''.format(
            software=self._software,
            polya=self._default['polya'],
            **locals()
        )

    @modify_cmd
    def cmd_eventalign(self,fastq,bam,reference,output):
        '''

        '''
        return r'''
{software} {eventalign} \
    -r {fastq} \
    --bam {bam} \
    --genome {reference} > {output}
        '''.format(
            software=self._software,
            eventalign=self._default['eventalign'],
            **locals()
        )

    def __repr__(self):
        return 'nanopolish:' + self._software

    def __str__(self):
        return 'Signal-level algorithms for MinION data'