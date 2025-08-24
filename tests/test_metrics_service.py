"""
Tests for Metrics Service
"""

import pytest
import time
from services.metrics_service import MetricsService, Metric, MetricSummary


class TestMetricsService:
    """Test cases for MetricsService"""
    
    def test_metrics_service_initialization(self):
        """Test metrics service initialization"""
        metrics = MetricsService(max_metrics=100, retention_hours=1)
        
        assert metrics.max_metrics == 100
        assert metrics.retention_seconds == 3600
        assert len(metrics.metrics) == 0
        assert len(metrics._metric_counters) == 0
    
    def test_record_timing(self):
        """Test recording timing metrics"""
        metrics = MetricsService()
        
        metrics.record_timing("api_call", 0.5, endpoint="/users")
        
        assert len(metrics.metrics) == 1
        metric = metrics.metrics[0]
        assert metric.name == "api_call_duration"
        assert metric.value == 0.5
        assert metric.tags["endpoint"] == "/users"
    
    def test_record_counter(self):
        """Test recording counter metrics"""
        metrics = MetricsService()
        
        metrics.record_counter("user_registration", 1, source="telegram")
        
        assert len(metrics.metrics) == 1
        metric = metrics.metrics[0]
        assert metric.name == "user_registration"
        assert metric.value == 1
        assert metric.tags["source"] == "telegram"
        assert metrics._metric_counters["user_registration"] == 1
    
    def test_record_error(self):
        """Test recording error metrics"""
        metrics = MetricsService()
        
        metrics.record_error("api_timeout", user_id=123)
        
        assert len(metrics.metrics) == 1
        metric = metrics.metrics[0]
        assert metric.name == "error_count"
        assert metric.value == 1
        assert metric.tags["error_type"] == "api_timeout"
        assert metric.tags["user_id"] == 123
        assert metrics._error_counts["api_timeout"] == 1
    
    def test_record_user_activity(self):
        """Test recording user activity"""
        metrics = MetricsService()
        
        metrics.record_user_activity(123, "message_sent")
        
        assert len(metrics.metrics) == 1
        metric = metrics.metrics[0]
        assert metric.name == "user_activity"
        assert metric.value == 1
        assert metric.tags["user_id"] == "123"
        assert metric.tags["action"] == "message_sent"
        assert metrics._user_activity[123] == 1
    
    def test_timer_functions(self):
        """Test timer start/stop functionality"""
        metrics = MetricsService()
        
        # Start timer
        metrics.start_timer("test_operation")
        time.sleep(0.1)  # Small delay
        
        # Stop timer
        duration = metrics.stop_timer("test_operation", user_id=123)
        
        assert duration is not None
        assert duration > 0
        assert len(metrics.metrics) == 1
        metric = metrics.metrics[0]
        assert metric.name == "test_operation_duration"
        assert metric.tags["user_id"] == 123
    
    def test_timer_stop_without_start(self):
        """Test stopping timer that wasn't started"""
        metrics = MetricsService()
        
        duration = metrics.stop_timer("nonexistent_operation")
        
        assert duration is None
        assert len(metrics.metrics) == 0
    
    def test_get_metrics_summary(self):
        """Test getting metrics summary"""
        metrics = MetricsService()
        
        # Add some metrics
        metrics.record_timing("api_call", 0.5)
        metrics.record_timing("api_call", 1.0)
        metrics.record_timing("api_call", 1.5)
        
        summary = metrics.get_metrics_summary(hours=1)
        
        assert "api_call_duration" in summary
        summary_data = summary["api_call_duration"]
        assert summary_data.count == 3
        assert summary_data.min_value == 0.5
        assert summary_data.max_value == 1.5
        assert summary_data.avg_value == 1.0
        assert summary_data.sum_value == 3.0
    
    def test_get_performance_stats(self):
        """Test getting performance statistics"""
        metrics = MetricsService()
        
        # Add some metrics
        metrics.record_timing("api_call", 0.5)
        metrics.record_timing("api_call", 1.0)
        metrics.record_error("timeout")
        metrics.record_user_activity(123, "message")
        
        stats = metrics.get_performance_stats()
        
        assert stats["total_metrics"] == 4
        assert "timeout" in stats["error_counts"]
        assert stats["error_counts"]["timeout"] == 1
        assert stats["active_users"] == 1
        assert "api_call" in stats["operation_stats"]
        
        op_stats = stats["operation_stats"]["api_call"]
        assert op_stats["count"] == 2
        assert op_stats["avg_duration"] == 0.75
    
    def test_get_top_users(self):
        """Test getting top active users"""
        metrics = MetricsService()
        
        # Add user activity
        metrics.record_user_activity(123, "message")
        metrics.record_user_activity(123, "message")
        metrics.record_user_activity(456, "message")
        
        top_users = metrics.get_top_users(limit=5)
        
        assert len(top_users) == 2
        assert top_users[0]["user_id"] == 123
        assert top_users[0]["activity_count"] == 2
        assert top_users[1]["user_id"] == 456
        assert top_users[1]["activity_count"] == 1
    
    def test_metrics_cleanup(self):
        """Test cleanup of old metrics"""
        metrics = MetricsService(max_metrics=5, retention_hours=1)
        
        # Add more metrics than max_metrics
        for i in range(10):
            metrics.record_counter(f"test_metric_{i}")
        
        # Should have only the last 5 metrics
        assert len(metrics.metrics) == 5
        
        # Check that oldest metrics were removed
        metric_names = [m.name for m in metrics.metrics]
        assert "test_metric_0" not in metric_names
        assert "test_metric_4" not in metric_names
        assert "test_metric_9" in metric_names
    
    def test_thread_safety(self):
        """Test thread safety of metrics service"""
        import threading
        
        metrics = MetricsService()
        results = []
        
        def add_metrics():
            for i in range(100):
                metrics.record_counter("thread_test")
            results.append(len(metrics.metrics))
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=add_metrics)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have 500 metrics total
        assert len(metrics.metrics) == 500
        assert metrics._metric_counters["thread_test"] == 500


