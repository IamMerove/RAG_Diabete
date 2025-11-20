import time
from rag_engine import LocalRAGSystem
from config import OUTPUT_FILE
import os

def main():
    print("=" * 50)
    print("🦙 RAG LOCAL AVEC OLLAMA")
    print("=" * 50)

    # Instanciation
    rag = LocalRAGSystem()
    
    # Vérification de la DB
    json_path = str(OUTPUT_FILE)
    if not os.path.exists("db_storage_local"):
        print("🏗️  Première construction de la base vectorielle...")
        rag.load_and_index(json_path)
    else:
        print("💾 Base de données trouvée sur le disque.")
        rag.setup_pipeline()

    # Boucle de chat
    print("\n💬 Pose ta question (quit pour quitter)")
    while True:
        q = input("\nToi: ")
        if q.lower() in ["quit", "exit"]:
            break
        
        start_time = time.time()
        print("🤔 Réflexion en cours...", end="", flush=True)
        
        try:
            response = rag.ask(q)
            duration = time.time() - start_time
            print(f"\r🤖 Assistant ({duration:.2f}s) :\n")
            print(response)
        except Exception as e:
            print(f"\n❌ Erreur : {e}")

if __name__ == "__main__":
    main()