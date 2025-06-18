# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple S3 log storage service using MCP (Model Context Protocol). The primary use case is to append logs to S3 objects, creating a centralized log storage system accessible via AI assistants.

## Commands

```bash
# Build and run with Docker
docker build -t s3-mcp .
docker run -e AWS_ACCESS_KEY_ID=your_key AWS_SECRET_ACCESS_KEY=your_secret nakatatsu/claude-log-mcp:latest -e AWS_S3_BUCKET=your_bucket -e AWS_S3_PREFIX=your_prefix -e
```





This S3 path specifies a hierarchical directory structure organized by service, environment, and timestamp.
- <bucket-name>: The name of the S3 bucket.
- service=<service-name>: The name of the service.
- env=<environment-name>: The environment name (e.g., dev, staging, production).
- year=<YYYY>: The 4-digit year.
- month=<MM>: The 2-digit month.
- day=<DD>: The 2-digit day.
- hour=<HH>: The 2-digit hour in 24-hour format.


## Architecture

The service is built to handle log appending operations to S3:

- **main.py**: MCP server implementation that provides S3 operations. For logging purposes, the most relevant tools are:
  - `put_object`: Write new log files

- **scripts/commands.py**: Development tooling (formatting, linting)

## Key Implementation for Logging

When implementing log storage:
1. Use a consistent naming convention for log files (e.g., `logs/YYYY-MM-DD/service-name.log`)
2. For appending, first read the existing object with `get_object`, then write back with `put_object`
3. Consider using S3 lifecycle policies via `put_bucket_lifecycle` to automatically archive or delete old logs
4. Use object tagging (`put_object_tagging`) to categorize logs by service, severity, or environment

## Common Log Storage Patterns

```python
# Example: Append to daily log file
date_key = f"logs/{datetime.now().strftime('%Y-%m-%d')}/app.log"
existing_content = await get_object(context, bucket_name, date_key)
new_content = existing_content + "\n" + new_log_entry
await put_object(context, bucket_name, date_key, new_content)
```

Note: S3 doesn't support true append operations, so each append requires reading and rewriting the entire object. For high-frequency logging, consider batching writes or using services designed for streaming logs.