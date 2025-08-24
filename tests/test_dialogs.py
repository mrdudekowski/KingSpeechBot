"""
Tests for Dialog System
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from cursor import Context, Step
from dialogs.main_survey import MainSurveyDialog

class TestMainSurveyDialog:
    """Test cases for MainSurveyDialog"""
    
    def setup_method(self):
        """Setup test environment"""
        self.dialog = MainSurveyDialog()
        self.context = Mock(spec=Context)
        self.context.telegram = Mock()
        self.context.telegram.id = 12345
        self.context.telegram.username = "test_user"
        
        # Mock context methods
        self.context.get_variable = Mock(side_effect=lambda key, default=None: {
            'interface_lang': 'ru',
            'user_name': '',
            'phone': '',
            'email': '',
            'telegram_username': 'test_user',
            'tutor_questions_left': 3,
            'test_current_question': 0,
            'test_score': 0,
            'test_answers': []
        }.get(key, default))
        self.context.set_variable = Mock()
        self.context.get_user_message = Mock(return_value="")
    
    def test_dialog_initialization(self):
        """Test dialog initialization"""
        assert self.dialog.name == "main_survey"
        assert self.dialog.description == "Main survey for course matching"
        assert "survey" in self.dialog.tags
        assert self.dialog.priority == 100
    
    def test_language_selection_step(self):
        """Test language selection step"""
        step = self.dialog._language_selection_step(self.context)
        
        assert isinstance(step, Step)
        assert "Пожалуйста, выберите язык" in step.message
        assert len(step.options) == 2
        assert "🇷🇺 Русский" in step.options
        assert "🇬🇧 English" in step.options
    
    def test_process_language_selection_ru(self):
        """Test Russian language selection"""
        self.context.get_user_message.return_value = "🇷🇺 Русский"
        
        step = self.dialog._process_language_selection(self.context, "🇷🇺 Русский")
        
        self.context.set_variable.assert_called_with('interface_lang', 'ru')
    
    def test_process_language_selection_en(self):
        """Test English language selection"""
        step = self.dialog._process_language_selection(self.context, "🇬🇧 English")
        
        self.context.set_variable.assert_called_with('interface_lang', 'en')
    
    def test_name_validation_valid(self):
        """Test valid name validation"""
        self.context.get_user_message.return_value = "Иван Петров"
        
        step = self.dialog._process_name(self.context)
        
        # Check that set_variable was called with user_name
        self.context.set_variable.assert_any_call('user_name', "Иван Петров")
    
    def test_name_validation_invalid(self):
        """Test invalid name validation"""
        self.context.get_user_message.return_value = "123"
        
        step = self.dialog._process_name(self.context)
        
        # Should return to name step with error message
        assert "недопустимые символы" in step.message or "только буквы" in step.message
    
    def test_phone_validation_valid(self):
        """Test valid phone validation"""
        self.context.get_user_message.return_value = "+79001234567"
        
        step = self.dialog._process_phone(self.context)
        
        # Check that set_variable was called with phone
        self.context.set_variable.assert_any_call("phone", "+79001234567")
    
    def test_phone_validation_invalid(self):
        """Test invalid phone validation"""
        self.context.get_user_message.return_value = "invalid_phone"
        
        step = self.dialog._process_phone(self.context)
        
        # Should return to phone step with error message
        assert "Неверный формат" in step.message or "некорректный" in step.message
