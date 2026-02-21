from pymongo import MongoClient

# Connessione a Docker
client = MongoClient('mongodb://localhost:27017/')
db = client['arredamento_db']
collection = db['prodotti']


collection.delete_many({})
print("🧹 Pulizia database completata.")


prodotti = [
    # kitchen
    { 
        "nome": "Cucina White Modern", "categoria": "Cucina", "prezzo": 1899.00, 
        "descrizione": "Cucina luminosa con finiture bianche laccate e top resistente.", 
        "materiali": "Legno MDF laccato, Acciaio Inox", "dimensioni": "300 x 60 x 90 cm",
        "immagine": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=80" 
    },
    { 
        "nome": "Set Tavolo Pranzo", "categoria": "Cucina", "prezzo": 750.00, 
        "descrizione": "Tavolo rotondo scandinavo perfetto per 4 persone.", 
        "materiali": "Quercia massello, Gambe in metallo nero", "dimensioni": "Diametro 120 cm",
        "immagine": "https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=600&q=80" 
    },
    
    # living room
    { 
        "nome": "Divano Grigio Comfort", "categoria": "Soggiorno", "prezzo": 899.00, 
        "descrizione": "Divano angolare a 3 posti con penisola reversibile.", 
        "materiali": "Tessuto antimacchia, Struttura in pino", "dimensioni": "240 x 160 x 85 cm",
        "immagine": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80" 
    },
    { 
        "nome": "Poltrona Gialla", "categoria": "Soggiorno", "prezzo": 340.00, 
        "descrizione": "Poltrona di design color senape, ideale per angolo lettura.", 
        "materiali": "Velluto, Legno di faggio", "dimensioni": "80 x 75 x 90 cm",
        "immagine": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80" 
    },

    # badroom
    { 
        "nome": "Letto King Size", "categoria": "Camera", "prezzo": 1100.00, 
        "descrizione": "Letto matrimoniale con testata imbottita capitonné.", 
        "materiali": "Ecopelle, Struttura in ferro rinforzato", "dimensioni": "180 x 200 cm",
        "immagine": "https://images.unsplash.com/photo-1582582621959-48d27397dc69?auto=format&fit=crop&w=600&q=80" 
    },
    { 
        "nome": "Armadio Guardaroba", "categoria": "Camera", "prezzo": 850.00, 
        "descrizione": "Armadio a due ante scorrevoli con specchio integrato.", 
        "materiali": "Laminato effetto legno, Specchio", "dimensioni": "180 x 60 x 240 cm",
        "immagine": "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=600&q=80" 
    },

    # bathroom
    { 
        "nome": "Mobile Bagno Chic", "categoria": "Bagno", "prezzo": 550.00, 
        "descrizione": "Mobile sospeso con lavabo in ceramica incluso.", 
        "materiali": "Legno idrorepellente, Ceramica", "dimensioni": "100 x 45 x 50 cm",
        "immagine": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?auto=format&fit=crop&w=600&q=80" 
    },

    # office
    { 
        "nome": "Scrivania Vetro", "categoria": "Ufficio", "prezzo": 299.00, 
        "descrizione": "Scrivania moderna per ufficio o smart working.", 
        "materiali": "Vetro temperato, Acciaio cromato", "dimensioni": "140 x 70 x 75 cm",
        "immagine": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=600&q=80" 
    },
    { 
        "nome": "Sedia Ergonomica", "categoria": "Ufficio", "prezzo": 250.00, 
        "descrizione": "Sedia girevole con supporto lombare e braccioli regolabili.", 
        "materiali": "Rete traspirante, Plastica rinforzata", "dimensioni": "Standard regolabile",
        "immagine": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&w=600&q=80" 
    }
]

collection.insert_many(prodotti)
print(f"✅ Inseriti {len(prodotti)} prodotti aggiornati con dettagli e materiali!")