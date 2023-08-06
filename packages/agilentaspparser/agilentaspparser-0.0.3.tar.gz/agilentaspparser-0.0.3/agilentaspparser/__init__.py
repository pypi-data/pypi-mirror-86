#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:48:09 2020

@author: gonik
"""
import os
import pandas as pd 
import numpy as np
import csv

class spectrum():
    def __init__(self):
        self.name = 0
        self.wavenumber = []
        self.transmittance = 0
        self.dict = 0 
        self.file = 0
    def __len__(self):
        return len(self.transmittance)
    def load_files(self, file):
        self.name = file[:-4]
        self.file = file
        self.parse_file()

    def parse_file(self):
        with open(self.file, 'r') as f:
            conv = [int, float, float]
            reader = csv.reader(f)
            param = [con(next(reader)[0]) for con,i in zip(conv,range(3))]
            trash = [next(reader) for i in range(3)]
            self.wavenumber = np.linspace(param[1], param[2], int(param[0]))
            self.transmittance = [float(line[0]) for line in reader]

    def as_pandas(self):
        return pd.Series(data = self.transmittance, index = self.wavenumber)
    def as_dict(self):
        return {'wavenumber': self.wavenumber, 'transmittance': self.transmittance}
    def as_array(self):
        return np.array((self.wavenumber, self.transmittance))

def load_file(file):
    obj = spectrum()
    obj.load_files(file)    
    return obj

class spectra(spectrum):
    def __init__(self):
        super().__init__()
        self.index  = []
        self.columns = {}
        self.spectra_list = 0
        self.name_list = None
    def __iter__(self):
        return self.spectra_list.__iter__()
    def __len__(self):
        return len(self.spectra_list)
    
    def rename(self, ft):
        for sp, name in zip(self.spectra_list, self. name_list):
            sp.name = name[:-len(ft)] 
        
    def import_dir(self,directory, ft = '.asp'):
        file_list = [file for file in os.listdir(directory) if ft in file[-len(ft):]]
        path_list = [os.path.join(directory, file) for file in file_list ]
        self.name_list = file_list.copy()
        self.spectra_list = [load_file(file) for file in path_list]
        self.rename(ft = ft)
        self.columns =  {sp.name:sp.transmittance for sp in self.spectra_list}
        self.index = np.array(self.spectra_list[0].wavenumber)

    def import_list(self, file_list):
        self.spectra_list = [load_file(file) for file in file_list]
        self.columns =  {sp.name:sp.transmittance for sp in self.spectra_list}
        self.index = np.array(self.spectra_list[0].wavenumber)

        
    def as_pandas(self):
        return pd.DataFrame(data = self.columns, index = self.index)
    def as_array(self):
        return np.array(self.index, self.columns)
    def as_dict(self):
        full_dict = self.columns.copy()
        full_dict['wavenumber'] = self.index
        return full_dict
    def export_csv(self, filename):
        self.as_pandas().to_csv(filename + '.csv')
    
        
def load_dir(directory):
    obj_sa = spectra()
    obj_sa.import_dir(directory)
    return obj_sa
def load_list(file_list):
    obj_sa = spectra()
    obj_sa.import_list(file_list)
    return obj_sa



