// ── MODIFICA INLINE ───────────────────────────────────────────────────────────
//
// Ogni campo (username, email) ha:
//   - un <input> con readonly di default → sembra testo normale
//   - una matita che chiama abilitaModifica(campo)
//   - due bottoni ✓ / ✕ nascosti che compaiono solo in modalità modifica
//
// Quando si clicca la matita:
//   1. L'input perde readonly → diventa editabile
//   2. La matita sparisce, appaiono ✓ e ✕
//   3. L'input prende il focus e il cursore va a fine testo
//
// Quando si clicca ✕ (annulla):
//   1. Il valore torna a quello originale (salvato prima della modifica)
//   2. L'input torna readonly
//   3. Riappaiono matita, spariscono ✓ e ✕

// Memorizza i valori originali al caricamento della pagina,
// così annullaModifica può ripristinarli anche dopo più modifiche.
const valoriOriginali = {};

document.addEventListener('DOMContentLoaded', function () {
    ['username', 'email'].forEach(function (campo) {
        const input = document.getElementById('input-' + campo);
        if (input) valoriOriginali[campo] = input.value;
    });
});


function abilitaModifica(campo) {
    const input   = document.getElementById('input-' + campo);
    const azioni  = document.getElementById('azioni-' + campo);
    const matita  = document.getElementById('matita-' + campo);

    // Salva il valore attuale nel caso l'utente annulli
    valoriOriginali[campo] = input.value;

    input.removeAttribute('readonly');
    input.classList.add('input-inline-attivo');

    azioni.style.display = 'flex';
    matita.style.display = 'none';

    // Porta il cursore a fine testo
    input.focus();
    const len = input.value.length;
    input.setSelectionRange(len, len);
}


function annullaModifica(campo) {
    const input   = document.getElementById('input-' + campo);
    const azioni  = document.getElementById('azioni-' + campo);
    const matita  = document.getElementById('matita-' + campo);

    // Ripristina il valore originale
    input.value = valoriOriginali[campo];

    input.setAttribute('readonly', '');
    input.classList.remove('input-inline-attivo');

    azioni.style.display = 'none';
    matita.style.display = '';
}


// ── TOGGLE PANEL (immagine e password) ───────────────────────────────────────

function togglePanel(id) {
    const tutti  = document.querySelectorAll('.panel-modifica');
    const target = document.getElementById(id);

    tutti.forEach(function (panel) {
        if (panel !== target) panel.style.display = 'none';
    });

    if (target.style.display === 'none') {
        // Se apre il panel immagine, salva l'src corrente dell'avatar
        // SOLO se non è già stato salvato — così se l'utente apre/chiude
        // più volte non sovrascriviamo con la base64 temporanea
        if (id === 'panel-immagine' && target._srcOriginale === undefined) {
            const img         = document.getElementById('avatar-profilo');
            const placeholder = document.getElementById('avatar-profilo-placeholder');
            target._srcOriginale        = img.src;
            // getComputedStyle dà il valore reale calcolato ('block', 'none'...)
            // invece di img.style.display che è vuoto se non impostato inline
            target._imgDisplayOriginale = window.getComputedStyle(img).display;
            target._phDisplayOriginale  = placeholder
                ? window.getComputedStyle(placeholder).display
                : null;
        }
        target.style.display = 'block';
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
        // Chiude il panel — se è quello immagine, ripristina l'avatar
        if (id === 'panel-immagine') {
            annullaImmagine(target);
        }
        target.style.display = 'none';
    }
}

// Ripristina avatar e input file allo stato prima dell'apertura del panel
function annullaImmagine(panel) {
    const img         = document.getElementById('avatar-profilo');
    const placeholder = document.getElementById('avatar-profilo-placeholder');
    const fileInput   = document.getElementById('id_immagine_profilo');
    const labelNome   = document.getElementById('nome-file');

    // Ripristina src e visibilità dell'avatar
    img.src           = panel._srcOriginale;
    img.style.display = panel._imgDisplayOriginale;

    if (placeholder && panel._phDisplayOriginale !== null) {
        placeholder.style.display = panel._phDisplayOriginale;
    }

    // Resetta l'input file
    if (fileInput) fileInput.value = '';
    if (labelNome) labelNome.textContent = 'Nessun file scelto';

    // Cancella i valori salvati così la prossima apertura
    // risalva lo stato aggiornato (es. dopo un salvataggio riuscito)
    panel._srcOriginale        = undefined;
    panel._imgDisplayOriginale = undefined;
    panel._phDisplayOriginale  = undefined;
}


// ── ANTEPRIMA AVATAR ─────────────────────────────────────────────────────────

function mostraNomeFile(input) {
    const labelNome = document.getElementById('nome-file');
    if (!input.files || !input.files[0]) {
        labelNome.textContent = 'Nessun file scelto';
        return;
    }
    labelNome.textContent = input.files[0].name;

    const reader = new FileReader();
    reader.onload = function (e) {
        const img         = document.getElementById('avatar-profilo');
        const placeholder = document.getElementById('avatar-profilo-placeholder');
        img.src           = e.target.result;
        img.style.display = 'block';
        if (placeholder) placeholder.style.display = 'none';
    };
    reader.readAsDataURL(input.files[0]);
}