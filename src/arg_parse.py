from __future__ import annotations
from typing import Union, Dict, Any
from pathlib import Path
import argparse
from argparse import Namespace, ArgumentParser
from .io import loadJsonFromFile


def createIntegrationArgumentParser(parser: ArgumentParser , default_config: Dict[str, str]) -> None:
    
    '''
        Function to create subparser for data integration module.

        Attribures:
        -------------
        parser: ArgumentParser : An argument parser object that may be top level parser or a subparser.
        default_config: Dict : A dictionary containing all default config parameters.

    '''

    parser.add_argument('-A', '--algorithm', default=default_config['algorithm'], type=str, dest='integration_algorithm')
    


def createPreprocessArgumentParser(parser: ArgumentParser, default_config: Dict[str, str], global_config:Dict[str, Any]) -> None:

    '''
        Function to create subparser for data integration module.

        Attribures:
        -------------
        parser: ArgumentParser : An argument parser object that may be top level parser or a subparser.
        default_config: Dict : A dictionary containing all default config parameters.

    '''

    registry_file = loadJsonFromFile(global_config['JSON']['JSON_PROCESSOR_REGISTRY'])[0]
    preprocessors = list(registry_file.keys())

    registry_convert_file = loadJsonFromFile(global_config['JSON']['JSON_FORMAT_REGISTRY'])[0]
    output_formats = list(registry_convert_file.keys())

    parser.add_argument('-c', '--cellline', action='store_true', dest='preprocess_cellline')
    parser.add_argument('-g', '--genename', action='store_true', dest='preprocess_genename')
    parser.add_argument('-p', '--process', nargs='+', choices=preprocessors, dest='datasets')
    parser.add_argument('-f', '--format', nargs='+', choices=output_formats, dest='formats')
    parser.add_argument('-i', '--input', dest='input_file')
    parser.add_argument('-o', '--output', dest='output_file')


def createArgumentParser(default_config_file: Union[str, Path], global_config:Dict[str, Any]) -> Namespace:

    '''
        Function to create command line argument

        Attributes:
        -------------
        default_config_file: str|Path : JSON file containing default argument mapping.

        Returns:
        -------------
        Parsed command line arguments as argparse.Namespace.

    '''

    default_configurations = loadJsonFromFile(data_file=default_config_file)[0]

    parser = ArgumentParser('Command line arguments')
    subparsers = parser.add_subparsers(help='sub-command help')

    preprocess_parser = subparsers.add_parser('preprocess', help='Preprocess parser')
    createPreprocessArgumentParser(preprocess_parser, default_configurations['preprocess'], global_config)

    format_parser = subparsers.add_parser('format', help='Format parser')
    createPreprocessArgumentParser(format_parser, default_configurations['format'], global_config)

    integration_parser = subparsers.add_parser('integration', help='Integration parser')
    createIntegrationArgumentParser(integration_parser, default_configurations['integration'])


    return parser.parse_args()
    
