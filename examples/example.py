import sys
import os

"""
This is a pythonic way to import the Application class from the cogito package from examples folder without being
a package itself. This is a common pattern in the Python world. 
"""
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

from cogito import Application

app = Application(
        port=8080
)

if __name__ == "__main__":
    app.run()