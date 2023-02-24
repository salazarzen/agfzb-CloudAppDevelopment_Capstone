"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}

# import sys
# from ibmcloudant.cloudant_v1 import CloudantV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("NY832ImwcVT3MtWN7Nf8Tddl4JHF32ZJrxb1oCigK5P7")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://47758dc9-211d-4a78-a038-617ad9e1338a-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find(
        db='reviews',
        selector={'dealership': {'$eq': int(dict["id"])}},
        ).get_result()
        
    try:
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        if(len(result['body']['data']['docs'])==0):
            return {
                'statusCode': 404,
                'message': 'Dealer ID does not exist'
            }
        else:
            return result
    except:
        return {
        'statusCode': 500,
        'message': 'Something went wrong'
        }

# import sys
# from ibmcloudant.cloudant_v1 import CloudantV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("NY832ImwcVT3MtWN7Nf8Tddl4JHF32ZJrxb1oCigK5P7")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://47758dc9-211d-4a78-a038-617ad9e1338a-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
    
    try:
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 500,
        'message': 'Something went wrong'
        }
