import os
from typing import Any
import boto3
from fastmcp import FastMCP, Context


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-west-1')
)

app = FastMCP("s3")

@app.tool(name="list_buckets", description="List all buckets")
async def list_buckets(context: Context) -> Any:
    try:
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return {"buckets": buckets}
    except Exception as e:
        return {"error": str(e)}

@app.tool(name="create_bucket", description="Create a new S3 bucket with optional security config")
async def create_bucket(context: Context, bucket_name: str, region: str = "us-west-1", config: dict = None):
    try:
        args = {
            "Bucket": bucket_name,
            "CreateBucketConfiguration": {"LocationConstraint": region}
        }

        # basic creation
        s3_client.create_bucket(**args)

        # optionally apply extra config
        if config:
            if config.get("blockPublicAccess"):
                s3_client.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration=config["blockPublicAccess"]
                )
            if config.get("versioning"):
                s3_client.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={"Status": "Enabled" if config["versioning"] else "Suspended"}
                )
            if config.get("encryption"):
                s3_client.put_bucket_encryption(
                    Bucket=bucket_name,
                    ServerSideEncryptionConfiguration={
                        "Rules": [{
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": config["encryption"]
                            }
                        }]
                    }
                )
        return {"success": True, "bucket": bucket_name}
    except Exception as e:
        return {"error": str(e)}

# Existing tools below...

@app.tool(name="list_bucket", description="List objects in a bucket")
async def list_bucket(context: Context, bucket_name: str, key_prefix: str = ""):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=key_prefix)
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat()
                })
        return {'bucket': bucket_name, 'files': files}
    except Exception as e:
        return {"error": str(e)}

@app.tool(name="get_object", description="Get an object from a bucket")
async def get_object(context: Context, bucket_name: str, key: str):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        return response['Body'].read()
    except Exception as e:
        return {"error": str(e)}

@app.tool(name="put_object", description="Put an object into a bucket")
async def put_object(context: Context, bucket_name: str, key: str, body: str):
    try:
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

@app.tool(name="upload_local_file", description="Upload a local file to a bucket")
async def upload_local_file(context: Context, bucket_name: str, local_path: str, key: str):
    try:
        s3_client.upload_file(local_path, bucket_name, key)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

@app.tool(name="download_file_to_local", description="Download a file from a bucket to a local path")
async def download_file_to_local(context: Context, bucket_name: str, key: str, local_path: str):
    try:
        s3_client.download_file(bucket_name, key, local_path)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

@app.tool(name="delete_object", description="Delete an object from a bucket")
async def delete_object(context: Context, bucket_name: str, key: str):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(transport='stdio')
