function mostraNomeFile(input) {
    // 1. Aggiorna il testo col nome del file
    const labelNome = document.getElementById('nome-file');
    if (!input.files || !input.files[0]) {
        labelNome.textContent = 'Nessun file scelto';
        return;
    }
    labelNome.textContent = input.files[0].name;

    // 2. Anteprima immagine con FileReader
    // FileReader legge il file localmente senza inviarlo al server.
    // readAsDataURL converte il file in una stringa base64
    // che può essere usata direttamente come src di un <img>.
    const reader = new FileReader();

    reader.onload = function(e) {
        // e.target.result contiene la stringa base64 del file
        const img = document.getElementById('avatar-profilo');
        const placeholder = document.getElementById('avatar-profilo-placeholder');

        img.src = e.target.result;
        img.style.display = 'block';

        // Se esiste il placeholder (cerchio con iniziale), lo nasconde
        if (placeholder) {
            placeholder.style.display = 'none';
        }
    };

    // Avvia la lettura — quando finisce scatta reader.onload
    reader.readAsDataURL(input.files[0]);
}
