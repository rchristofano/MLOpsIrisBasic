from train import train_model, split_data, get_model_metrics
from azureml.core.run import Run
from azureml.core import Dataset

import joblib

import os


step_output_path = './MLOpsBasic/diabetes_resgressionBasic/models/'
model_name = "diabetes_model.pkl"

# training parameters
train_args = {"alpha": 0.5}

run = Run.get_context()

# Log the training parameters
print(f"Parameters: {train_args}")
for (k, v) in train_args.items():
    run.log(k, v)
    run.parent.log(k, v)

# Get the dataset
dataset = Dataset.get_by_name(run.experiment.workspace, "diabetes_ds", "latest")  

# Link dataset to the step run so it is trackable in the UI
run.input_datasets['training_data'] = dataset
run.parent.tag("dataset_id", value=dataset.id)

# Split the data into test/train
df = dataset.to_pandas_dataframe()
data = split_data(df)

# Train the model
model = train_model(data, train_args)

# Evaluate and log the metrics returned from the train function
metrics = get_model_metrics(model, data)
for (k, v) in metrics.items():
    run.log(k, v)
    run.parent.log(k, v)

# Pass model file to next step
os.makedirs(step_output_path, exist_ok=True)
model_output_path = os.path.join(step_output_path, model_name)
joblib.dump(value=model, filename=model_output_path)

# Also upload model file to run outputs for history
os.makedirs('outputs', exist_ok=True)
output_path = os.path.join('outputs', model_name)
joblib.dump(value=model, filename=output_path)

run.tag("run_type", value="train")
print(f"tags now present for run: {run.tags}")

run.upload_file(name=model_name, path_or_stream=model_output_path)

run.complete()