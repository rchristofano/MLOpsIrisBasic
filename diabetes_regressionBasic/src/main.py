from train import train_model, split_data, get_model_metrics
from azureml.core.run import Run
from azureml.core import Dataset, Workspace, Experiment
from azureml.core.model import Model

import joblib

import os


step_output_path = './MLOpsBasic/diabetes_resgressionBasic/models/'
model_name = "diabetes_model.pkl"

# training parameters
train_args = {"alpha": 0.5}
# ----------------------------------


# subscription_id = '21128a5f-9486-40ab-bc5d-d398aadc0100'
# resource_group = 'lab'
# workspace_name = 'main'

# ws = Workspace(subscription_id, resource_group, workspace_name)
ws = Workspace.from_config()

dataset = Dataset.get_by_name(ws, name='diabetes_ds')
# dataset.to_pandas_dataframe()

print("Startingnggggg")

# ----------------------------------
experiment = Experiment(workspace=ws, name="diabetes-diabetes_regression_test")
#run = Run.get_context()
run = experiment.start_logging()
run.log("alpha_value", train_args["alpha"])



# Log the training parameters
## print(f"Parameters: {train_args}")
## for (k, v) in train_args.items():
##    run.log(k, v)
##    run.parent.log(k, v)

# Get the dataset
# dataset = Dataset.get_by_name(run.experiment.workspace, "diabetes_ds", "latest")  

# Link dataset to the step run so it is trackable in the UI
## run.input_datasets['training_data'] = dataset
## run.parent.tag("dataset_id", value=dataset.id)

# Split the data into test/train
df = dataset.to_pandas_dataframe()
data = split_data(df)

# Train the model
model = train_model(data, train_args)

# Evaluate and log the metrics returned from the train function
metrics = get_model_metrics(model, data)
## for (k, v) in metrics.items():
##     run.log(k, v)
##     run.parent.log(k, v)
run.log("mse", metrics["mse"])
# Register model
os.makedirs(step_output_path, exist_ok=True)
model_output_path = os.path.join(step_output_path, model_name)
joblib.dump(value=model, filename=model_output_path)


# register the model for deployment
model = Model.register(model_path = model_output_path, # this points to a local file
                       model_name = "diabetes_model", # name the model is registered as
                       tags = {'area': "diabetes", 'type': "regression"}, 
                       description = "A simple Ridge Regression model", 
                       workspace = ws)

# run.register_model(model_name="diabetes_model",
#                    model_path=model_output_path, # the relative cloud path
#                    tags={'area': 'diabetes', 'type': 'regression'},
#                    description='A simple Ridge Regression model'
#                    )

run.complete()