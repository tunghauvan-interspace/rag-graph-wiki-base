"""
Main entry point for RAG Graph Wiki Base Chat Application
"""
import sys
from chat_app import ChatApplication


def print_banner():
    """Print application banner."""
    print("\n" + "="*60)
    print("  RAG Graph Wiki Base - LLM Chat with Neo4j")
    print("="*60)
    print("  Commands:")
    print("    /history - Show conversation history")
    print("    /clear   - Clear conversation history")
    print("    /exit    - Exit the application")
    print("="*60 + "\n")


def main():
    """Main application loop."""
    print_banner()
    
    try:
        # Initialize chat application
        chat = ChatApplication()
        
        print("Chat started! Type your message or use commands.\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == "/exit":
                    print("\nGoodbye!")
                    break
                
                elif user_input.lower() == "/history":
                    history = chat.get_history_summary()
                    if not history:
                        print("\nNo conversation history found.\n")
                    else:
                        print("\n--- Conversation History ---")
                        for i, conv in enumerate(history, 1):
                            print(f"\n[{i}] {conv['timestamp']}")
                            print(f"You: {conv['user_message']}")
                            print(f"Assistant: {conv['assistant_message']}")
                        print("--- End of History ---\n")
                    continue
                
                elif user_input.lower() == "/clear":
                    chat.clear_history()
                    print()
                    continue
                
                # Regular chat
                response = chat.chat(user_input)
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"\nError during chat: {e}\n")
        
        # Cleanup
        chat.close()
        
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("Please check your .env file and ensure OPENAI_API_KEY is set.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error initializing application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
