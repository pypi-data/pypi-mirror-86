# AUTOGENERATED! DO NOT EDIT! File to edit: 16_nanopolishcomp.ipynb (unless otherwise specified).

__all__ = ['Nanopolishcomp']

# Cell

import os
from ..base import Base, modify_cmd



# Cell

class Nanopolishcomp(Base):
    def __init__(self, software, fd):
        super(Nanopolishcomp, self).__init__(software)
        self._default = fd


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
    def call_eventalign_collapse(self,eventalign_file,prefix):
        '''

        '''

        return r'''
{software} {eventalign_collapse} -i {eventalign_file} \
        -p {prefix}
        '''.format(
            software=self._software,
            eventalign_collapse=self._default['eventalign_collapse'],
            **locals()
        )



    def __repr__(self):
        return 'NanopolishComp:' + self._software

    def __str__(self):
        return 'NanopolishComp is a Python3 package for downstream analyses of Nanopolish output files'