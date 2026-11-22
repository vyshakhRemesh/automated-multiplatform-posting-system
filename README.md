# Automated Multi-Platform Posting System

A FastAPI-based application that automatically publishes a message containing a single CTA URL across multiple social media and content platforms through their official APIs.

## Features

- REST API using FastAPI.
- Accepts messages up to 200 characters.
- Validates that each message contains exactly one HTTP/HTTPS CTA URL.
- Publishes content to five platforms.
- Handles each platform independently.
- One platform's failure does not interrupt other publishing operations.
- Returns individual publishing status, post URL, public accessibility, timestamp, and error details.
- Uses environment variables to manage API credentials.

## Supported Platforms

| Platform  | Integration        |
| --------- | ------------------ |
| Mastodon  | Official REST API  |
| Bluesky   | AT Protocol API    |
| Reddit    | Reddit API         |
| WordPress | WordPress REST API |
| LinkedIn  | LinkedIn REST API  |

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- Pytest

## Project Structure

```text
app/
├── platforms/
│   ├── base.py
│   ├── mastodon.py
│   ├── bluesky.py
│   ├── reddit.py
│   ├── wordpress.py
│   └── linkedin.py
├── services/
│   └── posting_service.py
├── utils/
│   └── url_validator.py
├── config.py
├── main.py
└── schemas.py

tests/
├── test_api.py
├── test_posting_service.py
└── test_schemas.py

.env.example
.gitignore
requirements.txt
README.md
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Automated-Multi-Platform-Posting-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Add the credentials for the platforms you want to configure.

Never commit your `.env` file or expose API credentials publicly.

## Running the Application

```bash
uvicorn app.main:app --reload --port 4000
```

The API will be available at:

```text
http://localhost:4000
```

Interactive API documentation:

```text
http://localhost:4000/docs
```

## API Usage

### Endpoint

```http
POST /posting
```

### Request Body

```json
{
  "message": "Check out this update https://example.com"
}
```

### Validation Rules

- Message must not be empty.
- Maximum message length is 200 characters.
- Exactly one CTA URL must be present.
- CTA URL must use HTTP or HTTPS.

### Sample Response

The following is an illustrative response showing successful and failed platform operations:

```json
{
  "success": true,
  "results": [
    {
      "platform": "Mastodon",
      "status": "success",
      "posted_url": "https://mastodon.social/@username/example",
      "public_access": true,
      "datetime": "2026-11-22T17:36:28Z",
      "error": null
    },
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/profile/username/post/example",
      "public_access": true,
      "datetime": "2026-11-22T17:36:29Z",
      "error": null
    },
    {
      "platform": "Reddit",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "datetime": null,
      "error": "Reddit credentials are not configured"
    }
  ]
}
```

## Error Handling

Each platform is processed independently. Exceptions and request timeouts are caught separately, allowing the remaining platforms to continue publishing.

If credentials are missing or an API request fails, the corresponding platform returns a failed status with an error message.

## Testing

Run the automated test suite:

```bash
pytest -v
```

Current test coverage includes:

- Request validation.
- Missing CTA URL.
- Multiple CTA URLs.
- Message length validation.
- Invalid URL validation.
- Independent platform failure handling.
- API endpoint success.
- API endpoint validation errors.

**Latest test result: 8 passed.**

## Live Integration Testing

Mastodon and Bluesky were successfully tested with real API credentials and published posts.

Reddit, WordPress, and LinkedIn integrations are implemented but were not live-tested because their credentials were not configured.

## Security

- API credentials are stored in environment variables.
- `.env` is excluded from Git.
- `.env.example` provides the required configuration template.
- No API credentials should be committed to the repository.

## Author

**Vyshakh R**
