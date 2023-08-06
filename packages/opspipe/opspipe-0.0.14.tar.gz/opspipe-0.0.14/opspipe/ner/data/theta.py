# -*- coding: utf-8 -*-
import json,os
from pathlib import Path
from ...utils import read_json 
from ..data.base import Base

class Theta(Base):
    def __init__(self, data = None): 
        Base.__init__(self, data)  
        #self.data = data
    
    def read(self,path):  
        strjson = read_json(path)
        
        print(path)
        
    def converfrom(self,fun):
        self.data = fun.data
    
    def save(self,path):
        assert self.data == None
        print(path)
        
    