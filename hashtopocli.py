#!/usr/bin/env python

import argparse
import datetime as dt
import re
import sys
import os

import requests
import yaml


def message(msg, title=False, stat=False, quiet=False):
    """
    Prints formatted text to CLI
    """

    class Colors:
        GREEN = "\033[32m"
        ENDC = '\033[0m'
        BOLD = '\033[1m'

    if title:
        if not quiet:
            print(f'{Colors.GREEN}{Colors.BOLD}[{str(dt.datetime.now().strftime("%H:%M:%S"))}] {msg}{Colors.ENDC}')
    elif stat:
        print(f'{msg}')


def validate_user_input(user_input_str):
    """
    Validates user input against an allowlist
    @param user_input_str: input string
    @return: string if valid otherwise break
    """

    if bool(re.match('^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890:/.?]+$', str(user_input_str))):
        return user_input_str
    else:
        message('Error validating user input!', title=True, quiet=args.quiet)
        exit()


class HashtopolisAuth:
    """
    Handles auth and requests to API
    """
    def __init__(self, url, token) -> None:
        self.apiUrl = self.validate_url(url)
        self.apiToken = validate_user_input(token)
        self.apiEndpoint = self.validate_api(url + '/api/user.php')
        self.test_auth()

    @staticmethod
    def validate_url(url):
        """
        Validates that the url is correct
        @param url: URL to test
        @return: url if valid
        """
        validate_user_input(url)
        response = requests.get(url=url)
        if response.status_code != 200:
            message('Error validating URL!', title=True, quiet=args.quiet)
            exit()
        return url

    @staticmethod
    def validate_api(url):
        """
        Validates that the API exists for the URL
        @param url: the URL to test with the API endpoint
        @return: url if valid
        """
        validate_user_input(url)
        data = {'section': 'test', 'request': 'connection'}
        response = requests.post(url, json=data)
        if response.json()['response'] != 'SUCCESS':
            message('Error validating API endpoint!', title=True, quiet=args.quiet)
            exit()
        return url

    def test_auth(self):
        """
        Tests authentication to the API
        """
        data = {'section': 'test', 'request': 'access', 'accessKey': self.apiToken}
        response = requests.post(self.apiEndpoint, json=data)
        if response.json()['response'] != 'OK':
            message('Error authenticating to the API!', title=True, quiet=args.quiet)
            exit()

    def api_request(self, data, silent=False):
        """
        Main function to send API requests
        @param data: JSON body to post
        @param silent: controls if output should include timestamp
        @return: JSON response
        """
        data['accessKey'] = self.apiToken
        response = requests.post(self.apiEndpoint, json=data)
        if not silent:
            message(f'Requesting {data["request"]}...', title=True, quiet=args.quiet)
        return response.json()


