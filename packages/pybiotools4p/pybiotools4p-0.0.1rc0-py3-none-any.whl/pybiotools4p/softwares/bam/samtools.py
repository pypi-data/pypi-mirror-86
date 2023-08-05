# AUTOGENERATED! DO NOT EDIT! File to edit: 05_samtools.ipynb (unless otherwise specified).

__all__ = ['Samtools']

# Cell

from ..base import Base, modify_cmd


# Cell

class Samtools(Base):
    def __init__(self, software, fd):
        super(Samtools, self).__init__(software)
        self._default = fd


    def cmd_version(self):
        '''
        :return:
        '''
        return 'echo {repr} ;echo $({software} 2>&1 | grep Version)  '.format(
            repr=self.__repr__(),
            software=self._software
        )

    @modify_cmd
    def cmd_faidx(self,reference):
        '''
        :param reference:
        :return:
        '''
        return r'''
{software} {faidx} {reference}
        '''.format(
            software=self._software,
            faidx=self._default['faidx'],
            **locals()
        )

    @modify_cmd
    def cmd_sam2bam(self, samtools_idx, samfile, bamfile=None):
        '''
        :param samtools_idx:
        :param samfile:
        :param bamfile:
        :return:
        '''
        if bamfile in [None,'']:
            bamfile = ''
        else:
            bamfile = '-o ' + bamfile
        return r'''
{samtools} {sam2bam_paras} {samtools_idx} {samfile} {bamfile}
            '''.format(
            sam2bam_paras=self._default['sam2bam'],
            samtools=self._software,
            **locals())

    @modify_cmd
    def cmd_sort(self, bamfile, sortbam=None):
        '''
        :return:
        '''
        if sortbam in ['',None]:
            sortbam = ''
        else:
            sortbam = '-o ' + sortbam
        return r'''
{samtools} {sort_paras} {bamfile} {sortbam}
        '''.format(
            samtools=self._software,
            sort_paras=self._default['sort'],
            **locals())

    @modify_cmd
    def cmd_index(self, bamfile):
        '''
        :param bamfile:
        :return:
        '''
        return r'''
{samtools} {index_paras} {bamfile}
            '''.format(
            samtools=self._software,
            index_paras=self._default['index'],
            **locals())

    def __repr__(self):
        return 'samtools:' + self._software

    def __str__(self):
        return 'SAM Tools provide various utilities for manipulating alignments in the SAM format, ' \
               'including sorting, merging, indexing and generating alignments in a per-position format.'
