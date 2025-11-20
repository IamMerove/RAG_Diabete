# # ============================================================
# # FICHIER 5: test_scraper.py (OPTIONNEL)
# # Tests unitaires
# # ============================================================

# from scraper import WebScraperForRAG


# def test_chunk_splitting():
#     """Test du découpage en chunks"""
#     scraper = WebScraperForRAG()
    
#     text = "Phrase 1. " * 100  # 1100 caractères
#     chunks = scraper.split_into_chunks(text, chunk_size=500, overlap=100)
    
#     print(f"Texte de {len(text)} caractères découpé en {len(chunks)} chunks")
#     assert len(chunks) > 1, "Le texte devrait être découpé"
#     print("✓ Test réussi")


# def test_scraping():
#     """Test du scraping sur une URL"""
#     scraper = WebScraperForRAG()
    
#     urls = ["https://www.ameli.fr/la-reunion/assure/sante/themes/diabete-adulte/diabete-symptomes-evolution/diagnostic-diabete"]
    
#     documents = scraper.scrape_urls(urls, chunk_size=1000)
    
#     assert len(documents) > 0, "Au moins un document devrait être extrait"
#     assert documents[0]['chunks'], "Le document devrait contenir des chunks"
#     print("✓ Test de scraping réussi")


# if __name__ == "__main__":
#     print("Lancement des tests...\n")
#     test_chunk_splitting()
#     test_scraping()
#     print("\n✓ Tous les tests passés")