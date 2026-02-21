/* Global Variables */
let carrello = JSON.parse(localStorage.getItem('carrello')) || [];
let utenteLoggato = null;
let map = null;

/* Website Launch */
document.addEventListener('DOMContentLoaded', () => {
    console.log("Script caricato correttamente!");
    
    /* Check if user is logged */
    controllaLogin();
    
    /* Initialize Map */
    inizializzaMappa();
    
    /* DRender Saved Cart */
    aggiornaGraficaCarrello();
    
    /* Show Home on startup */
    mostraHome();
});

/* Modal Management (Login, Sign Up, Cart) */

function apriModal(tipo) {
    console.log("Apro modale:", tipo);
    document.getElementById('auth-modal').style.display = 'block';
    
    if (tipo === 'login') {
        document.getElementById('login-form').style.display = 'block';
        document.getElementById('register-form').style.display = 'none';
    } else {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    }
}

function chiudiModal(id) {
    document.getElementById(id).style.display = 'none';
}

function mostraForm(tipo) {
    /* Use the same logic as openModal to switch forms */
    apriModal(tipo);
}

/* Cart Management(Sidebar)*/

function apriCarrello() {
    console.log("Apro carrello");
    document.getElementById("cart-sidebar").style.width = "350px";
}

function chiudiCarrello() {
    document.getElementById("cart-sidebar").style.width = "0";
}

function salvaCarrello() {
    localStorage.setItem('carrello', JSON.stringify(carrello));
    aggiornaGraficaCarrello();
}

function aggiungiAlCarrello(id, nome, prezzo) {
    const esistente = carrello.find(i => i.id === id);
    if(esistente) {
        esistente.quantita++;
    } else {
        carrello.push({id: id, nome: nome, prezzo: prezzo, quantita: 1});
    }
    salvaCarrello();
    apriCarrello();
}

function cambiaQuantita(id, delta) {
    const item = carrello.find(i => i.id === id);
    if (!item) return;
    
    item.quantita += delta;
    if (item.quantita <= 0) {
        rimuoviDalCarrello(id);
    } else {
        salvaCarrello();
    }
}

function rimuoviDalCarrello(id) {
    carrello = carrello.filter(i => i.id !== id);
    salvaCarrello();
}

function aggiornaGraficaCarrello() {
    const div = document.getElementById('cart-items');
    const countSpan = document.getElementById('cart-count');
    const totalSpan = document.getElementById('cart-total');
    
    let totale = 0;
    let qty = 0;
    div.innerHTML = '';

    if (carrello.length === 0) {
        div.innerHTML = '<p style="text-align:center;">Il carrello è vuoto.</p>';
    }

    carrello.forEach(i => {
        totale += i.prezzo * i.quantita;
        qty += i.quantita;
        
        div.innerHTML += `
            <div class="cart-item">
                <div style="font-weight:600;">${i.nome}</div>
                <div style="color:#e67e22;">€ ${i.prezzo} cad.</div>
                
                <div class="cart-controls">
                    <div class="qty-wrapper">
                        <button class="qty-btn" onclick="cambiaQuantita('${i.id}', -1)">-</button>
                        <span>${i.quantita}</span>
                        <button class="qty-btn" onclick="cambiaQuantita('${i.id}', 1)">+</button>
                    </div>
                    <strong>€ ${(i.prezzo * i.quantita).toFixed(2)}</strong>
                </div>
                
                <button class="del-btn" style="color:red; background:none; border:none; margin-top:5px; cursor:pointer;" onclick="rimuoviDalCarrello('${i.id}')">Rimuovi</button>
            </div>
        `;
    });

    if(countSpan) countSpan.innerText = qty;
    if(totalSpan) totalSpan.innerText = totale.toFixed(2);
}

/* Home / Catalog Navigation */

function mostraHome() {
    document.getElementById('hero-section').style.display = 'flex';
    document.getElementById('catalog-section').style.display = 'none';
    const sb = document.querySelector('.search-bar');
    if(sb) sb.style.visibility = 'hidden';
    window.scrollTo({top: 0, behavior: 'smooth'});
}

function mostraCatalogo() {
    document.getElementById('hero-section').style.display = 'none';
    document.getElementById('catalog-section').style.display = 'flex';
    const sb = document.querySelector('.search-bar');
    if(sb) sb.style.visibility = 'visible';
    
    /* Apply Filters */
    applicaFiltri();
    
    document.getElementById('catalog-section').scrollIntoView({behavior: "smooth"});
}

/* Product & Filter Logic */

function applicaFiltri() {
    const search = document.getElementById('search-input').value;
    
    /* category */
    const catEl = document.querySelector('input[name="cat"]:checked');
    const categoria = catEl ? catEl.value : 'Tutte';

    /* prices */
    const minPrezzo = document.getElementById('min-price').value;
    const maxPrezzo = document.getElementById('max-price').value;

    const url = `/api/prodotti?search=${encodeURIComponent(search)}&categoria=${encodeURIComponent(categoria)}&min_prezzo=${minPrezzo}&max_prezzo=${maxPrezzo}`;
    
    caricaProdotti(url);
}

