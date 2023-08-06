# -*- coding: utf-8 -*-
import sys
import os
import re
import json
from json.decoder import JSONDecodeError
#from schema import Schema, And, Use, Optional, SchemaError, Regex
#from jsonschema import validate
from cerberus import Validator
import logging

from identify_logline.schema import agent_definitions_regex

# pip3 install cerberus

# run a test scenario to identify an agent from RAW log line
# echo '{"testkey": "testvalue"}' | python3 identify.py


def schema_validates(conf_schema, conf):
    try:
        conf_schema.validate(conf)
        return True
    except SchemaError:
        return False

class AnsiColor():
    header = '\033[95m'
    blue = '\033[0;34m'
    green = '\033[0;32m'
    cyan = '\033[0;36m'
    red = '\033[0;31m'
    purple = '\033[0;35m'
    brown = '\033[0;33m'
    gray = '\033[0;37m'
    dark_gray = '\033[1;30m'
    light_blue = '\033[1;34m'
    light_green = '\033[1;32m'
    light_cyan = '\033[1;36m'
    light_red = '\033[1;31m'
    light_purple = '\033[1;35m'
    yellow = '\033[1;33m'
    white = '\033[1;37m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


# define log agent definitions and a structure of log lines to match to
# currently only supports searches 1 level deep

if not os.fstat(sys.stdin.fileno()).st_size > 0:
    print(
        """missing stdin, try something like:\n"""
        """  echo '{"agentkey": "agentvalue"}' | python script.py""")
    exit()


def read_stdin():
    """ read from console stdin and return the json decode dresult
    :return: str
    """
    lines = []
    for line in sys.stdin:
        lines.append(line)
    try:
        lines = json.loads("".join(lines))
    except JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        exit()
    return lines


def predict_agent(logline):
    """
    applies a set of regex templates and determines the agent identifiers + confidence score
    if multiple regex rules apply, there will be multiple items in the return dict!
    and
    checks the cerberus schema definition to check for type/structure fingerprinting of a log
    message, this also supports multi-dimensional dictionary recursion by default
    :return: dict
    :example function output: {'heroku': {'confidence': 10}}
    """
    potential_matches = dict()
    match_counts = dict()
    schema_ok = dict()
    for agentdefinition_name, agentdefinition_struct in agent_definitions_regex.items():

        matchscore = agentdefinition_struct['confidence']
        likely_match = []
        match_counts[agentdefinition_name] = dict()
        schema_ok[agentdefinition_name] = dict()
        match_counts[agentdefinition_name]['expected'] = len(
            agentdefinition_struct.get('logline', []))
        match_counts[agentdefinition_name]['actual'] = 0
        if agentdefinition_struct.get('logline', None):
            for expected_line_key, expected_line_regex in agentdefinition_struct['logline'].items():
                for linekey, linevalue in logline.items():
                    if expected_line_key == linekey:
                        if isinstance(linevalue, str):
                            # only supports first dimensional string regex right now, hopefully recursion soon
                            if re.match(expected_line_regex, linevalue):
                                match_counts[agentdefinition_name]['actual'] += 1
                                potential_matches[agentdefinition_name] = {
                                    "confidence": matchscore}
        if agentdefinition_struct.get('schema', None):
            v = Validator()
            v.schema = agentdefinition_struct['schema']
            # permit unkown fields within schema
            v.allow_unknown = True
            if v.validate(logline, agentdefinition_struct.get('schema')):
                schema_ok[agentdefinition_name]['schema_ok'] = True
            else:
                schema_ok[agentdefinition_name]['schema_ok'] = False
        else:
            logging.info(f"Ignoring schema for {agentdefinition_name}")
            schema_ok[agentdefinition_name]['schema_ok'] = True
    # Validate our comparative values and make a judgement
    actual_matches = dict()
    for potential_match, payload in potential_matches.items():
        if not (match_counts[potential_match]['expected'] == match_counts[potential_match]['actual']):
            logging.error(f"JSON regex for {potential_match} was invalid")
        if schema_ok[potential_match]['schema_ok'] == False:
            logging.error(f"JSON schema for {potential_match} was invalid")
        if ((match_counts[potential_match]['expected'] == match_counts[potential_match]['actual']) and (schema_ok[potential_match]['schema_ok'] == True)):
            actual_matches[potential_match] = payload
    return actual_matches

def main():
    logline = read_stdin()
    predictions = predict_agent(logline)
    print("="*15)
    print("Reference line")
    print("="*15)
    print(f"{AnsiColor.red}"+json.dumps(logline, indent=3)+f"{AnsiColor.end}")

    print("="*29)
    print("Git Repo / Documentation URL")
    print("="*29)
    for agent_hint, agent_intel in predictions.items():
        agent_url = agent_definitions_regex[agent_hint].get('url', None)
        if agent_url:
            print(f"  * {AnsiColor.green}{agent_url}{AnsiColor.end}")


    print("="*29)
    print("NOTES")
    print("="*29)
    for agent_hint, agent_intel in predictions.items():
        notes = agent_definitions_regex[agent_hint].get('notes', None)
        if notes:
            print(f"{AnsiColor.gray}{notes}{AnsiColor.end}")
        else:
            print("")

    print("="*29)
    print("Implementation Example")
    print("="*29)
    for agent_hint, agent_intel in predictions.items():
        implementation_example = agent_definitions_regex[agent_hint].get('implementation_example', None)
        if implementation_example:
            print(f"{AnsiColor.gray}{implementation_example}{AnsiColor.end}")
        else:
            print("")

    print("="*18)
    print("Noteworthy Fields")
    print("="*18)
    _logtype = logline.get('_logtype', None)
    _ingester = logline.get('_ingester', None)
    noteworthy = False
    if _logtype:
        noteworthy = True
        print(f"  * logtype  = {logline['_logtype']}")
    if _ingester:
        noteworthy = True
        print(f"  * ingester = {logline['_ingester']}")
    if not noteworthy:
        print(f"{AnsiColor.dark_gray}  * Nothing to report{AnsiColor.end}")

    print("="*21)
    print("Agent Identification")
    print("="*21)
    if not predictions:
        print("Unknown")
    for agent_hint, agent_intel in predictions.items():
        print(f"  * {AnsiColor.green}{agent_hint} (confidence: {agent_intel['confidence']}){AnsiColor.end}")


