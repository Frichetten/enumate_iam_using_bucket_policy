#!/usr/bin/env python3
import boto3, botocore, argparse

parser = argparse.ArgumentParser(description='Enumerate IAM/Users of an AWS account. You must provide your OWN AWS account and bucket')
parser.add_argument('--id', required=True, help="The account id of the target account")
parser.add_argument('--my_bucket', required=True, help="The bucket used for testing (belongs to you)")
parser.add_argument('--wordlist', help="Wordlist containers user/role names")

# Role or User
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--role', action="store_true", help="Search for a IAM Role")
group.add_argument('--user', action="store_true", help="Search for a IAM User")
args = parser.parse_args()

account_id = args.id
bucket_name = args.my_bucket

session = boto3.session.Session()
s3 = session.resource('s3')
bucket_policy = s3.BucketPolicy(bucket_name)

if args.wordlist:
    wordlist = args.wordlist
else:
    wordlist = 'default-word-list.txt'

if args.role:
    principal = "role"
else:
    principal = "user"

with open(wordlist, 'r') as r:
    for name in r:
        policy_json = '{"Version":"2012-10-17","Statement":[{"Sid":"Example permissions","Effect":"Deny","Principal":{"AWS":"arn:aws:iam::'+ account_id +':'+ principal +'/'+ name[:-1] +'"},"Action":["s3:ListBucket"],"Resource":"arn:aws:s3:::'+ bucket_name +'"}]}'

        try:
            bucket_policy.put(Policy=policy_json)
            print("%s Found!: %s" % (principal, name[:-1]))
        except botocore.exceptions.ClientError as error:
            None
