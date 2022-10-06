"""
This script creates IAM users

To parse console input it uses Fire.

Info about parameters
-- filename
    provide path to the CSV file that contains user accounts data.
    Sample file you can find in
"""

from os import environ
import csv

from randpass import get_pass

import fire
import boto3
from colorama import Fore
from mail import send


TAGS = [
    {"Key": "goal", "Value": "workshops"},
]


class Accounts:
    """Manages accounts and users on AWS"""

    def __init__(self, aws_profile: str):
        self._session = boto3.session.Session(profile_name=aws_profile)
        self._client = self._session.client("iam")

    def create(self, filename: str):
        """create users in account"""
        accounts_info = self._load_accounts_info(filename)
        self._create_accounts(accounts_info)

    def assign_group(self, filename: str, group: str, boundary: str):
        """Assign groups to to all users from given file"""
        accounts_info = self._load_accounts_info(filename)
        self._assign_group_to_users(group, accounts_info, boundary)

    def _load_accounts_info(self, filename):
        info = []
        with open(filename, "r") as f_p:
            reader = csv.DictReader(f_p, delimiter=";")
            for row in reader:
                info.append(row)
        return info

    def _create_accounts(self, accounts_info: list):
        for account_info in accounts_info:
            account_id, exc = self._create_account(account_info)

    def _create_account(self, account_info: dict):
        email = account_info["Email"]
        username = email.split("@")[0]
        print(f"Creating account for {username}[{email}]")
        user, err = self._create_user(username, TAGS)
        password = get_pass(4)
        self._client.create_login_profile(
            UserName=username, Password=password, PasswordResetRequired=False
        )

        self._client.attach_user_policy(
            UserName=username, PolicyArn="arn:aws:iam::aws:policy/IAMUserChangePassword"
        )
        ak_response = self._client.create_access_key(UserName=username)
        access_key = ak_response["AccessKey"]["AccessKeyId"]
        access_secret = ak_response["AccessKey"]["SecretAccessKey"]
        template_context = {
            "username": username,
            "password": password,
            "access_key": access_key,
            "access_secret": access_secret,
        }
        self._send_mail(email, template_context)
        return user, err

    def _create_user(self, username, tags):
        path = "/workshops/001/"
        try:
            user = self._client.create_user(Path=path, UserName=username, Tags=tags)
            waiter = self._client.get_waiter("user_exists")
            waiter.wait(UserName=username, WaiterConfig={"Delay": 15, "MaxAttempts": 5})
            print(Fore.GREEN + "User created")

        except self._client.exceptions.EntityAlreadyExistsException:
            print(Fore.YELLOW + f"User already exists[{username}]")
            user = self._client.get_user(UserName=username)

        except Exception as ex:
            print(Fore.RED + "Error in creating user")
            print(ex)
            return (None, ex)
        return (user, None)

    def _assign_group_to_users(
        self, group_name: str, accounts_info: list, boundary: str = None
    ):
        for account_info in accounts_info:
            self._assign_group(group_name, account_info, boundary)

    def _assign_group(self, group_name, account_info: dict, boundary: str = None):
        email = account_info["Email"]
        username = email.split("@")[0]
        print(f"Assign group for user {username}[{email}]")
        user = self._session.resource("iam").User(username)
        user.add_group(GroupName=group_name)
        if boundary:
            self._client.put_user_permissions_boundary(
                UserName=username, PermissionsBoundary=boundary
            )

    def _send_mail(self, email, context: dict):
        content = f"""
            <h1>Siema {context['username']}!
            <h4>Dostęp do konsoli AWS:</h4>
            <ul>o
                <li>Adres do zalogowania: https://252520820660.signin.aws.amazon.com/console</li>
                <li>Twoje haslo: {context['password']}</li>
            </ul>

            <h4>Dostęp z terminala:</h4>
            <ul>
                <li>Access key: {context['access_key']}</li>
                <li>Secretkey: {context['access_secret']}</li>
            </ul>
            """
        send(email, content)
        send("kamil.waldoch@profil-software.com", content)


if __name__ == "__main__":
    """ """
    AWS_PROFILE = environ["AWS_PROFILE"]
    good_profile = input(f"Use AWS profile {AWS_PROFILE} y/n?")
    if good_profile != "y":
        exit(-1)
    accounts = Accounts(aws_profile=AWS_PROFILE)
    fire.Fire(accounts)
