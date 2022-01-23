import boto3
session = boto3.session.Session(profile_name='default')

import json

f = open('C:\\temp\managed_list_of_accounts.json')
data = json.load(f)
for i in data['accounts']:
    print(i)
    try:
        sts_client = boto3.client('sts')
        assumed_role_object=sts_client.assume_role(
            RoleArn="arn:aws:iam::" + i + ":role/Automation",
            RoleSessionName="AssumeRoleSessionAutomation"
        )
        print(assumed_role_object)
        credentials=assumed_role_object['Credentials']

        iam = boto3.client(
            'iam',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )
    except:
        break

    print("starting cleanup in account: " + i)
    response = iam.list_groups()
    for group in response['Groups']:
        group_details = iam.get_group(GroupName=group['GroupName'])
        for user in group_details['Users']:
            if "dev" in group['GroupName']:
                dev_users = (user['UserName'])
                dev_group = (group['GroupName'])
                print(dev_users)
                print(dev_group)
                for users in dev_group:
                    response_remove_users = iam.remove_user_from_group(
                        GroupName=dev_group,
                        UserName=dev_users,
                    )
                print(response_remove_users)


        if "dev" in group['GroupName']:
            dev_group = (group['GroupName'])
            global policy_names
            global arn
            for group in dev_group:
                print(dev_group)
                attached_group_policies = (iam.list_attached_group_policies(GroupName=dev_group)['AttachedPolicies'])
                print(attached_group_policies)
                for policy in attached_group_policies:
                    arn = policy['PolicyArn']
                    response_remove_polices = iam.detach_group_policy(
                            GroupName=dev_group,
                            PolicyArn=arn,
                    )
                    print(response_remove_polices)
            response_delete_group = iam.delete_group(
                GroupName=dev_group
            )
            print(response_delete_group)


    response_dev_iam_users = iam.list_users()
    for iam_user in response_dev_iam_users['Users']:
        if "dev" in iam_user['UserName']:
            dev_user = iam_user['UserName']
            print(dev_user)
            global policy_names
            global iam_arn
            attached_user_policies = (iam.list_attached_user_policies(UserName=dev_user)['AttachedPolicies'])
            print(attached_user_policies)
            for policy in attached_user_policies:
                iam_arn = policy['PolicyArn']
                response_remove_user_polices = iam.detach_user_policy(
                    UserName=dev_user,
                    PolicyArn=iam_arn,
                )
                print(response_remove_user_polices)
            try:
                response_delete_iam_user = iam.delete_user(
                    UserName=dev_user
                )
                print(response_delete_iam_user)
            except:
                print("user has keys, ignore: " + dev_user)
                pass
