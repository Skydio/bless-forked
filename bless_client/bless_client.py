#!/usr/bin/env python

"""bless_client
A sample client to invoke the BLESS Lambda function and save the signed SSH Certificate.

Usage:
  bless_client.py region lambda_function_name requesting_user remote_usernames
  <id_rsa.pub to sign> <output id_rsa-cert.pub>

    region: AWS region where your lambda is deployed.

    lambda_function_name: The AWS Lambda function's alias or ARN to invoke.

    requesting_user: The user requesting the certificate.

    remote_usernames: Comma-separated list of username(s) or authorized principals on the remote
    server that will be used in the SSH request.  This is enforced in the issued certificate.

    id_rsa.pub to sign: The id_rsa.pub that will be used in the SSH request.  This is
    enforced in the issued certificate.

    output id_rsa-cert.pub: The file where the certificate should be saved.  Per man SSH(1):
        "ssh will also try to load certificate information from the filename
        obtained by appending -cert.pub to identity filenames" e.g.  the <id_rsa.pub to sign>.
"""
import json
import os
import stat
import sys

import boto3


def main(argv):
    if len(argv) < 9 or len(argv) > 10:
        print(
            'Usage: bless_client.py region lambda_function_name requesting_user '
            'remote_usernames <id_rsa.pub to sign> '
            '<output id_rsa-cert.pub> [kmsauth token]')
        return -1

    region, lambda_function_name, requesting_user, remote_usernames, \
        public_key_filename, certificate_filename = argv[:6]

    with open(public_key_filename, 'r') as f:
        public_key = f.read().strip()

    payload = {'requesting_user': requesting_user, 'remote_usernames': remote_usernames, 
               'public_key_to_sign': public_key}

    if len(argv) == 10:
        payload['kmsauth_token'] = argv[9]

    payload_json = json.dumps(payload)

    print('Executing:')
    print('payload_json is: \'{}\''.format(payload_json))
    lambda_client = boto3.client('lambda', region_name=region)
    response = lambda_client.invoke(FunctionName=lambda_function_name,
                                    InvocationType='RequestResponse', LogType='None',
                                    Payload=payload_json)
    print('{}\n'.format(response['ResponseMetadata']))

    if response['StatusCode'] != 200:
        print('Error creating cert.')
        return -1

    payload = json.loads(response['Payload'].read())

    if 'certificate' not in payload:
        print(payload)
        return -1

    cert = payload['certificate']

    with os.fdopen(os.open(certificate_filename, os.O_WRONLY | os.O_CREAT, 0o600),
                   'w') as cert_file:
        cert_file.write(cert)

    # If cert_file already existed with the incorrect permissions, fix them.
    file_status = os.stat(certificate_filename)
    if 0o600 != (file_status.st_mode & 0o777):
        os.chmod(certificate_filename, stat.S_IRUSR | stat.S_IWUSR)

    print('Wrote Certificate to: ' + certificate_filename)


if __name__ == '__main__':
    main(sys.argv[1:])
