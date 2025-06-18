# Claude Log MCP

A simple MCP (Model Context Protocol) server for storing logs to Amazon S3 with automatic timestamp-based partitioning.

## Overview

Claude Log MCP is designed to provide AI assistants with a simple way to store structured logs in S3. It automatically organizes logs by timestamp and compresses them for efficient storage.

## Features

- Automatic timestamp-based S3 path generation (year/month/day/hour partitioning)
- GZIP compression for all log entries
- JSONL format for structured logging
- Simple single-tool interface

## S3 Path Structure

Logs are stored with the following path structure:

```
s3://<bucket>/<prefix>/year=<YYYY>/month=<MM>/day=<DD>/hour=<HH>/<timestamp>_<title>.jsonl.gz
```

Example:
```
s3://my-logs/logs/year=2024/month=01/day=15/hour=14/20240115T143022Z_error_report.jsonl.gz
```

## Prerequisites

- AWS Account with S3 access
- AWS credentials with permissions to write to S3
- Docker (for containerized deployment)

## Environment Variables

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: AWS region (defaults to us-west-1)
- `AWS_S3_BUCKET`: Target S3 bucket name
- `AWS_S3_PREFIX`: Prefix for log paths (defaults to "logs")

## Usage

### Standalone Docker

```bash
docker run --rm -it \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_REGION=your_region \
  -e AWS_S3_BUCKET=your_bucket \
  -e AWS_S3_PREFIX=logs \
  nakatatsu/claude-log-mcp
```

### Building from Source

Clone the repository and build:

```bash
docker build -t claude-log-mcp .
```

## API

The MCP server exposes a single tool:

### `put`

Write a log entry to S3 with automatic timestamp-based path generation.

**Parameters:**
- `title` (string): Title for the log entry (used in filename)
- `content` (string): Content to be logged

**Returns:**
```json
{
  "success": true,
  "key": "logs/year=2024/month=01/day=15/hour=14/20240115T143022Z_error_report.jsonl.gz"
}
```

## Log Format

Each log file contains GZIP-compressed JSONL (JSON Lines) with the following structure:

```json
{
  "timestamp": "2024-01-15T14:30:22Z",
  "title": "Error Report",
  "content": "Detailed error information..."
}
```

## License

MIT