import time
from datetime import datetime
import os
import glob
from pathlib import Path
import csv
from urllib.parse import urlparse
import subprocess
import string 
import random
import math

import ipyvuetify as v
import pandas as pd

from ..sepalwidgets import SepalWidget

def hide_component(widget):
    """hide a vuetify based component"""
    if isinstance(widget, SepalWidget):
        widget.hide()
    elif not 'd-none' in str(widget.class_):
        widget.class_ = str(widget.class_).strip() + ' d-none'
        
    return

def show_component(widget):
    """show a vuetify based component"""
    if isinstance(widget, SepalWidget):
        widget.show()
    elif 'd-none' in str(widget.class_):
        widget.class_ = widget.class_.replace('d-none', '')
        
    return 

def create_FIPS_dic():
    """create the list of the country code in the FIPS norm using the CSV file provided in utils
        
    Returns:
        fips_dic (dic): the country FIPS_codes labelled with english country names
    """
    
    # file path
    path = os.path.join(os.path.dirname(__file__), 'country_code.csv')
    
    # get the df and sort by country name
    df = pd.read_csv(path).sort_values(by=['country_na'])
    
    # create the dict
    fip_dic = {row['country_na'] : row['FIPS 10-4'] for i, row in df.iterrows()}
        
    return fip_dic

def get_iso_3(fips_code):
    """return the iso_3 code of a fips country code use the fips_code if the iso-3 is not available"""
    
    #file path
    path = os.path.join(os.path.dirname(__file__), 'country_code.csv')
    
    # get the df
    df = pd.read_csv(path)
    
    row = df[df['FIPS 10-4'] == fips_code]
    
    code = fips_code
    if len(row):
        code = row['ISO 3166-1 alpha-3'].values[0]
        
    return code
    
def create_download_link(pathname):
    """return a clickable link to download the pathname target"""
    
    result_path = os.path.expanduser(pathname)
    home_path = os.path.expanduser('~')
    download_path='/'+os.path.relpath(result_path,home_path)
    
    link = "/api/files/download?path={}".format(download_path)
    
    return link

def is_absolute(url):
    """ check if the given url is an absolute or relative path"""
    return bool(urlparse(url).netloc)

def launch(command, output=None):
    """launch the command and exit the output in a su.displayIO"""
    
    kwargs = {
        'args' : command,
        'cwd' : os.path.expanduser('~'),
        'stdout' : subprocess.PIPE,
        'stderr' : subprocess.PIPE,
        'universal_newlines' : True
    }
    
    output_txt = ''
    with subprocess.Popen(**kwargs) as p:
        for line in p.stdout:
            output_txt += line + '\n'
            if output:
                output.add_live_msg(line)
    
    return output_txt

def random_string(string_length=3):
    """Generates a random string of fixed length. 
    Args:
        string_length (int, optional): Fixed length. Defaults to 3.
    Returns:
        str: A random string
    """
    # random.seed(1001)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))

def get_file_size(filename):
    """return the file size as string of 2 digit in the adapted scale (B, KB, MB....)"""
    
    file_size = Path(filename).stat().st_size
    
    if file_size == 0:
        return "0B"
    
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    
    i = int(math.floor(math.log(file_size, 1024)))
    s = file_size / math.pow(1024, i)
        
    return '{:.1f} {}'.format(s, size_name[i])