function caricaProdotti(url) {
    const container = document.getElementById('products-container');
    container.innerHTML = '<p style="grid-column: 1/-1; text-align:center;">Caricamento...</p>';
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            container.innerHTML = '';
            
            if(data.length === 0) {
                container.innerHTML = '<p style="grid-column: 1/-1; text-align:center;">Nessun prodotto trovato.</p>';
                return;
            }

            data.forEach(prod => {
                // Gestione Stella Preferiti
                const isFav = utenteLoggato && utenteLoggato.preferiti && utenteLoggato.preferiti.includes(prod._id);
                const starClass = isFav ? 'fas' : 'far';

                const card = document.createElement('div');
                card.classList.add('card');
                card.innerHTML = `
                    <article>
                        <img src="${prod.immagine}" alt="${prod.nome}" class="product-img">
                        <div class="card-header" style="display:flex; justify-content:space-between; align-items:center;">
                            <h3>${prod.nome}</h3>
                            <i id="star-${prod._id}" class="${starClass} fa-star star-icon" onclick="togglePreferito('${prod._id}')"></i>
                        </div>
                        <p style="font-size:0.9em; color:#666;">${prod.categoria}</p>
                        <p>${prod.descrizione}</p>
                        <p class="price">€ ${prod.prezzo}</p>
                        <button class="add-btn" onclick="aggiungiAlCarrello('${prod._id}', '${prod.nome}', ${prod.prezzo})">
                            <i class="fas fa-cart-plus"></i> Aggiungi
                        </button>
                    </article>
                `;
                container.appendChild(card);
            });
        })
        .catch(err => console.error("Errore Prodotti:", err));
}


/* user & login */

function controllaLogin() {
    fetch('/api/user_status')
    .then(r => r.json())
    .then(data => {
        if (data.logged_in) {
            utenteLoggato = data.user;
            document.getElementById('guest-buttons').style.display='none';
            document.getElementById('logged-user').style.display='inline-block';
            document.getElementById('username-display').innerText = data.user.nome;
        } else {
            utenteLoggato = null;
            document.getElementById('guest-buttons').style.display='flex';
            document.getElementById('logged-user').style.display='none';
        }
        
    })
    .catch(err => console.log("Errore Auth:", err));
}

function effettuaLogin() {
    const email = document.getElementById('login-email').value;
    const pass = document.getElementById('login-pass').value;
    
    fetch('/api/login', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password: pass })
    })
    .then(r => r.json())
    .then(d => {
        if(d.success) {
            chiudiModal('auth-modal');
            window.location.reload();
        } else {
            alert(d.message || "Errore login");
        }
    });
}

function effettuaRegistrazione() {
    const nome = document.getElementById('reg-nome').value;
    const cognome = document.getElementById('reg-cognome').value;
    const email = document.getElementById('reg-email').value;
    const pass = document.getElementById('reg-pass').value;

    if(!nome || !email || !pass) return alert("Compila i campi!");

    fetch('/api/register', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ nome, cognome, email, password: pass })
    })
    .then(r => r.json())
    .then(d => {
        if(d.success) {
            alert("Registrato!"); mostraForm('login');
        } else {
            alert(d.message);
        }
    });
}

function logout() {
    fetch('/api/logout', {method:'POST'}).then(() => window.location.reload());
}

function toggleUserMenu() {
    document.getElementById("user-dropdown-content").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn') && !event.target.matches('.dropbtn *')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            if (dropdowns[i].classList.contains('show')) dropdowns[i].classList.remove('show');
        }
    }
}

/* account date */

function apriDatiPersonali() {
    if (!utenteLoggato) return;
    document.getElementById('prof-nome').value = utenteLoggato.nome || '';
    document.getElementById('prof-cognome').value = utenteLoggato.cognome || '';
    document.getElementById('prof-nascita').value = utenteLoggato.data_nascita || '';
    document.getElementById('prof-indirizzo').value = utenteLoggato.indirizzo || '';
    document.getElementById('prof-civico').value = utenteLoggato.civico || '';
    document.getElementById('prof-citta').value = utenteLoggato.citta || '';
    document.getElementById('prof-cap').value = utenteLoggato.cap || '';
    document.getElementById('personal-data-modal').style.display = 'block';
}

function salvaProfilo() {
    const dati = {
        nome: document.getElementById('prof-nome').value,
        cognome: document.getElementById('prof-cognome').value,
        data_nascita: document.getElementById('prof-nascita').value,
        indirizzo: document.getElementById('prof-indirizzo').value,
        civico: document.getElementById('prof-civico').value,
        citta: document.getElementById('prof-citta').value,
        cap: document.getElementById('prof-cap').value
    };
    fetch('/api/update_profile', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(dati)
    }).then(r => r.json()).then(d => {
        if(d.success) {
            alert("Salvato!");
            utenteLoggato = d.user;
            document.getElementById('username-display').innerText = utenteLoggato.nome;
            chiudiModal('personal-data-modal');
        }
    });
}


