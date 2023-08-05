#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 University of Groningen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Provides a processor that reads a PDB file.

See also
--------
:mod:`vermouth.pdb.pdb`
"""


from ..pdb import read_pdb
from .processor import Processor


class PDBInput(Processor):
    def __init__(self, filename, exclude=(), ignh=False, modelidx=0):
        super().__init__()
        self.filename = filename
        self.exclude = exclude
        self.ignh = ignh
        self.modelidx = modelidx

    def run_system(self, system):
        molecules = read_pdb(self.filename, exclude=self.exclude,
                             ignh=self.ignh, modelidx=self.modelidx)
        for molecule in molecules:
            system.add_molecule(molecule)
