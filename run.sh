#!/bin/bash
prefect cloud login -k $(your_prefect_cloud_api_key) --workspace $(your_prefect_cloud_workspace)
prefect deployment build -n dockercontainerdeployment -p default-agent-pool -q test main.py:main_flow -sb s3/sandp-s3-block
prefect deployment apply ./main_flow-deployment.yaml
prefect agent start -p 'default-agent-pool'
