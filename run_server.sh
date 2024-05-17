#!/bin/bash

# Activate environment
source /env/bin/activate

git_repo_url="https://github.com/$1.git"

# Clone the repo into a subfolder
echo "cloning repo $1"
git clone -b production "$git_repo_url" "code"

# Copy over any bootstrap databases
cp -R database/. code/database/

# Change directory to the cloned repository
cd "code" || exit

# Run app
echo "Running the application..."

uvicorn src.csrs.main:app --host 0.0.0.0 --port 80