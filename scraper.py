# ============================================================
# FICHIER 1: scraper.py
# Ce fichier contient la classe principale pour le scraping
# ============================================================

import json
from datetime import datetime
from typing import List, Dict, Optional
from trafilatura import extract
from trafilatura.downloads import add_to_compressed_dict, buffered_downloads, load_download_buffer
from trafilatura.settings import use_config
import hashlib


class WebScraperForRAG:
    """Scraper web optimisé pour alimenter un système RAG"""
    
    def __init__(self, threads: int = 2, sleep_time: int = 5):
        self.threads = threads
        self.sleep_time = sleep_time
        self.config = use_config()
        self.config.set("DEFAULT", "EXTRACTION_TIMEOUT", "30")
        
    def generate_chunk_id(self, url: str, index: int) -> str:
        """Génère un ID unique pour chaque chunk"""
        base = f"{url}_{index}"
        return hashlib.md5(base.encode()).hexdigest()[:16]
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Découpe le texte en chunks avec overlap"""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            if end < text_length:
                last_period = text.rfind('.', start, end)
                if last_period > start + chunk_size // 2:
                    end = last_period + 1
            
            chunks.append(text[start:end].strip())
            start = end - overlap if end < text_length else end
            
        return chunks
    
    def extract_metadata(self, html_content: str, url: str) -> Dict:
        """Extrait les métadonnées du contenu HTML"""
        metadata = extract(
            html_content,
            include_comments=False,
            include_tables=True,
            output_format='json',
            config=self.config
        )
        
        if metadata:
            try:
                return json.loads(metadata)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def process_url(self, url: str, html_content: str, chunk_size: int = 1000) -> Optional[Dict]:
        """Traite une URL et retourne un document structuré"""
        if not html_content:
            return None
        
        main_content = extract(html_content, config=self.config)
        
        if not main_content:
            return None
        
        metadata = self.extract_metadata(html_content, url)
        chunks = self.split_into_chunks(main_content, chunk_size)
        
        document = {
            "url": url,
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "date": metadata.get("date", ""),
            "scraped_at": datetime.now().isoformat(),
            "description": metadata.get("description", ""),
            "language": metadata.get("language", "fr"),
            "content_length": len(main_content),
            "chunks": [
                {
                    "id": self.generate_chunk_id(url, i),
                    "text": chunk,
                    "chunk_index": i,
                    "chunk_length": len(chunk)
                }
                for i, chunk in enumerate(chunks)
            ],
            "metadata": {
                "domain": url.split('/')[2] if len(url.split('/')) > 2 else "",
                "total_chunks": len(chunks),
                "categories": metadata.get("categories", []),
                "tags": metadata.get("tags", [])
            }
        }
        
        return document
    
    def scrape_urls(self, urls: List[str], chunk_size: int = 1000) -> List[Dict]:
        """Scrape multiple URLs"""
        documents = []
        url_store = add_to_compressed_dict(urls)
        
        while not url_store.done:
            bufferlist, url_store = load_download_buffer(
                url_store, 
                sleep_time=self.sleep_time
            )
            
            for url, html_content in buffered_downloads(bufferlist, self.threads):
                print(f"Traitement de: {url}")
                
                document = self.process_url(url, html_content, chunk_size)
                
                if document:
                    documents.append(document)
                    print(f"✓ {url} - {document['content_length']} caractères - {len(document['chunks'])} chunks")
                else:
                    print(f"✗ Échec: {url}")
        
        return documents
    
    def save_to_json(self, documents: List[Dict], output_file: str):
        """Sauvegarde les documents en JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Sauvegardé dans {output_file}")
        print(f"  - {len(documents)} documents")
        print(f"  - {sum(len(d['chunks']) for d in documents)} chunks")