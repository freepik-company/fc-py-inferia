# Freepik Company cogito

A longer description of the project.

## Development

### Build the local development environment

```sh
make build
```

## Installation

### Using UV

First, you have to install Freepik Company private artifact registry, they can be `dev` dependencies:
```sh
uv add keyring keyrings.google-artifactregistry-auth --dev
```

Then, you can install the package:
```sh
uv add freepikcompany.cogito --index https://oauth2accesstoken@europe-west1-python.pkg.dev/fc-shared/python/simple/
```

### Using pip

First, you have to install Freepik Company private artifact registry:

```sh
pip install keyring keyrings.google-artifactregistry-auth
```

Add new extra index url to your `requirements.txt` file:
```txt
--extra-index-url https://oauth2accesstoken@europe-west1-python.pkg.dev/fc-shared/python/simple/
```

Then, you can install the package:
```sh
pip install freepikcompany.cogito
```

## Usage

*Put here any information about how to use this amazing library*