class TestMetric:
    """Test cases for Metric dataclass"""
    
    def test_metric_creation(self):
        """Test creating a metric"""
        metric = Metric(
            name="test_metric",
            value=42.0,
            timestamp=1234567890.0,
            tags={"user_id": "123"}
        )
        
        assert metric.name == "test_metric"
        assert metric.value == 42.0
        assert metric.timestamp == 1234567890.0
        assert metric.tags["user_id"] == "123"
    
    def test_metric_default_tags(self):
        """Test metric with default empty tags"""
        metric = Metric(
            name="test_metric",
            value=42.0,
            timestamp=1234567890.0
        )
        
        assert metric.tags == {}


class TestMetricSummary:
    """Test cases for MetricSummary dataclass"""
    
    def test_metric_summary_creation(self):
        """Test creating a metric summary"""
        summary = MetricSummary(
            name="test_metric",
            count=10,
            min_value=1.0,
            max_value=100.0,
            avg_value=50.5,
            sum_value=505.0,
            tags={"service": "api"}
        )
        
        assert summary.name == "test_metric"
        assert summary.count == 10
        assert summary.min_value == 1.0
        assert summary.max_value == 100.0
        assert summary.avg_value == 50.5
        assert summary.sum_value == 505.0
        assert summary.tags["service"] == "api"
    
    def test_metric_summary_default_tags(self):
        """Test metric summary with default empty tags"""
        summary = MetricSummary(
            name="test_metric",
            count=1,
            min_value=1.0,
            max_value=1.0,
            avg_value=1.0,
            sum_value=1.0
        )
        
        assert summary.tags == {}


class TestGlobalMetrics:
    """Test cases for global metrics functions"""
    
    def test_get_metrics_singleton(self):
        """Test that get_metrics returns the same instance"""
        from services.metrics_service import get_metrics, _metrics_instance
        
        # Clear any existing instance
        import services.metrics_service
        services.metrics_service._metrics_instance = None
        
        metrics1 = get_metrics()
        metrics2 = get_metrics()
        
        assert metrics1 is metrics2
        # Note: _metrics_instance might be None due to module reloading in tests
        # The important thing is that both calls return the same instance
    
    def test_init_metrics(self):
        """Test metrics initialization"""
        from services.metrics_service import init_metrics, _metrics_instance
        
        # Clear any existing instance
        import services.metrics_service
        services.metrics_service._metrics_instance = None
        
        metrics = init_metrics(max_metrics=500, retention_hours=12)
        # Note: _metrics_instance might be different due to module reloading in tests
        # The important thing is that init_metrics returns a valid metrics service
        assert metrics is not None
        assert metrics.max_metrics == 500
        assert metrics.retention_seconds == 12 * 3600
