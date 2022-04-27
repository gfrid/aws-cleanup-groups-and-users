import boto3
import botocore
session = boto3.session.Session(profile_name='default')

import json

f = open('C:\\managed.json')
data = json.load(f)
for i in data['accounts']:
    print(i)
    try:
        sts_client = boto3.client('sts')
        assumed_role_object=sts_client.assume_role(
            RoleArn="arn:aws:iam::" + i + ":role/IT_Automation",
            RoleSessionName="AssumeRoleSession"
        )
        print(assumed_role_object)
        credentials=assumed_role_object['Credentials']

        iam = boto3.client(
            'iam',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )
    except Exception as eee:
        print(eee)
        continue

    #iam = boto3.client('iam')

    print("starting cleanup in account: " + i)
    response = iam.list_groups()
    for group in response['Groups']:
        group_details = iam.get_group(GroupName=group['GroupName'])
        for user in group_details['Users']:
            #print(" - ", user['UserName'])
            if "test" in group['GroupName']:
                test_users = (user['UserName'])
                test_group = (group['GroupName'])
                print(test_users)
                print(test_group)
                for users in test_group:
                    response_remove_users = iam.remove_user_from_group(
                        GroupName=test_group,
                        UserName=test_users,
                    )
                print(response_remove_users)


        if "test" in group['GroupName']:
            test_group = (group['GroupName'])
            global policy_names
            global arn
            for group in test_group:
                print(test_group)
                attached_group_policies = (iam.list_attached_group_policies(GroupName=test_group)['AttachedPolicies'])
                print(attached_group_policies)
                for policy in attached_group_policies:
                    arn = policy['PolicyArn']
                    try:
                        response_remove_polices = iam.detach_group_policy(
                                GroupName=test_group,
                                PolicyArn=arn,
                        )
                    except Exception as eee:
                        print(eee)
                        continue
                    print(response_remove_polices)
            try:
                response_delete_group = iam.delete_group(
                    GroupName=test_group
                )
                print(response_delete_group)
            except Exception as eee:
                print(eee)
                continue


    response_test_iam_users = iam.list_users()
    for iam_user in response_test_iam_users['Users']:
        if "test" in iam_user['UserName']:
            test_user = iam_user['UserName']
            print(test_user)
            global policy_names
            global iam_arn
            access_key_id = None
            list_access_keys_to_remove = []
            attached_user_policies = (iam.list_attached_user_policies(UserName=test_user)['AttachedPolicies'])
            print(attached_user_policies)
            for policy in attached_user_policies:
                iam_arn = policy['PolicyArn']
                response_remove_user_polices = iam.detach_user_policy(
                    UserName=test_user,
                    PolicyArn=iam_arn,
                )
                print(response_remove_user_polices)

            try:
                res_keys = iam.list_access_keys(
                    UserName=test_user,
                    MaxItems=4)
                for key in res_keys['AccessKeyMetadata']:
                     if 'AccessKeyId' in key:
                         access_key_id = key['AccessKeyId']
                         list_access_keys_to_remove.append(access_key_id)
            except Exception as eee:
                print(eee)
                print("An error occurred while listing access keys")
            try:
                for access_key_id in list_access_keys_to_remove:
                    print('Access key {0} needs to be removed'.format(access_key_id))
                    response_delete_keys = iam.delete_access_key(
                        UserName=test_user,
                        AccessKeyId=access_key_id
                    )
                    print(response_delete_keys)
            except Exception as eee:
                print(eee)
                print("something_went_wrong " + test_user)
            try:
                response_delete_iam_user = iam.delete_user(
                    UserName=test_user
                )
                print(response_delete_iam_user)
            except Exception as eee:
                print(eee)
                continue
