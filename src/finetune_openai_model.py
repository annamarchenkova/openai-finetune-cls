## Fine tune Azure open ai model
# - The official example here: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?pivots=programming-language-python
# - The example with easier data preparation: https://github.com/openai/openai-cookbook/blob/main/examples/Fine-tuned_classification.ipynb

import openai
from openai import cli
import time

# parameters used during preprocessing to eliminate unfrequent groups from the dataset
# and too short strings.
thresh_unfr = 100
thresh_very_unfr = 60
min_text_len = 20

def check_status(training_id, validation_id):
    train_status = openai.File.retrieve(training_id)["status"]
    valid_status = openai.File.retrieve(validation_id)["status"]
    print(f'Status (training_file | validation_file): {train_status} | {valid_status}')
    return (train_status, valid_status)


deployment_name = 'gpt-note-crm'
deployment_name_embeddigns = 'embeddings-ada-002'
openai.api_type = 'azure'
openai.api_key = open(os.path.join(PROJECT_DIR, "keys", "azure_openai_key.txt"), "r").read().strip("\n")
openai.api_base = 'https://notecrm.openai.azure.com/' # endpoint
openai.api_version = '2023-05-15'

os.environ['OPENAI_API_KEY'] = openai.api_key
os.environ['OPENAI_API_VERSION'] = openai.api_version
os.environ['OPENAI_API_BASE'] = openai.api_base

def main():
  #### Training agents
  training_file_name = f'ag{thresh_unfr}_{thresh_very_unfr}_{min_text_len}_prepared_train.jsonl'
  validation_file_name = f'ag{thresh_unfr}_{thresh_very_unfr}_{min_text_len}_prepared_valid.jsonl'
  
  # Upload the training and validation dataset files to Azure OpenAI.
  training_id = cli.FineTune._get_or_upload(training_file_name, True)
  validation_id = cli.FineTune._get_or_upload(validation_file_name, True)
  
  # Check on the upload status of the training and validation dataset files.
  (train_status, valid_status) = check_status(training_id, validation_id)
  classification_n_classes = df.completion.nunique()
  
  # This example defines a fine-tune job that creates a customized model based on curie, 
  # with just a single pass through the training data. The job also provides classification-
  # specific metrics, using our validation data, at the end of that epoch.
  args = {
      "n_epochs": 1,
      "training_file": training_id,
      "validation_file": validation_id,
      "model": "curie",
      "compute_classification_metrics": True,
      "classification_n_classes": classification_n_classes,
      # "batch_size": 1100,
  }
  # Create the fine-tune job and retrieve the job ID
  # and status from the response.
  resp = openai.FineTune.create(**args)
  
  job_id = resp["id"]
  status = resp["status"]
  
  # You can use the job ID to monitor the status of the fine-tune job.
  # The fine-tune job may take some time to start and complete.
  print(f'Fine-tuning model with job ID: {job_id}.')
  
  # # Get job_ids list
  # result = openai.FineTune.list()
  # job_ids = [i['id'] for i in result["data"]]
  # job_ids
  
  # Get the status of our fine-tune job.
  status = openai.FineTune.retrieve(id=job_id)["status"]
  
  # If the job isn't yet done, poll it every 2 seconds.
  if status not in ["succeeded", "failed"]:
      print(f'Job not in terminal status: {status}. Waiting.')
      while status not in ["succeeded", "failed"]:
          time.sleep(2)
          status = openai.FineTune.retrieve(id=job_id)["status"]
          print(f'Status: {status}')
  else:
      print(f'Fine-tune job {job_id} finished with status: {status}')
  
  # Check if there are other fine-tune jobs in the subscription. 
  # Your fine-tune job may be queued, so this is helpful information to have
  # if your fine-tune job hasn't yet started.
  print('Checking other fine-tune jobs in the subscription.')
  result = openai.FineTune.list()
  job_ids = [i['id'] for i in result["data"]]
  print(f'Found {len(job_ids)} fine-tune jobs: {job_ids}.')
  return job_id

if __name__ == 'main':
  job_id = main()






