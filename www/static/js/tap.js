const coin = document.getElementById('game_tap_coin');
const coinElement = document.querySelector('.coin');
const balance = document.querySelectorAll('.user_balance');

var taps = 0;

coin.addEventListener('click', (event) => {
    let number = document.createElement('span');
    number.className = 'tap_number';
    number.innerText = '+1';
    
    number.style.left = `${event.pageX}px`;
    number.style.top = `${event.pageY}px`;
    
    document.body.appendChild(number);
    
    number.addEventListener('animationend', function() {
        number.remove();
    })

    const rect = coin.getBoundingClientRect();
    const coinCenterX = rect.left + rect.width / 2;
    const coinCenterY = rect.top + rect.height / 2;

    const deltaX = event.clientX - coinCenterX;
    const deltaY = event.clientY - coinCenterY;

    const tiltX = -(deltaY / rect.height) * 30;
    const tiltY = (deltaX / rect.width) * 30;

    coinElement.style.setProperty('--tilt-x', `${tiltX}deg`);
    coinElement.style.setProperty('--tilt-y', `${tiltY}deg`);

    coinElement.classList.remove('tilt');
    
    requestAnimationFrame(() => {
        coinElement.classList.add('tilt');
    });

    coinElement.addEventListener('animationend', function() {
        coinElement.classList.remove('tilt');
    })
    taps++;
    balance.forEach(item => {
        item.innerHTML = Number(item.innerHTML) + 1;
    })
});

setInterval(() => {
    if (taps > 0) {
        fetch('/api/tap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify({ taps: taps })
        })
        .then(response => console.log(response))
        taps = 0;
    }
}, 5000);
