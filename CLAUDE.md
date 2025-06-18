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

The S3 path naming rule is as follows:

```
s3://<bucket-name>/<prefix>/year=<YYYY>/month=<MM>/day=<DD>/hour=<HH>/
```

This S3 path specifies a hierarchical directory structure organized by service, environment, and timestamp.
- <bucket-name>: The name of the S3 bucket.
- service=<service-name>: The name of the service.
- env=<environment-name>: The environment name (e.g., dev, staging, production).
- year=<YYYY>: The 4-digit year.
- month=<MM>: The 2-digit month.
- day=<DD>: The 2-digit day.
- hour=<HH>: The 2-digit hour in 24-hour format.

And file name conserve as follows

```

YYYYMMDDThhmmssZ_<title>.jsonl.gz

```

## Architecture

The service is built to handle log appending operations to S3:

- **main.py**: MCP server implementation that provides S3 operations. For logging purposes, the most relevant tools are:
  - `put`: Write new log files

- **scripts/commands.py**: Development tooling (formatting, linting)

## Workflow

1. A title and content are provided.
2. An S3 key is generated based on the current timestamp and the title.
3. the content is saved using this key.
