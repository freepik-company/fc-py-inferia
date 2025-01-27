## 0.1.2b0 (2025-01-27)

### Feat

- **cli**: adds run cli command (#35)

## 0.1.2a0 (2025-01-27)

## 0.1.1 (2025-01-27)

### Fix

- input model name for http request (#36)

## 0.1.0 (2025-01-27)

### Feat

- build and publish cogito as a pip module in test pypi and pypi (#31)
- Implements type inspection of predict methods (#20)

### Fix

- Changes JSONResponse importation (#26)

### Refactor

- add codestyle pre commit (#32)
- models setup on lifespan (#25)

## 0.0.1 (2025-01-24)

### Feat

- generate predictor classes in client implementations using scaffolds (#27)
- handle setup and predict method raised exceptions (#22)
- update init command for both default/prompted values and forced initialization (#21)
- Adds inspection of predict return type  (#18)
- handling predictor initialization (#13)
- **config.py**: Handles NotFileFound if inferia.yaml not found (#15)
- add default healtcheck endpoint (#4)
- add config file management (#5)
- add app class to initialize (#3)
- initial commit

### Fix

- **inferia/core/app.py**:  re-import correct module for get_predictor_handler_return_type (#19)
- **config.py**: Fixes bug in load_from_file exception handling (#16)

### Refactor

- **setup.py, .gitignore**: Update package dependencies and ignore build artifacts
- define common inference server and training config (#17)
- **setup.py**: update project description and remove old one
- Remove unused files and modules for cleaner structure
