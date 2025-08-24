"""
Tests for Rate Limiter Service
"""

import pytest
import time
from unittest.mock import patch
from services.rate_limiter import RateLimiter, RateLimitConfig

class TestRateLimiter:
    """Test cases for RateLimiter"""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization"""
        config = RateLimitConfig(max_requests=5, window_seconds=60)
        limiter = RateLimiter(config)
        
        assert limiter.config.max_requests == 5
        assert limiter.config.window_seconds == 60
    
    def test_rate_limiter_allows_requests_within_limit(self):
        """Test that rate limiter allows requests within limit"""
        config = RateLimitConfig(max_requests=3, window_seconds=60)
        limiter = RateLimiter(config)
        user_id = 12345
        
        # First 3 requests should be allowed
        assert limiter.is_allowed(user_id) is True
        assert limiter.is_allowed(user_id) is True
        assert limiter.is_allowed(user_id) is True
        
        # 4th request should be blocked
        assert limiter.is_allowed(user_id) is False
    
    def test_rate_limiter_resets_after_window(self, fast_rate_limiter):
        """Test that rate limiter resets after time window"""
        user_id = 12345
        
        # Make 2 requests
        assert fast_rate_limiter.is_allowed(user_id) is True
        assert fast_rate_limiter.is_allowed(user_id) is True
        
        # 3rd request should be blocked
        assert fast_rate_limiter.is_allowed(user_id) is False
        
        # Wait for window to expire (0.1 seconds)
        time.sleep(0.15)
        
        # Should be allowed again
        assert fast_rate_limiter.is_allowed(user_id) is True
    
    def test_rate_limiter_cooldown_period(self, fast_rate_limiter):
        """Test cooldown period after limit exceeded"""
        user_id = 12345
        
        # First request allowed
        assert fast_rate_limiter.is_allowed(user_id) is True
        
        # Second request blocked and user enters cooldown
        assert fast_rate_limiter.is_allowed(user_id) is False
        
        # Should still be blocked during cooldown
        assert fast_rate_limiter.is_allowed(user_id) is False
        
        # Wait for cooldown to expire (0.05 seconds)
        time.sleep(0.1)
        
        # Should be allowed again
        assert fast_rate_limiter.is_allowed(user_id) is True
    
    def test_get_remaining_requests(self):
        """Test getting remaining requests count"""
        config = RateLimitConfig(max_requests=5, window_seconds=60)
        limiter = RateLimiter(config)
        user_id = 12345
        
        # Initially should have 5 remaining
        assert limiter.get_remaining_requests(user_id) == 5
        
        # After 2 requests, should have 3 remaining
        limiter.is_allowed(user_id)
        limiter.is_allowed(user_id)
        assert limiter.get_remaining_requests(user_id) == 3
    
    def test_get_cooldown_remaining(self):
        """Test getting remaining cooldown time"""
        config = RateLimitConfig(max_requests=1, window_seconds=60, cooldown_seconds=5)
        limiter = RateLimiter(config)
        user_id = 12345
        
        # Initially no cooldown
        assert limiter.get_cooldown_remaining(user_id) == 0
        
        # Exceed limit to trigger cooldown
        limiter.is_allowed(user_id)
        limiter.is_allowed(user_id)  # This triggers cooldown
        
        # Should have some cooldown remaining
        remaining = limiter.get_cooldown_remaining(user_id)
        assert remaining > 0
        assert remaining <= 5
    
    def test_reset_user(self):
        """Test resetting user's rate limit"""
        config = RateLimitConfig(max_requests=2, window_seconds=60)
        limiter = RateLimiter(config)
        user_id = 12345
        
        # Make requests to reach limit
        limiter.is_allowed(user_id)
        limiter.is_allowed(user_id)
        assert limiter.is_allowed(user_id) is False
        
        # Reset user
        limiter.reset_user(user_id)
        
        # Should be allowed again
        assert limiter.is_allowed(user_id) is True
    
    def test_cleanup_old_data(self, fast_rate_limiter):
        """Test cleanup of old data"""
        user_id = 12345
        
        # Make some requests
        fast_rate_limiter.is_allowed(user_id)
        fast_rate_limiter.is_allowed(user_id)
        
        # Wait for window to expire (0.1 seconds)
        time.sleep(0.15)
        
        # Cleanup should remove old data
        fast_rate_limiter.cleanup_old_data()
        
        # Should be allowed again after cleanup
        assert fast_rate_limiter.is_allowed(user_id) is True
    
    def test_multiple_users_independent(self):
        """Test that multiple users have independent limits"""
        config = RateLimitConfig(max_requests=2, window_seconds=60)
        limiter = RateLimiter(config)
        user1 = 12345
        user2 = 67890
        
        # User 1 makes 2 requests
        assert limiter.is_allowed(user1) is True
        assert limiter.is_allowed(user1) is True
        assert limiter.is_allowed(user1) is False
        
        # User 2 should still be able to make requests
        assert limiter.is_allowed(user2) is True
        assert limiter.is_allowed(user2) is True
        assert limiter.is_allowed(user2) is False
    
    def test_edge_cases(self):
        """Test edge cases"""
        config = RateLimitConfig(max_requests=0, window_seconds=60)
        limiter = RateLimiter(config)
        user_id = 12345
        
        # With max_requests=0, no requests should be allowed
        assert limiter.is_allowed(user_id) is False
        
        # Test with negative user ID
        limiter2 = RateLimiter()
        assert limiter2.is_allowed(-12345) is True
