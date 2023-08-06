import os
from locative_ml_helpers.platform_helpers.gcp import storage

if __name__ == '__main__':

    print("Starting clean up")
    os.chdir('/home/')
    print("uploading model dir to storage")
    storage.package_and_upload_model_dir(local_path='/opt/ml/model', storage_dir_path=os.environ['SM_MODEL_DIR'], scheme='gs')

    print("uploading output data dir to storage")
    storage.package_and_upload_output_data_dir(local_path='/opt/ml/output', storage_dir_path=os.environ['SM_OUTPUT_DATA_DIR'], scheme='gs')
    print("Done")

