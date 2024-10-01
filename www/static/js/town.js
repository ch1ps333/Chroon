housePrices = [
    1000,
    5000,
    10000,
    100000,
    1000000,
]

async function buyHouse(houseID, text, acceptButton) {
    if (userData.balance >= housePrices[houseID - 1]) {
        confirmResponse = await showConfirm(text, acceptButton);

        if (confirmResponse) {
            fetch('/api/buy_house', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ houseID: houseID })
            })
            .then(response => {
                if (response.ok) {
                    showNotification('The purchase of the house was successful');
                }
            })
            .then(data => {
                const balance = document.querySelectorAll('.user_balance');
                const townResidentialPlaces = document.getElementById('town_residential_places');

                balance.forEach(item => {
                    item.innerHTML = data.user.balance;
                })

                townResidentialPlaces.innerHTML = data.user.town_residential_places;
            })
            .catch(error => {
                showNotification("Error, please try again later");
            });
            
        }
    } else {
        showNotification("Insufficient balance");
    }
}

async function buyWorkplace(workID, text, acceptButton) {
    if (userData.balance >= workplacePrices[workID - 1]) {
        confirmResponse = await showConfirm(text, acceptButton);

        if (confirmResponse) {
            fetch('/api/buy_workplace', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ workID: workID })
            })
            .then(response => {
                if (response.ok) {
                    showNotification('The purchase of the workplace was successful');
                }
            })
            .then(data => {
                const balance = document.querySelectorAll('.user_balance');
                const townResidentialPlaces = document.getElementById('town_residential_places');

                balance.forEach(item => {
                    item.innerHTML = data.user.balance;
                })

                townResidentialPlaces.innerHTML = data.user.town_residential_places;
            })
            .catch(error => {
                showNotification("Error, please try again later");
            });
            
        }
    } else {
        showNotification("Insufficient balance");
    }
}


document.addEventListener('DOMContentLoaded', function() {
    withdrawTownBallanceButton = document.getElementById('withdraw_town_balance');
    townBalance = document.getElementById('town_balance').innerHTML;

    withdrawTownBallanceButton.addEventListener('click', function() {
        if (townBalance != '0') {
            fetch('/api/withdraw_town_balance', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                }
            })
            .then(response => {
                if (response.ok) {
                    townBalanceBlock = document.getElementById('town_balance');
                    giveBalance(Number(townBalanceBlock.innerHTML));
                    townBalanceBlock.innerHTML = '0';
                    showNotification('The city balance is charged to the personal balance')
                } else {
                    showNotification('Error request')
                }
            })
        }
    })
})