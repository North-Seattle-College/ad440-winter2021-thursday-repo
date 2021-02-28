bucket_name=$1
aws_access_key=$2
aws_access_secret=$3
local_path=$4

# https://keithweaver.ca/lessons/uploading-files-to-aws-s3-with-github-actions?s=yktc

# S3 Upload shell script for users/id/tasks/id

# # Create a zip of the current directory.
# zip -r $local_path . -x .git/ .git/*** .github/workflows/artillery-report-users-user_id-tasks-task_id.yaml scripts/artillery-shell-users-user_id-tasks-task_id.sh scripts/artillery-python-users-user_id-tasks-task_id.py .DS_Store

# Install required dependencies for Python script.
pip3 install boto3

# Run upload script
python3 scripts/artillery-python-users-id-tasks-id.py $bucket_name $aws_access_key $aws_access_secret $local_path
