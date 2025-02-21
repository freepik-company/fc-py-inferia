import os
from huggingface_hub import snapshot_download
from google.cloud import storage


def download_huggingface_model(model_id: str, cache_dir: str) -> str:
    """
    Download a model from Hugging Face and return the model id.
    """
    return snapshot_download(repo_id=model_id, cache_dir=cache_dir)


def download_gcp_model(model_path: str, cache_dir: str) -> str:
    """
    Download a model from Google Cloud Storage and return the local file path.
    """
    client = storage.Client()
    path_parts = model_path.replace("gs://", "").split("/", 1)
    bucket_name, blob_path = path_parts[0], path_parts[1]
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    model_file = os.path.join(cache_dir, os.path.basename(blob_path))

    if os.path.exists(model_file):
        return model_file

    blob.download_to_filename(model_file)
    return model_file
