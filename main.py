# ============================================================
# FICHIER 3: main.py
# Script principal pour lancer le scraping
# ============================================================

from scraper import WebScraperForRAG
from config import URLS_TO_SCRAPE, SCRAPING_CONFIG, OUTPUT_FILE
import os


def main():
    """Fonction principale"""
    print("=" * 60)
    print("SCRAPING WEB POUR RAG")
    print("=" * 60)
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    
    # Initialiser le scraper
    scraper = WebScraperForRAG(
        threads=SCRAPING_CONFIG["threads"],
        sleep_time=SCRAPING_CONFIG["sleep_time"]
    )
    
    print(f"\n📋 {len(URLS_TO_SCRAPE)} URLs à scraper")
    print(f"⚙️  Configuration: {SCRAPING_CONFIG['threads']} threads, {SCRAPING_CONFIG['sleep_time']}s délai\n")
    
    # Lancer le scraping
    documents = scraper.scrape_urls(
        urls=URLS_TO_SCRAPE,
        chunk_size=SCRAPING_CONFIG["chunk_size"]
    )
    
    # Sauvegarder les résultats
    if documents:
        scraper.save_to_json(documents, OUTPUT_FILE)
        
        # Afficher un résumé
        print("\n" + "=" * 60)
        print("RÉSUMÉ")
        print("=" * 60)
        for doc in documents:
            print(f"\n📄 {doc['title']}")
            print(f"   URL: {doc['url']}")
            print(f"   Chunks: {len(doc['chunks'])}")
            print(f"   Longueur: {doc['content_length']} caractères")
    else:
        print("\n⚠️  Aucun document extrait")


if __name__ == "__main__":
    main()