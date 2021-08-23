from azureml.core import Workspace, Datastore, Dataset
from azureml.core.authentication import ServicePrincipalAuthentication

datastore_name = 'workspaceblobstore'

svc_pr = ServicePrincipalAuthentication(
    tenant_id="5b25ec18-40df-4980-9b74-ee18f1141106",
    service_principal_id="47821d63-15cd-474e-bec6-77a23ae1c3f0",
    service_principal_password="dUcDVt4D7_KF60SdMaGdXnmi_J.15_TH_."
)

# get existing workspace
ws = Workspace.get(
    name="main",
    subscription_id="21128a5f-9486-40ab-bc5d-d398aadc0100",
    resource_group="lab",
    auth=svc_pr
)
    
# retrieve an existing datastore in the workspace by name
datastore = Datastore.get(ws, datastore_name)
# path_on_datastore = 'https://mainstorage96ac1322da8d4.blob.core.windows.net/azureml-blobstore-56ac70ab-b973-483c-a123-3042c79cec8a/UI/diabetes.csv'
# dataset = Dataset.Tabular.from_delimited_files(path=(datastore, path_on_datastore))

path ='https://mainstorage96ac1322da8d4.blob.core.windows.net/azureml-blobstore-56ac70ab-b973-483c-a123-3042c79cec8a/UI/diabetes2.csv'
dataset = Dataset.Tabular.from_delimited_files(path=path)

dataset = dataset.register(
    workspace=ws,
    name="diabetes_ds",
    description="diabetes training data",
    tags={"format": "CSV"},
    create_new_version=True,
)


