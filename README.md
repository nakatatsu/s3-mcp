# FastMCP S3 Server

A FastMCP server implementation that provides a secure interface for interacting with AWS S3. This server allows clients to perform various S3 operations through a structured API.

## Overview

This server enables you to:

- Manage S3 buckets and objects
- Handle lifecycle configurations
- Set and retrieve object tags
- Manage bucket policies
- Configure CORS settings

## Installation

There are multiple ways to use this server depending on your setup.

### Cursor (recommended)

Add this to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "s3-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "AWS_SECRET_ACCESS_KEY=your_access_key",
        "-e",
        "AWS_ACCESS_KEY_ID=hvs.your_access_key-vault-token",
        "-e",
        "AWS_REGION=your_region",
        "ashgw/vault-mcp:latest"
      ]
    }
  }
}
```

> If you prefer pinning to a specific docker image build (e.g. 20250413-165732), use that tag instead of latest. Browse available versions on [Docker Hub](https://hub.docker.com/r/ashgw/s3-mcp/tags).

Once added, you can use prompts like:

> "Read the secret at path `apps/myapp/config` from Vault"

Cursor will route that request through the MCP server automatically.

---

### Docker (manual)

You can run Vault MCP manually via Docker:

```bash
docker run --rm -it \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_REGION=your_region \
  ashgw/s3-mcp
```

This uses the pre-built image published at [ashgw/s3-mcp](https://hub.docker.com/repository/docker/ashgw/s3-mcp).

---

### Repo

Clone the repository and `cd` into it, then build with

```
docker build -t vault-mcp .
```

Then run with

```
docker run --rm -e VAULT_ADDR=localhost:8200 -e VAULT_TOKEN=hsv.yourtoken vault-mcp
```

### Environment Variables

Set the following environment variables for AWS credentials:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=your_region
```

## Features

- **List Buckets**: Retrieve a list of all S3 buckets.
- **Create Bucket**: Create a new S3 bucket with optional configurations.
- **List Objects**: List all objects in a specified bucket.
- **Get Object**: Retrieve the content of a specified object.
- **Put Object**: Upload an object to a specified bucket.
- **Delete Object**: Remove an object from a specified bucket.
- **Generate Presigned URL**: Create a presigned URL for accessing or uploading an object.
- **Set Bucket Policy**: Update or set a policy for a specified bucket.
- **Get Bucket Policy**: Retrieve the current policy for a specified bucket.
- **Delete Bucket Policy**: Remove the current policy for a specified bucket.
- **Lifecycle Configuration**: Manage lifecycle rules for S3 buckets.
- **Object Tagging**: Set and retrieve tags for S3 objects.
- **CORS Configuration**: Get and set CORS rules for a bucket.

## Usage Examples

### List Buckets

```python
response = await tool("list_buckets")
print(response)
```

### Create a Bucket

```python
response = await tool("create_bucket", {
    "bucket_name": "my-new-bucket",
    "region": "us-west-1",
    "config": {
        "blockPublicAccess": {
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        },
        "versioning": True,
        "encryption": "AES256"
    }
})
print(response)
```

### Upload a File

```python
response = await tool("upload_local_file", {
    "bucket_name": "my-new-bucket",
    "local_path": "/path/to/local/file.txt",
    "key": "file.txt"
})
print(response)
```

### Get Object Tags

```python
response = await tool("get_object_tagging", {
    "bucket_name": "my-new-bucket",
    "key": "file.txt"
})
print(response)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments

- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for AWS SDK for Python.
- [FastMCP](https://github.com/yourusername/fastmcp) for the Model Context Protocol framework.
