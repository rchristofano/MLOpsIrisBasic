from azureml.core.run import Run
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline, PipelineData, PublishedPipeline
from azureml.core import Workspace, Dataset, Datastore, Experiment
from azureml.core.runconfig import RunConfiguration
# from ml_service.pipelines.load_sample_data import create_sample_data_csv
# from util.attach_compute import get_compute
from util.env_variables import Env
from util.manage_environment import get_environment
import os

def main():
    e = Env()
    # Get Azure machine learning workspace
    ws = Workspace.get(
        name=e.workspace_name,
        subscription_id=e.subscription_id,
        resource_group=e.resource_group,
    )

    # ws = Run.get_context().experiment.workspace
    # dataset = Dataset.get_by_name(ws, "diabetes_ds", "latest")  

    # datastore_name = ws.get_default_datastore().name

    # print(datastore_name)
    pipeline_data = PipelineData(
        "pipeline_data", datastore=ws.get_default_datastore()
    )

    model_name_param = PipelineParameter(name="model_name", default_value=e.model_name)  # NOQA: E501
    dataset_version_param = PipelineParameter(
        name="dataset_version", default_value=e.dataset_version
    )
    data_file_path_param = PipelineParameter(
        name="data_file_path", default_value="none"
    )
    caller_run_id_param = PipelineParameter(name="caller_run_id", default_value="none")  # NOQA: E501

    environment = get_environment(
        ws,
        e.aml_env_name,
        conda_dependencies_file=e.aml_env_train_conda_dep_file,
        create_new=e.rebuild_env,
    )  #

    run_config = RunConfiguration()
    run_config.environment = environment
    # Get dataset name
    dataset_name = e.dataset_name
    train_step = PythonScriptStep(
        name="Train Model",
        script_name=e.train_script_path,        
        compute_target="cpu-cluster",
        source_directory=e.sources_directory_train,
        outputs=[pipeline_data],
        arguments=[
            "--model_name",
            model_name_param,
            "--step_output",
            pipeline_data,
            "--dataset_version",
            dataset_version_param,
            "--data_file_path",
            data_file_path_param,
            "--caller_run_id",
            caller_run_id_param,
            "--dataset_name",
            dataset_name,
        ],
        
        runconfig=run_config,
        allow_reuse=True,
    )

    # ws.get_run
    print("Step Train created")

    register_step = PythonScriptStep(
        name="Register Model ",
        script_name=e.register_script_path,
        compute_target="cpu-cluster",
        source_directory=e.sources_directory_train,
        inputs=[pipeline_data],
        arguments=["--model_name", model_name_param, "--step_input", pipeline_data, ],  # NOQA: E501
        runconfig=run_config,
        allow_reuse=False,
    )
    print("Step Register created")

    register_step.run_after(train_step)
    steps = [train_step, register_step]

    train_pipeline = Pipeline(workspace=ws, steps=steps)
    train_pipeline._set_experiment_name
    train_pipeline.validate()
    published_pipeline = train_pipeline.publish(
        name=e.pipeline_name,
        description="Model training/retraining pipeline",
        version=e.build_id,
    )
    print(f"Published pipeline: {published_pipeline.name}")
    print(f"for build {published_pipeline.version}")

    # Find the pipeline that was published by the specified build ID
    # pipelines = PublishedPipeline.list(ws)

    pipeline_parameters = {"model_name": e.model_name}
    tags = {"BuildId": e.build_id}

    experiment = Experiment(
            workspace=ws,
            name=e.experiment_name)
    run = experiment.submit(
        published_pipeline,
        tags=tags,
        pipeline_parameters=pipeline_parameters)
    
    
    print("Pipeline run initiated ", run.id)

if __name__ == "__main__":
    main()