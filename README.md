# 🛋️ Arredamento.it - Piattaforma E-Commerce

Un'applicazione web e-commerce completa per la vendita di mobili e arredamento moderno, costruita con **Python (Flask)** e **MongoDB**. Il progetto include sia l'interfaccia utente per i clienti (catalogo, carrello, checkout) sia un Pannello di Amministrazione avanzato per la gestione del negozio.

## ✨ Funzionalità Principali

### 👤 Lato Cliente (User)
* **Catalogo Dinamico:** Visualizzazione prodotti con filtri per categoria (Cucina, Soggiorno, ecc.), range di prezzo e barra di ricerca.
* **Carrello Intelligente:** Carrello laterale (Offcanvas) gestito in `localStorage` con la possibilità di selezionare/deselezionare i singoli articoli prima del checkout.
* **Autenticazione:** Registrazione e Login con password criptate.
* **Checkout & Profilo:** Simulazione di checkout con scelta dell'indirizzo e metodo di pagamento (Carta/Contanti). Storico ordini visibile nell'area personale.

### 🛠️ Lato Amministratore (Admin Panel)
* **Dashboard Statistiche:** Monitoraggio di incassi, ordini totali, spese di spedizione e utile netto.
* **Performance Categorie:** Analisi visiva (con progress bar) delle vendite e degli utili suddivisi per ambiente.
* **Gestione Prodotti (CRUD):** Creazione, modifica e cancellazione dei prodotti con **upload delle immagini** integrato.
* **Gestione Ordini:** Visualizzazione in tempo reale degli ordini effettuati dai clienti, con dettagli sui prodotti acquistati e calcolo delle spese di gestione.

---

## 💻 Stack Tecnologico

* **Backend:** Python 3, Flask
* **Database:** MongoDB (libreria `pymongo`)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Librerie Extra:** `werkzeug.security` (hashing password), FontAwesome (Icone)

---

## 🚀 Requisiti e Installazione

Assicurati di avere installati sul tuo computer **Python 3** e **MongoDB** (in esecuzione locale sulla porta di default `27017`).
