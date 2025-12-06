"""
Base Integration Framework for Agent Zero
Provides core functionality for 3rd party service integrations
"""

import time
import json
import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from threading import Lock
from collections import deque
import urllib.parse
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    max_requests: int = 100  # Max requests per window
    window_seconds: int = 60  # Time window in seconds
    burst_size: int = 10  # Max burst requests


@dataclass
class RetryConfig:
    """Retry configuration with exponential backoff"""
    max_retries: int = 3
    initial_delay: float = 1.0  # Initial delay in seconds
    max_delay: float = 60.0  # Maximum delay in seconds
    backoff_factor: float = 2.0  # Exponential backoff multiplier
    retry_on_status: List[int] = field(default_factory=lambda: [429, 500, 502, 503, 504])


@dataclass
class OAuthConfig:
    """OAuth 2.0 configuration"""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    authorize_url: Optional[str] = None
    token_url: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class RateLimiter:
    """Token bucket rate limiter with sliding window"""

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.requests = deque()
        self.lock = Lock()

    def acquire(self) -> bool:
        """Attempt to acquire a rate limit token"""
        with self.lock:
            now = time.time()
            window_start = now - self.config.window_seconds

            # Remove old requests outside the window
            while self.requests and self.requests[0] < window_start:
                self.requests.popleft()

            # Check if we can make a request
            if len(self.requests) < self.config.max_requests:
                self.requests.append(now)
                return True

            return False

    def wait_time(self) -> float:
        """Get the time to wait before next request is allowed"""
        with self.lock:
            if len(self.requests) < self.config.max_requests:
                return 0.0

            now = time.time()
            oldest_request = self.requests[0]
            window_start = now - self.config.window_seconds

            if oldest_request < window_start:
                return 0.0

            return oldest_request + self.config.window_seconds - now


