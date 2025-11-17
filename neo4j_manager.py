"""
Neo4j Database Manager for RAG Graph Wiki Base
Handles connections and operations with Neo4j database.
"""
import os
from typing import List, Dict, Optional
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class Neo4jManager:
    """Manages Neo4j database connections and operations."""
    
    def __init__(self):
        """Initialize Neo4j connection."""
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password123")
        self.driver = None
        
    def connect(self):
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Verify connectivity
            self.driver.verify_connectivity()
            print(f"✓ Connected to Neo4j at {self.uri}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to Neo4j: {e}")
            return False
    
    def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()
            print("✓ Neo4j connection closed")
    
    def save_conversation(self, session_id: str, user_message: str, 
                         assistant_message: str, timestamp: str):
        """
        Save a conversation exchange to Neo4j.
        
        Args:
            session_id: Unique session identifier
            user_message: User's message
            assistant_message: Assistant's response
            timestamp: Timestamp of the conversation
        """
        with self.driver.session() as session:
            session.execute_write(
                self._create_conversation_node,
                session_id, user_message, assistant_message, timestamp
            )
    
    @staticmethod
    def _create_conversation_node(tx, session_id: str, user_message: str,
                                 assistant_message: str, timestamp: str):
        """Create conversation node in Neo4j."""
        query = """
        MERGE (s:Session {id: $session_id})
        CREATE (c:Conversation {
            user_message: $user_message,
            assistant_message: $assistant_message,
            timestamp: $timestamp
        })
        CREATE (s)-[:HAS_CONVERSATION]->(c)
        RETURN c
        """
        tx.run(query, session_id=session_id, user_message=user_message,
               assistant_message=assistant_message, timestamp=timestamp)
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """
        Retrieve conversation history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of conversations to retrieve
            
        Returns:
            List of conversation dictionaries
        """
        with self.driver.session() as session:
            result = session.execute_read(
                self._fetch_conversation_history,
                session_id, limit
            )
            return result
    
    @staticmethod
    def _fetch_conversation_history(tx, session_id: str, limit: int):
        """Fetch conversation history from Neo4j."""
        query = """
        MATCH (s:Session {id: $session_id})-[:HAS_CONVERSATION]->(c:Conversation)
        RETURN c.user_message as user_message,
               c.assistant_message as assistant_message,
               c.timestamp as timestamp
        ORDER BY c.timestamp DESC
        LIMIT $limit
        """
        result = tx.run(query, session_id=session_id, limit=limit)
        conversations = []
        for record in result:
            conversations.append({
                "user_message": record["user_message"],
                "assistant_message": record["assistant_message"],
                "timestamp": record["timestamp"]
            })
        return list(reversed(conversations))  # Return in chronological order
    
    def clear_session(self, session_id: str):
        """
        Clear all conversations for a session.
        
        Args:
            session_id: Session identifier
        """
        with self.driver.session() as session:
            session.execute_write(self._delete_session, session_id)
    
    @staticmethod
    def _delete_session(tx, session_id: str):
        """Delete session and its conversations."""
        query = """
        MATCH (s:Session {id: $session_id})-[:HAS_CONVERSATION]->(c:Conversation)
        DETACH DELETE c, s
        """
        tx.run(query, session_id=session_id)
