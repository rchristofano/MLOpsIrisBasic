import logging
from azureml.core import Workspace, Dataset
from azureml.core.authentication import ServicePrincipalAuthentication
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info("path before")
    
    req_body = req.get_json()

    path_file = req_body.get('path')

    logging.info(path_file)

    if not path_file:
        try:
            req_body = req.get_json()
            logging.info("req_body")
            logging.info(req_body)
        except ValueError:
            pass
        else:
            path_file = req_body.get('path')
            logging.info("path_file")
            logging.info(path_file)

    logging.info("path after") 
    logging.info(path_file)
    if path_file:
        #azure CLI Authentication
        # we can adopt password using system environment variable
        # svc_pr_password = os.environ.get("AZUREML_PASSWORD")
        logging.info("first if")
        svc_pr = ServicePrincipalAuthentication(
            tenant_id="5b25ec18-40df-4980-9b74-ee18f1141106",
            service_principal_id="47821d63-15cd-474e-bec6-77a23ae1c3f0",
            service_principal_password="dUcDVt4D7_KF60SdMaGdXnmi_J.15_TH_."
        )
        logging.info("Service Principal ok")
        # get existing workspace
        ws = Workspace.get(
            name="main",
            subscription_id="21128a5f-9486-40ab-bc5d-d398aadc0100",
            resource_group="lab",
            auth=svc_pr
        )
        logging.info("ws connected")
        # datastore_name = 'workspaceblobstore'
        
        # retrieve an existing datastore in the workspace by name
        # datastore = Datastore.get(ws, datastore_name)
        # path_on_datastore = 'https://mainstorage96ac1322da8d4.blob.core.windows.net/azureml-blobstore-56ac70ab-b973-483c-a123-3042c79cec8a/UI/diabetes.csv'
        # dataset = Dataset.Tabular.from_delimited_files(path=(datastore, path_on_datastore))        
        # print("path=",path)
        # path ='https://mainstorage96ac1322da8d4.blob.core.windows.net/azureml-blobstore-56ac70ab-b973-483c-a123-3042c79cec8a/UI/diabetes5.csv'
        dataset = Dataset.Tabular.from_delimited_files(path=path_file)
        logging.info("DataSet Delimited")
        dataset = dataset.register(
            workspace=ws,
            name="diabetes_ds",
            description="diabetes training data",
            tags={"format": "CSV"},
            create_new_version=True,
        )
        logging.info("DataSet Registered")

        return func.HttpResponse("Successfull", status_code=200)

    else:
        logging.info("second if")
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a path in the query string or in the request body for a personalized response.",
             status_code=200
        )