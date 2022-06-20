"""
This script creates users accounts in AWS organization
and moves account to provided organization unit(OU).

To parse console input it uses Fire.

Info about parameters
-- filename
    provide path to the CSV file that contains user accounts data.
    Sample file you can find in 
-- root_id 
    Prganization root id. All the accounts are created in the root by default.  
-- ou_id 
    Organization unit id. 
    Indicates the OU into which we want to assign newly created accounts
"""

from os import environ
import csv

import fire
import boto3

from botocore.exceptions import WaiterError
from botocore.waiter import WaiterModel
from botocore.waiter import create_waiter_with_client


class Accounts:
    def __init__(self, aws_profile):
        self._session = boto3.session.Session(profile_name=aws_profile)
        self._organizations = self._session.client("organizations")

    def create(self, filename: str):
        accounts_info = self._load_accounts_info(filename)
        self._create_accounts(accounts_info)

    def _load_accounts_info(self, filename):
        info = []
        with open(filename, "r") as fp:
            reader = csv.DictReader(fp, delimiter=";")
            for row in reader:
                info.append(row)
        return info

    def _create_accounts(self, accounts_info: list):
        for account_info in accounts_info:
            account_id, exc = self._create_account(account_info)

    def _create_account(self, account_info):
        account = None
        print(f"Creating account for {account_info['Email']}")

        try:
            account = self._organizations.create_account(**account_info)
        except Exception as ex:
            print(f"Error in creating account request")
            print(ex)
            return (None, e)

        create_request_id = account.get("CreateAccountStatus").get("Id")
        # create account succeded, wait for status change
        try:
            waiter = self._create_accounts_waiter()
            waiter.wait(CreateAccountRequestId=create_request_id)
            print("Account created!!")
        except WaiterError as e:
            print("Error on creating accunt")
            print(e)
            return (None, e)
        response = self._organizations.describe_create_account_status(
            CreateAccountRequestId=create_request_id
        )
        account_id = response.get("CreateAccountStatus").get("AccountId")
        print("Account status:")
        print(response)
        return (account_id, None)

    def _create_accounts_waiter(self):
        delay = 3
        max_attempts = 30
        waiter_name = "create-account-waiter"
        waiter_config = {
            "version": 2,
            "waiters": {
                "create-account-waiter": {
                    "operation": "DescribeCreateAccountStatus",
                    "delay": delay,
                    "maxAttempts": max_attempts,
                    "acceptors": [
                        {
                            "matcher": "path",
                            "expected": "IN_PROGRESS",
                            "argument": "CreateAccountStatus.State",
                            "state": "retry",
                        },
                        {
                            "matcher": "path",
                            "expected": "SUCCEEDED",
                            "argument": "CreateAccountStatus.State",
                            "state": "success",
                        },
                        {
                            "matcher": "path",
                            "expected": "FAILED",
                            "argument": "CreateAccountStatus.State",
                            "state": "failure",
                        },
                    ],
                },
            },
        }

        waiter_model = WaiterModel(waiter_config)
        custom_waiter = create_waiter_with_client(
            waiter_name=waiter_name,
            waiter_model=waiter_model,
            client=self._organizations,
        )
        return custom_waiter


if __name__ == "__main__":
    """root id: r-3ifs
    workshops ou id: ou-3ifs-sjkjm04e
    """
    AWS_PROFILE = environ["AWS_PROFILE"]
    accounts = Accounts(aws_profile=AWS_PROFILE)
    fire.Fire(accounts)
