"""
Test cases for RAG Graph Wiki Base
Simple tests to validate core functionality
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


class TestNeo4jManager(unittest.TestCase):
    """Test Neo4j Manager functionality."""
    
    @patch('neo4j_manager.GraphDatabase')
    def test_connect_success(self, mock_graph_db):
        """Test successful Neo4j connection."""
        from neo4j_manager import Neo4jManager
        
        # Mock driver
        mock_driver = Mock()
        mock_driver.verify_connectivity.return_value = None
        mock_graph_db.driver.return_value = mock_driver
        
        manager = Neo4jManager()
        result = manager.connect()
        
        self.assertTrue(result)
        mock_graph_db.driver.assert_called_once()
        mock_driver.verify_connectivity.assert_called_once()
    
    @patch('neo4j_manager.GraphDatabase')
    def test_connect_failure(self, mock_graph_db):
        """Test Neo4j connection failure."""
        from neo4j_manager import Neo4jManager
        
        # Mock driver that fails
        mock_graph_db.driver.side_effect = Exception("Connection failed")
        
        manager = Neo4jManager()
        result = manager.connect()
        
        self.assertFalse(result)
    
    @patch('neo4j_manager.GraphDatabase')
    def test_save_conversation(self, mock_graph_db):
        """Test saving conversation to Neo4j."""
        from neo4j_manager import Neo4jManager
        
        # Mock driver and session
        mock_driver = Mock()
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        
        manager = Neo4jManager()
        manager.driver = mock_driver
        
        # Save conversation
        manager.save_conversation(
            "test_session",
            "Hello",
            "Hi there!",
            "2025-01-17T15:00:00"
        )
        
        # Verify session was called
        mock_driver.session.assert_called_once()


class TestChatApplication(unittest.TestCase):
    """Test Chat Application functionality."""
    
    @patch('chat_app.ChatOpenAI')
    @patch('chat_app.Neo4jManager')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_chat_app_initialization(self, mock_neo4j, mock_llm):
        """Test chat application initialization."""
        from chat_app import ChatApplication
        
        # Mock Neo4j connection
        mock_neo4j_instance = Mock()
        mock_neo4j_instance.connect.return_value = True
        mock_neo4j.return_value = mock_neo4j_instance
        
        # Create chat app
        app = ChatApplication(session_id="test_session")
        
        self.assertEqual(app.session_id, "test_session")
        self.assertTrue(app.neo4j_connected)
    
    @patch('chat_app.ChatOpenAI')
    @patch('chat_app.Neo4jManager')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_chat_response(self, mock_neo4j, mock_llm):
        """Test chat response generation."""
        from chat_app import ChatApplication
        
        # Mock Neo4j
        mock_neo4j_instance = Mock()
        mock_neo4j_instance.connect.return_value = True
        mock_neo4j_instance.get_conversation_history.return_value = []
        mock_neo4j.return_value = mock_neo4j_instance
        
        # Mock LLM response
        mock_llm_instance = Mock()
        mock_response = Mock()
        mock_response.content = "This is a test response"
        mock_llm_instance.invoke.return_value = mock_response
        mock_llm.return_value = mock_llm_instance
        
        # Create chat app and send message
        app = ChatApplication()
        response = app.chat("Hello")
        
        self.assertEqual(response, "This is a test response")
        mock_llm_instance.invoke.assert_called_once()
    
    @patch.dict('os.environ', {}, clear=True)
    def test_chat_app_missing_api_key(self):
        """Test chat application with missing API key."""
        from chat_app import ChatApplication
        
        with self.assertRaises(ValueError) as context:
            ChatApplication()
        
        self.assertIn("OPENAI_API_KEY", str(context.exception))


class TestMainFunctionality(unittest.TestCase):
    """Test main application functionality."""
    
    def test_imports(self):
        """Test that all modules can be imported."""
        try:
            import main
            import chat_app
            import neo4j_manager
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_print_banner(self):
        """Test print banner function."""
        from main import print_banner
        
        # Should not raise any exceptions
        try:
            print_banner()
        except Exception as e:
            self.fail(f"print_banner raised exception: {e}")


if __name__ == '__main__':
    unittest.main()
