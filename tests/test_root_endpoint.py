"""Tests for GET / endpoint using AAA pattern."""
import pytest


def test_root_redirects_to_static_index(client):
    """Arrange-Act-Assert: Verify root endpoint redirects to /static/index.html."""
    # Arrange (no setup needed)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert "/static/index.html" in response.headers["location"]


def test_root_with_follow_redirects_returns_html(client):
    """Arrange-Act-Assert: Verify following redirect serves index.html."""
    # Arrange (no setup needed)
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
