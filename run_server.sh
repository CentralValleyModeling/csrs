# assume that the container already has activated the right environment
# asumme current working directory is at the top level of this repo
# Build should pass the GITHUB_TOKEN as a --build_arg
git_repo_url="https://$GITHUB_TOKEN@github.com/CentralValleyModeling/csrs"
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Warning: GITHUB_TOKEN environment variable is not set, assuming public repo"
    git_repo_url="https://github.com/CentralValleyModeling/csrs"
fi

echo "git_repo = ${git_repo_url}"
git clone "${git_repo_url}" "code"

# Run app
uvicorn code.src.csrs.main:app --host 0.0.0.0 --port 80