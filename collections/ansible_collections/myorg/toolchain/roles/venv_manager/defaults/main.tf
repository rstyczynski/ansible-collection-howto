---
# Path where the virtual environment will be created
venv_manager_path: "~/.ansible/venv"

# Python executable to use for creating the venv (must exist on the host)
# Example values: python3, /usr/bin/python3, python3.12
venv_manager_python: "python3"

# Whether to upgrade bootstrap tooling in the venv (pip/setuptools/wheel)
venv_manager_upgrade_bootstrap: true

# Which bootstrap packages to manage when venv_manager_upgrade_bootstrap is true
venv_manager_bootstrap_packages:
  - pip
  - setuptools
  - wheel

# Optional: path to a requirements file (relative to playbook or absolute).
# Set to null/empty (~) to skip.
venv_manager_requirements_file: ~

# Optional: explicit list of packages (PEP 508 specifiers).
# Leave empty to skip.
venv_manager_packages: []
