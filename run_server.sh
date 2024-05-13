#!/bin/bash

# Activate environment
source /env/bin/activate

# Check if the GITHUB_TOKEN environment variable is set 
# (should be passed to docker build as a build-arg)
if [ -z "$GITHUB_TOKEN" ]; then
    echo "assuming repo is public, no token set"
    git_repo_url="https://github.com/$1.git"
else
    echo "github token set"
    git_repo_url="https://$GITHUB_TOKEN@github.com/$1.git"
fi

# Clone the repo into a subfolder
echo "cloning repo $1"
git clone "$git_repo_url" "code"

# Copy over any bootstrap databases
cp -R database/. code/database/

# Change directory to the cloned repository
cd "code" || exit

# Run app
echo "Running the application..."

uvicorn src.csrs.main:app --host 0.0.0.0 --port 80