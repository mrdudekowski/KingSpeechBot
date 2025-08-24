"""
Tests for Input Validation Service
"""

import pytest
from services.validators import input_validator, ValidationResult

class TestInputValidator:
    """Test cases for InputValidator"""
    
    def test_validate_name_valid(self):
        """Test valid name validation"""
        result = input_validator.validate_name("Иван Петров", "ru")
        assert result.is_valid is True
        assert result.sanitized_value == "Иван Петров"
    
    def test_validate_name_invalid_empty(self):
        """Test empty name validation"""
        result = input_validator.validate_name("", "ru")
        assert result.is_valid is False
        assert "обязательно" in result.error_message
    
    def test_validate_name_invalid_too_short(self):
        """Test too short name validation"""
        result = input_validator.validate_name("А", "ru")
        assert result.is_valid is False
        assert "минимум 2 символа" in result.error_message
    
    def test_validate_name_invalid_too_long(self):
        """Test too long name validation"""
        long_name = "А" * 51
        result = input_validator.validate_name(long_name, "ru")
        assert result.is_valid is False
        assert "50 символов" in result.error_message
    
    def test_validate_name_invalid_characters(self):
        """Test name with invalid characters"""
        result = input_validator.validate_name("John123", "ru")
        assert result.is_valid is False
        assert "только буквы" in result.error_message
    
    def test_validate_phone_valid_plus7(self):
        """Test valid phone with +7 format"""
        result = input_validator.validate_phone("+79001234567", "ru")
        assert result.is_valid is True
        assert result.sanitized_value == "+79001234567"
    
    def test_validate_phone_valid_8(self):
        """Test valid phone with 8 format"""
        result = input_validator.validate_phone("89001234567", "ru")
        assert result.is_valid is True
        assert result.sanitized_value == "+79001234567"
    
    def test_validate_phone_invalid_format(self):
        """Test invalid phone format"""
        result = input_validator.validate_phone("1234567890", "ru")
        assert result.is_valid is False
        assert "формат" in result.error_message
    
    def test_validate_phone_invalid_empty(self):
        """Test empty phone validation"""
        result = input_validator.validate_phone("", "ru")
        assert result.is_valid is False
        assert "обязателен" in result.error_message
    
    def test_validate_email_valid(self):
        """Test valid email validation"""
        result = input_validator.validate_email("test@example.com", "ru")
        assert result.is_valid is True
        assert result.sanitized_value == "test@example.com"
    
    def test_validate_email_invalid_format(self):
        """Test invalid email format"""
        result = input_validator.validate_email("invalid-email", "ru")
        assert result.is_valid is False
        assert "формат" in result.error_message
    
    def test_validate_general_text_valid(self):
        """Test valid general text validation"""
        result = input_validator.validate_general_text("Hello, world!", lang="ru")
        assert result.is_valid is True
        assert result.sanitized_value == "Hello, world!"
    
    def test_validate_general_text_too_long(self):
        """Test too long text validation"""
        long_text = "A" * 1001
        result = input_validator.validate_general_text(long_text, lang="ru")
        assert result.is_valid is False
        assert "1000 символов" in result.error_message
    
    def test_validate_choice_valid(self):
        """Test valid choice validation"""
        allowed_choices = ["option1", "option2", "option3"]
        result = input_validator.validate_choice("option1", allowed_choices, "ru")
        assert result.is_valid is True
        assert result.sanitized_value == "option1"
    
    def test_validate_choice_invalid(self):
        """Test invalid choice validation"""
        allowed_choices = ["option1", "option2", "option3"]
        result = input_validator.validate_choice("invalid_option", allowed_choices, "ru")
        assert result.is_valid is False
        assert "недопустимый" in result.error_message
    
    def test_sanitize_text_removes_html(self):
        """Test HTML tag removal"""
        text_with_html = "<script>alert('test')</script>Hello <b>world</b>"
        sanitized = input_validator._sanitize_text(text_with_html)
        assert "<script>" not in sanitized
        assert "<b>" not in sanitized
        assert "Hello world" in sanitized
    
    def test_sanitize_text_removes_control_chars(self):
        """Test control character removal"""
        text_with_control = "Hello\x00world\x1f"
        sanitized = input_validator._sanitize_text(text_with_control)
        assert "\x00" not in sanitized
        assert "\x1f" not in sanitized
        assert "Hello world" in sanitized
    
    def test_validate_user_data_valid(self):
        """Test valid user data validation"""
        data = {
            "user_name": "Иван Петров",
            "phone": "+79001234567",
            "email": "test@example.com"
        }
        required_fields = ["user_name", "phone", "email"]
        
        results = input_validator.validate_user_data(data, required_fields, "ru")
        assert input_validator.is_valid_user_data(results) is True
        assert len(input_validator.get_validation_errors(results)) == 0
    
    def test_validate_user_data_invalid(self):
        """Test invalid user data validation"""
        data = {
            "user_name": "Иван Петров",
            "phone": "invalid_phone",
            "email": "invalid_email"
        }
        required_fields = ["user_name", "phone", "email"]
        
        results = input_validator.validate_user_data(data, required_fields, "ru")
        assert input_validator.is_valid_user_data(results) is False
        errors = input_validator.get_validation_errors(results)
        assert len(errors) == 2  # phone and email are invalid
