var townNameInput = document.getElementById('input_town_name');
const createTownButton = document.getElementById('button_create_town');

const validPattern = /^\p{L}+$/u;

townNameInput.addEventListener('input', function(event) {
    let text = this.value;
    if (!validPattern.test(text)) {
        this.value = text.replace(/[^a-zA-Zа-яА-ЯёЁ]/g, '');
    }
    
    text = this.value.trim();
    
    if (text.length > 1) {
        createTownButton.disabled = false;
    } else {
        createTownButton.disabled = true;
    }
});

function createTown() {
    fetch('/api/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ townName: townNameInput.value })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.text();
    })
    .then(html => {
        document.open();
        document.write(html);
        document.close();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
