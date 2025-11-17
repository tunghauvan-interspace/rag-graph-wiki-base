"""
LangChain Chat Application
Simple LLM chat interface using LangChain with Neo4j for conversation storage.
"""
import os
from datetime import datetime
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from neo4j_manager import Neo4jManager

load_dotenv()


class ChatApplication:
    """Simple chat application using LangChain and Neo4j."""
    
    def __init__(self, session_id: str = None):
        """
        Initialize chat application.
        
        Args:
            session_id: Optional session ID, generates one if not provided
        """
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize OpenAI LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        # Initialize Neo4j
        self.neo4j = Neo4jManager()
        self.neo4j_connected = self.neo4j.connect()
        
        # System message
        self.system_message = SystemMessage(
            content="You are a helpful AI assistant. Provide clear and concise answers."
        )
        
        print(f"✓ Chat application initialized (Session: {self.session_id})")
    
    def load_history(self) -> List:
        """Load conversation history from Neo4j."""
        if not self.neo4j_connected:
            return []
        
        history = self.neo4j.get_conversation_history(self.session_id)
        messages = []
        
        for conv in history:
            messages.append(HumanMessage(content=conv["user_message"]))
            messages.append(AIMessage(content=conv["assistant_message"]))
        
        return messages
    
    def chat(self, user_input: str) -> str:
        """
        Send a message and get a response.
        
        Args:
            user_input: User's message
            
        Returns:
            Assistant's response
        """
        # Load conversation history
        history = self.load_history()
        
        # Build messages for LLM
        messages = [self.system_message] + history + [HumanMessage(content=user_input)]
        
        # Get response from LLM
        response = self.llm.invoke(messages)
        assistant_message = response.content
        
        # Save to Neo4j
        if self.neo4j_connected:
            timestamp = datetime.now().isoformat()
            self.neo4j.save_conversation(
                self.session_id,
                user_input,
                assistant_message,
                timestamp
            )
        
        return assistant_message
    
    def get_history_summary(self) -> List[Dict]:
        """Get conversation history summary."""
        if not self.neo4j_connected:
            return []
        return self.neo4j.get_conversation_history(self.session_id)
    
    def clear_history(self):
        """Clear conversation history for current session."""
        if self.neo4j_connected:
            self.neo4j.clear_session(self.session_id)
            print(f"✓ Cleared history for session {self.session_id}")
    
    def close(self):
        """Close connections."""
        if self.neo4j_connected:
            self.neo4j.close()
