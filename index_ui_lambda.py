import boto3

def lambda_handler(event, context):
    cluster_name = event.get("cluster_name")
    region = event.get("region")

    if not cluster_name or not region:
        return {
            "status": "error",
            "message": "Missing cluster_name or region in event"
        }

    eks = boto3.client("eks", region_name=region)
    try:
        response = eks.describe_cluster(name=cluster_name)
        oidc_issuer = response["cluster"]["identity"]["oidc"]["issuer"]
        oidc_provider_id = oidc_issuer.split("/")[-1]

        return {
            "OIDCURL": oidc_issuer,
            "OIDCProviderId": oidc_provider_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
