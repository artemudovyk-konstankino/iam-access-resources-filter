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


def find_allowed_resources_subset(resources: list[str], allowed_resources: set[str]) -> set[str]:
    allowed_resources_subset = []
    wildcard_allowed_resources = [allowed_resource for allowed_resource in allowed_resources if "*" in allowed_resource]

    for resource in resources:
        if resource in allowed_resources:
            allowed_resources_subset.append(resource)
        
        # Check if the resource matches the wildcard allowed resource
        for wildcard_allowed_resource in wildcard_allowed_resources:
            if resource.startswith(wildcard_allowed_resource.replace("*", "")):
                allowed_resources_subset.append(resource)
            
    return set(allowed_resources_subset)


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
            "Resource": ["resource_wildcard*", "resource2", "resource3"],
        }
    ]

    target_action = "s3:GetObject"
    allowed_resources = find_allowed_resources(policies, target_action)
    print("allowed_resources:", allowed_resources)
    
    resources = ["resource_wildcard1", "resource_wildcard2", "resource2", "resource3", "resource4", "definitely_not_allowed"]
    
    allowed_resources_subset = find_allowed_resources_subset(resources, allowed_resources)
    print("all resources:", resources)
    print("allowed_resources_subset:", allowed_resources_subset)
