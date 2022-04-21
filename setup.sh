#!/usr/bin/env nix-shell
#!nix-shell -p python39
#!nix-shell -i bash


set -e

script_dir=$(dirname $0)
if [ $script_dir = '.' ]
then
script_dir="$(pwd)"
fi
pushd $script_dir > /dev/null

# Create a virtual environment for this project.
virtualenv_name=venv-$(basename $script_dir)

echo "Creating a virtual environment for this project called $virtualenv_name..."
mkdir -p .$virtualenv_name/
python -m venv .$virtualenv_name
echo "Done."

# Activate the virtual environment
echo "Activating the virtual environment..."
source .$virtualenv_name/bin/activate
echo "Done."

echo "Upgrading pip..."
pip install --upgrade pip
echo "Done."

echo "Installing requirements-dev.txt..."
pip install -U -r requirements-dev.txt
echo "Done."

echo "
Setup succeeded!

  - Now run 'source .$virtualenv_name/bin/activate' in the shell to activate the
    virtual environment.

  - Run 'deactivate' to exit the virtual environment."

popd > /dev/null
