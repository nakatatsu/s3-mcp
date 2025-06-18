import boto3
import gzip
import json
from datetime import datetime, timezone
from typing import Dict, Union
from fastmcp import FastMCP, Context
from env import env

s3_client = boto3.client(
    "s3",
    aws_access_key_id=env.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
    region_name=env.AWS_REGION,
)

app: FastMCP = FastMCP("claude-log-mcp")


@app.tool(name="put", description="Write log entry to S3")
async def put_log(
    context: Context, title: str, content: str
) -> Dict[str, Union[bool, str]]:
    """
    Write a log entry to S3 with automatic timestamp-based path generation.

    Args:
        title (str): Title for the log entry (used in filename)
        content (str): Content to be logged

    Returns:
        A dictionary indicating success with the S3 key or error.

    Example:
        {
            "success": True,
            "key": "logs/year=2024/month=01/day=15/hour=14/20240115T143022Z_error_report.jsonl.gz"
        }
    """
    try:
        # Generate timestamp
        now = datetime.now(timezone.utc)
        
        # Build S3 path: prefix/year=YYYY/month=MM/day=DD/hour=HH/
        path_parts = [
            env.AWS_S3_PREFIX,
            f"year={now.strftime('%Y')}",
            f"month={now.strftime('%m')}",
            f"day={now.strftime('%d')}",
            f"hour={now.strftime('%H')}"
        ]
        s3_path = "/".join(filter(None, path_parts))  # filter removes empty strings
        
        # Build filename: YYYYMMDDThhmmssZ_<title>.jsonl.gz
        safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in title)
        filename = f"{now.strftime('%Y%m%dT%H%M%SZ')}_{safe_title}.jsonl.gz"
        
        # Full S3 key
        s3_key = f"{s3_path}/{filename}"
        
        # Create log entry
        log_entry = {
            "timestamp": now.isoformat(),
            "title": title,
            "content": content
        }
        
        # Compress the content
        json_line = json.dumps(log_entry) + "\n"
        compressed_content = gzip.compress(json_line.encode("utf-8"))
        
        # Upload to S3
        s3_client.put_object(
            Bucket=env.AWS_S3_BUCKET,
            Key=s3_key,
            Body=compressed_content,
            ContentType="application/x-gzip",
            ContentEncoding="gzip"
        )
        
        return {"success": True, "key": s3_key}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    app.run(transport="stdio")