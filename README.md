# aws_cleanup_groups_and_users
Python script to remove AWS Groups and Users attached to them

what it does
- Lists groups, users and policies
- Removes users from group
- Removes attached policies
- Removes group
- Removes user policies
- Removes user

Script uses a JSON file with AWS Account numbers as bellow, you can modify it and build other logic if needed.

{
	"accounts": [
		"XXXXXXXXXXX1",
		"XXXXXXXXXXX2"
	],
	"Description": test,
	"success": true
}

