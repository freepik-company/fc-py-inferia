import logging
import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))


# Set up logging with a stream handler
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

from cogito import Application

if __name__ == "__main__":
    app = Application(config_file_path=HERE)
    app.run()