class HashtopolisApi:
    """
    Handles the API call schemas
    """
    def __init__(self, auth_obj) -> None:
        self.api = auth_obj

    def get_hash(self, input_hash):
        """
        Search if a hash is found on the server. This searches on all hashlists which the user has access to.
        @param input_hash: single hash to check
        """
        validate_user_input(input_hash)
        data = {
            "section": "hashlist",
            "request": "getHash",
            "hash": str(input_hash)
        }
        response = self.api.api_request(data, silent=True)
        try:
            message(response['hash'] + ':' + response['plain'], stat=True)
        except KeyError:
            pass

    def get_cracked(self, input_id):
        """
        Retrieve all cracked hashes of a given hashlist.
        @param input_id: input hashlistId to search
        """
        validate_user_input(input_id)
        data = {
            "section": "hashlist",
            "request": "getCracked",
            "hashlistId": str(input_id)
        }
        response = self.api.api_request(data, silent=True)
        try:
            for itr in response['cracked']:
                message(itr['hash'] + ':' + itr['plain'], stat=True)
        except KeyError:
            pass

    def get_task_cracked(self, input_id):
        """
        Retrieve all cracked hashes of a given task.
        @param input_id: input taskId to search
        """
        validate_user_input(input_id)
        data = {
            "section": "task",
            "request": "getCracked",
            "taskId": str(input_id)
        }
        response = self.api.api_request(data, silent=True)
        try:
            for itr in response['cracked']:
                message(itr['hash'] + ':' + itr['plain'], stat=True)
        except KeyError:
            pass

    def get_hashlist(self, input_id):
        """
        Get information about a specific hashlist.
        @param input_id: input hashlistId to search
        """
        validate_user_input(input_id)
        data = {
            "section": "hashlist",
            "request": "getHashlist",
            "hashlistId": str(input_id)
        }
        response = self.api.api_request(data, silent=True)
        return response

    def list_hashlist(self):
        """
        Lists all the hashlists
        """
        data = {
            "section": "hashlist",
            "request": "listHashlists"
        }
        response = self.api.api_request(data)
        for itr in response['hashlists']:
            metadata = self.get_hashlist(itr["hashlistId"])
            message(
                f'List[{itr["hashlistId"]}] Type[{itr["hashtypeId"]}] -> {itr["name"]} cracked {str(metadata["cracked"]) + "/" + str(itr["hashCount"])}',
                stat=True)

    def import_supertask(self, input_lst, name):
        """
        Create a supertask configuration with a given list of masks.
        @param input_lst: input list of masks to create the task with
        @param name: name to create the supertask as
        """
        if isinstance(input_lst, list):
            for m in input_lst: validate_user_input(m)
            validate_user_input(name)
        else:
            exit()
        message(f'Creating SuperTask: {name}:', title=True, quiet=args.quiet)
        for itr in input_lst:
            message(itr, stat=True)
        data = {
            "section": "supertask",
            "request": "importSupertask",
            "name": name,
            "isCpuOnly": False,
            "isSmall": False,
            "masks": input_lst,
            "optimizedFlag": True,
            "crackerTypeId": 1,
            "benchmarkType": "speed",
            "accessKey": "mykey"
        }
        response = self.api.api_request(data)
        message(response['response'], stat=True)


if __name__ == '__main__':
    config = yaml.safe_load(open(os.path.join(sys.path[0], 'config.yml')))
    userAuth = HashtopolisAuth(config['url'], config['key'])
    apiObj = HashtopolisApi(userAuth)

    parser = argparse.ArgumentParser(description='CLite for Hashtopolis')
    parser.add_argument("-i", "--input", action="store", default=False, help='Input list of hashes or single hash')
    parser.add_argument("-q", "--quiet", action="store_true", default=False, help="Hides titles")
    parser.add_argument("-l", "--list", action="store_true", default=False, help="Lists available hashlists")
    parser.add_argument("-c", "--cracked", action="store", default=False, help="Gets cracks from a hashlistId")
    parser.add_argument("-t", "--task", action="store", default=False, help="Gets cracks from a taskId")
    parser.add_argument("-m", "--masks", action="store", default=False,
                        help="Imports a list of Hashcat masks to a new super task")
    args = parser.parse_args()

    if not sys.stdin.isatty() and not args.input:
        args.input = sys.stdin.read().rstrip()

    if args.input:
        try:
            with open(args.input) as file:
                while i := file.readline().rstrip():
                    validate_user_input(i)
                    apiObj.get_hash(i)
        except FileNotFoundError:
            for i in args.input.split('\n'):
                input_str = validate_user_input(str(i))
                apiObj.get_hash(input_str)
    elif args.list:
        apiObj.list_hashlist()
    elif args.cracked:
        try:
            with open(args.cracked) as file:
                while i := file.readline().rstrip():
                    validate_user_input(i)
                    apiObj.get_cracked(i)
        except FileNotFoundError:
            for i in args.cracked.split('\n'):
                input_str = validate_user_input(str(i))
                apiObj.get_cracked(input_str)
    elif args.taskcracked:
        try:
            with open(args.taskcracked) as file:
                while i := file.readline().rstrip():
                    validate_user_input(i)
                    apiObj.get_task_cracked(i)
        except FileNotFoundError:
            for i in args.taskcracked.split('\n'):
                input_str = validate_user_input(str(i))
                apiObj.get_task_cracked(input_str)
    elif args.masks:
        try:
            mask_lst = []
            with open(args.masks) as file:
                while i := file.readline().rstrip():
                    validate_user_input(i)
                    if bool(re.match('^[ludhsabH?]+$', str(i))):
                        mask_lst.append(i)
            apiObj.import_supertask(mask_lst, validate_user_input(args.masks))
        except FileNotFoundError:
            message('No input file found!', title=True)
            exit()