class WebhookHandler:
    """Webhook handler for receiving events from services"""

    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.secret_key: Optional[str] = None

    def register(self, event_type: str, handler: Callable):
        """Register a webhook handler for an event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def verify_signature(self, payload: bytes, signature: str, algorithm: str = "sha256") -> bool:
        """Verify webhook signature"""
        if not self.secret_key:
            return True  # No verification if no secret

        if algorithm == "sha256":
            expected = hashlib.sha256(self.secret_key.encode() + payload).hexdigest()
        elif algorithm == "sha1":
            expected = hashlib.sha1(self.secret_key.encode() + payload).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        return signature == expected

    def handle(self, event_type: str, payload: Dict[str, Any]) -> List[Any]:
        """Handle a webhook event"""
        results = []
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    result = handler(payload)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Webhook handler error for {event_type}: {e}")
                    results.append({"error": str(e)})
        return results


class BaseIntegration(ABC):
    """
    Base class for all 3rd party service integrations

    Provides:
    - OAuth 2.0 authentication
    - API key management
    - Rate limiting
    - Retry logic with exponential backoff
    - Webhook support
    - Request/response logging
    """

    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        rate_limit: Optional[RateLimitConfig] = None,
        retry_config: Optional[RetryConfig] = None
    ):
        self.name = name
        self.config = config
        self.enabled = config.get("enabled", True)

        # Rate limiting
        self.rate_limiter = RateLimiter(rate_limit or RateLimitConfig())

        # Retry configuration
        self.retry_config = retry_config or RetryConfig()

        # OAuth configuration
        self.oauth = OAuthConfig(
            client_id=config.get("client_id"),
            client_secret=config.get("client_secret"),
            redirect_uri=config.get("redirect_uri"),
            authorize_url=config.get("authorize_url"),
            token_url=config.get("token_url"),
            scopes=config.get("scopes", []),
            access_token=config.get("access_token"),
            refresh_token=config.get("refresh_token")
        )

        # API key (alternative to OAuth)
        self.api_key = config.get("api_key")

        # Webhook handler
        self.webhook = WebhookHandler()
        self.webhook.secret_key = config.get("webhook_secret")

        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "rate_limited": 0,
            "retries": 0
        }

        logger.info(f"Initialized {self.name} integration")

    @abstractmethod
    def get_base_url(self) -> str:
        """Get the base URL for the API"""
        pass

    def is_authenticated(self) -> bool:
        """Check if integration is authenticated"""
        if self.api_key:
            return True
        if self.oauth.access_token:
            # Check if token is expired
            if self.oauth.token_expires_at:
                return datetime.now() < self.oauth.token_expires_at
            return True
        return False

    def get_oauth_authorize_url(self, state: Optional[str] = None) -> str:
        """Generate OAuth authorization URL"""
        if not self.oauth.authorize_url:
            raise ValueError("OAuth authorize URL not configured")

        params = {
            "client_id": self.oauth.client_id,
            "redirect_uri": self.oauth.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.oauth.scopes)
        }

        if state:
            params["state"] = state

        query_string = urllib.parse.urlencode(params)
        return f"{self.oauth.authorize_url}?{query_string}"

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        if not self.oauth.token_url:
            raise ValueError("OAuth token URL not configured")

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.oauth.redirect_uri,
            "client_id": self.oauth.client_id,
            "client_secret": self.oauth.client_secret
        }

        response = self._make_request(
            "POST",
            self.oauth.token_url,
            data=data,
            skip_auth=True
        )

        self.oauth.access_token = response.get("access_token")
        self.oauth.refresh_token = response.get("refresh_token")

        if "expires_in" in response:
            self.oauth.token_expires_at = datetime.now() + timedelta(seconds=response["expires_in"])

        return response

    def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh the access token using refresh token"""
        if not self.oauth.refresh_token:
            raise ValueError("No refresh token available")

        if not self.oauth.token_url:
            raise ValueError("OAuth token URL not configured")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.oauth.refresh_token,
            "client_id": self.oauth.client_id,
            "client_secret": self.oauth.client_secret
        }

        response = self._make_request(
            "POST",
            self.oauth.token_url,
            data=data,
            skip_auth=True
        )

        self.oauth.access_token = response.get("access_token")

        if "refresh_token" in response:
            self.oauth.refresh_token = response["refresh_token"]

        if "expires_in" in response:
            self.oauth.token_expires_at = datetime.now() + timedelta(seconds=response["expires_in"])

        return response

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for requests"""
        headers = {}

        if self.oauth.access_token:
            headers["Authorization"] = f"Bearer {self.oauth.access_token}"
        elif self.api_key:
            # Override in subclass for service-specific header
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        skip_auth: bool = False,
        skip_rate_limit: bool = False
    ) -> Any:
        """
        Make an HTTP request with rate limiting, retries, and authentication

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: Full URL or path (will be appended to base_url if relative)
            params: URL query parameters
            data: Form data
            json_data: JSON request body
            headers: Additional headers
            skip_auth: Skip authentication headers
            skip_rate_limit: Skip rate limiting

        Returns:
            Response data (parsed JSON or raw text)
        """
        # Check if enabled
        if not self.enabled:
            raise RuntimeError(f"{self.name} integration is disabled")

        # Rate limiting
        if not skip_rate_limit:
            while not self.rate_limiter.acquire():
                wait_time = self.rate_limiter.wait_time()
                logger.warning(f"Rate limited, waiting {wait_time:.2f}s")
                self.stats["rate_limited"] += 1
                time.sleep(wait_time)

        # Build full URL
        if not url.startswith("http"):
            url = self.get_base_url().rstrip("/") + "/" + url.lstrip("/")

        # Add query parameters
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"

        # Build headers
        request_headers = {
            "User-Agent": f"AgentZero-Integration/{self.name}",
            "Accept": "application/json"
        }

        if not skip_auth:
            request_headers.update(self.get_auth_headers())

        if headers:
            request_headers.update(headers)

        # Prepare request body
        request_data = None
        if json_data is not None:
            request_data = json.dumps(json_data).encode("utf-8")
            request_headers["Content-Type"] = "application/json"
        elif data is not None:
            request_data = urllib.parse.urlencode(data).encode("utf-8")
            request_headers["Content-Type"] = "application/x-www-form-urlencoded"

        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                self.stats["total_requests"] += 1

                # Create and send request
                req = urllib.request.Request(
                    url,
                    data=request_data,
                    headers=request_headers,
                    method=method
                )

                with urllib.request.urlopen(req, timeout=30) as response:
                    response_data = response.read()

                    # Try to parse as JSON
                    try:
                        result = json.loads(response_data.decode("utf-8"))
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        result = response_data.decode("utf-8", errors="replace")

                    self.stats["successful_requests"] += 1
                    return result

            except urllib.error.HTTPError as e:
                last_exception = e
                status_code = e.code

                # Read error response
                try:
                    error_data = json.loads(e.read().decode("utf-8"))
                except:
                    error_data = {"error": e.reason}

                logger.error(f"HTTP {status_code} error: {error_data}")

                # Check if we should retry
                if status_code in self.retry_config.retry_on_status and attempt < self.retry_config.max_retries:
                    delay = min(
                        self.retry_config.initial_delay * (self.retry_config.backoff_factor ** attempt),
                        self.retry_config.max_delay
                    )
                    logger.info(f"Retrying in {delay:.2f}s (attempt {attempt + 1}/{self.retry_config.max_retries})")
                    self.stats["retries"] += 1
                    time.sleep(delay)
                    continue

                # Token refresh on 401
                if status_code == 401 and self.oauth.refresh_token and not skip_auth:
                    logger.info("Access token expired, refreshing...")
                    try:
                        self.refresh_access_token()
                        # Retry with new token
                        self.stats["retries"] += 1
                        continue
                    except Exception as refresh_error:
                        logger.error(f"Token refresh failed: {refresh_error}")

                self.stats["failed_requests"] += 1
                raise RuntimeError(f"HTTP {status_code}: {error_data}")

            except Exception as e:
                last_exception = e
                logger.error(f"Request error: {e}")

                if attempt < self.retry_config.max_retries:
                    delay = min(
                        self.retry_config.initial_delay * (self.retry_config.backoff_factor ** attempt),
                        self.retry_config.max_delay
                    )
                    logger.info(f"Retrying in {delay:.2f}s (attempt {attempt + 1}/{self.retry_config.max_retries})")
                    self.stats["retries"] += 1
                    time.sleep(delay)
                    continue

                self.stats["failed_requests"] += 1
                raise

        # All retries exhausted
        self.stats["failed_requests"] += 1
        raise RuntimeError(f"Request failed after {self.retry_config.max_retries} retries: {last_exception}")

    def get_stats(self) -> Dict[str, Any]:
        """Get integration statistics"""
        success_rate = 0.0
        if self.stats["total_requests"] > 0:
            success_rate = (self.stats["successful_requests"] / self.stats["total_requests"]) * 100

        return {
            **self.stats,
            "success_rate": f"{success_rate:.2f}%",
            "enabled": self.enabled,
            "authenticated": self.is_authenticated()
        }

    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "rate_limited": 0,
            "retries": 0
        }

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the integration connection

        Returns:
            Dict with status and details
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} enabled={self.enabled}>"
