import os
from pathlib import Path
from typing import Optional, Union, Dict
from huggingface_hub import snapshot_download
from google.cloud import storage
import logging
from urllib.parse import urlparse


class ModelDownloader:
    """A class to download AI models from Hugging Face or Google Cloud Storage."""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the ModelDownloader.

        Args:
            cache_dir: Optional directory to store models. If None, uses INFERIA_MODELS_PATH
                      environment variable or defaults to ~/.inferia/models
        """
        self.cache_dir = cache_dir or os.getenv(
            "INFERIA_MODELS_PATH", str(Path.home() / ".inferia" / "models")
        )
        os.makedirs(self.cache_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def download(
        self, model_url: str, credentials: Optional[Union[str, Dict]] = None, **kwargs
    ) -> str:
        """
        Download a model from the given URL.
        Automatically determines the source (Hugging Face or GCS) from the URL.

        Args:
            model_url: URL or identifier for the model
                Examples:
                - "hf://bert-base-uncased"
                - "huggingface://bert-base-uncased"
                - "gs://bucket-name/path/to/model"
                - "gcs://bucket-name/path/to/model"
            credentials: Optional credentials for private repositories (GCS only)
            **kwargs: Additional arguments to pass to the specific downloader

        Returns:
            str: Path to the downloaded model

        Raises:
            ValueError: If the URL scheme is not supported
        """
        parsed_url = urlparse(model_url)
        scheme = parsed_url.scheme.lower()

        if scheme in ["hf", "huggingface"] or not scheme:
            model_id = parsed_url.path if parsed_url.path else model_url
            if model_id.startswith("/"):
                model_id = model_id[1:]
            return self.download_from_hf(model_id, **kwargs)

        elif scheme in ["gs", "gcs"]:
            bucket_name = parsed_url.netloc
            model_path = parsed_url.path
            if model_path.startswith("/"):
                model_path = model_path[1:]
            return self.download_from_gcs(
                bucket_name, model_path, credentials=credentials
            )

        else:
            raise ValueError(
                f"Unsupported model source: {scheme}. "
                "Supported schemes are: hf://, huggingface://, gs://, gcs://"
            )

    def download_from_hf(self, model_id: str, **kwargs) -> str:
        """
        Download a model from Hugging Face Hub.

        Args:
            model_id: The Hugging Face model ID (e.g., 'bert-base-uncased')
            **kwargs: Additional arguments to pass to snapshot_download

        Returns:
            str: Path to the downloaded model
        """
        self.logger.info(f"Downloading model {model_id} from Hugging Face")
        try:
            local_path = snapshot_download(
                repo_id=model_id, cache_dir=self.cache_dir, **kwargs
            )
            return local_path
        except Exception as e:
            self.logger.error(f"Error downloading from Hugging Face: {str(e)}")
            raise

    def download_from_gcs(
        self,
        bucket_name: str,
        model_path: str,
        credentials: Optional[Union[str, Dict]] = None,
    ) -> str:
        """
        Download a model from Google Cloud Storage, supporting private repositories.

        Args:
            bucket_name: Name of the GCS bucket
            model_path: Path to the model within the bucket
            credentials: Optional credentials for private buckets. Can be:
                - Path to service account JSON file
                - Dictionary containing service account info
                - None (will use environment variables GOOGLE_APPLICATION_CREDENTIALS)

        Returns:
            str: Path to the downloaded model
        """
        self.logger.info(f"Downloading model from GCS: {bucket_name}/{model_path}")
        try:
            if credentials:
                if isinstance(credentials, str):
                    client = storage.Client.from_service_account_json(credentials)
                elif isinstance(credentials, dict):
                    client = storage.Client.from_service_account_info(credentials)
            else:
                client = storage.Client()

            bucket = client.bucket(bucket_name)

            model_name = Path(model_path).name
            local_path = Path(self.cache_dir) / model_name

            blob = bucket.blob(model_path)
            blob.download_to_filename(str(local_path))

            return str(local_path)
        except Exception as e:
            self.logger.error(f"Error downloading from GCS: {str(e)}")
            raise

    def get_model_path(self, model_name: str) -> str:
        """
        Get the local path for a model.

        Args:
            model_name: Name of the model

        Returns:
            str: Full path to the model in the cache directory
        """
        return str(Path(self.cache_dir) / model_name)
