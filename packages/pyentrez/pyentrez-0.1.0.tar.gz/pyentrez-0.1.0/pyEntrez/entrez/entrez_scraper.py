# Core Python Utils
import os, sys, inspect

# Biopython tools
from Bio import Entrez
from Bio import Medline

# Logger
from loguru import logger
from pyEntrez.utils import logger_utils as lu


class Scraper:
    def __init__(self):
        self.email          = str(os.environ['PYENT_EMAIL'])
        self.db             = str(os.environ['PYENT_DB'])
        self.sort           = str(os.environ['PYENT_SORT'])
        self.retmax         = int(os.environ['PYENT_RETMAX'])
        self.retmode        = str(os.environ['PYENT_RETMODE'])
        self.rettype        = str(os.environ['PYENT_RETTYPE'])
        self.term           = None
        logger.info(f'{self.email} {self.db} {self.sort} {self.retmax} {self.retmode} {self.rettype}')
        
    def search(self):
        """
        Takes CLI and config args to build the NCBI request handle and then calls the Fetch function.
        """
        Entrez.email = self.email
        handle = Entrez.esearch(db=self.db, sort=self.sort, retmax=self.retmax, retmode=self.retmode, term=self.term)
        results = Entrez.read(handle)
        self.id_list = results['IdList']
        return self.id_list
        

    def fetch(self):
        self.ids = ','.join(self.id_list)
        Entrez.email = self.email
        handle = Entrez.efetch(db=self.db,retmode=self.retmode,id=self.ids, rettype=self.rettype)
        results = Medline.parse(handle)
        results = list(results)
        return results