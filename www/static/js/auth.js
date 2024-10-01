var tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

const initData = tg.initData;
//const initData = 'query_id=AAGZHZtrAAAAAJkdm2srP0rs&user=%7B%22id%22%3A1805327769%2C%22first_name%22%3A%22Valentin%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22psh_valentin%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1721550259&hash=8449f7f7e6b9be063aeade1b0b9f95f1d310ff97e4e44787835220a21e45ecdc'

document.addEventListener('DOMContentLoaded', function() {
    if (initData) {
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + initData
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const html = data.html;
            localStorage.setItem('token', data.token);
            document.open();
            document.write(html);
            document.close();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } else {
        console.error('Not auth');
    }
});
