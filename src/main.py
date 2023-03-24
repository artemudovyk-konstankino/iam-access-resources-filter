def find_allowed_resources(policies: list[dict], target_action: str) -> set[str]:
    allowed_resources = []

    for policy in policies:
        if policy["Effect"] == "Allow":
            for action in policy["Action"]:
                # Check if the target action is allowed by the policy
                if target_action == action or (action.replace("*", "") in target_action):
                    allowed_resources.extend(policy["Resource"])

    # Remove duplicates and return the result
    return set(allowed_resources)


if __name__ == "__main__":
    policies = [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*",
            ],
            "Resource": ["resource1", "resource2", "resource3"],
        }
    ]

    target_action = "s3:GetObject"
    allowed_resources = find_allowed_resources(policies, target_action)
    print("allowed_resources:", allowed_resources)
