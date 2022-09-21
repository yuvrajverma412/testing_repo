from __future__ import annotations
from typing import Union
from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation

def getConfig(config_file: Union[str, Path]='config.ini') -> ConfigParser:

    '''
        Function to load configuration files.

        Attributes:
        --------------
        config_file: str : default="config.ini"

        Returns:
        ---------------
        A config parser object
        
    '''

    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(config_file)

    return parser
