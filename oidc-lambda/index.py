import boto3
import json
import urllib3
import cfnresponse

def handler(event, context):
    print("Received event:", event)

    cluster_name = event["ResourceProperties"].get("ClusterName")
    region = event["ResourceProperties"].get("Region")

    if not cluster_name or not region:
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Message": "Missing cluster name or region"})
        return

    eks = boto3.client("eks", region_name=region)

    try:
        response = eks.describe_cluster(name=cluster_name)
        oidc_issuer = response["cluster"]["identity"]["oidc"]["issuer"]
        oidc_provider_id = oidc_issuer.split("/")[-1]

        responseData = {
            "OIDCURL": oidc_issuer,
            "OIDCProviderId": oidc_provider_id
        }

        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)

    except Exception as e:
        print("Error:", str(e))
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Message": str(e)})
