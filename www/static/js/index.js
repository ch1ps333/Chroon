towns = [ // [name / town population]
    ['Hamlet', 0],
    ['Village', 2500],
    ['Town', 25000],
    ['Small City', 100000],
    ['City', 500000],
    ['Metropolis', 1000000]
];

function showConfirm(textConfirm, acceptButton) {
    return new Promise((resolve) => {
        let modal = document.createElement('div');
        modal.id = 'myModal';
        modal.style.display = 'block';
        modal.style.position = 'fixed';
        modal.style.zIndex = '1';
        modal.style.left = '0';
        modal.style.top = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.overflow = 'auto';
        modal.style.backgroundColor = 'rgb(0,0,0)';
        modal.style.backgroundColor = 'rgba(0,0,0,0.4)';
        modal.style.paddingTop = '60px';

        let modalContent = document.createElement('div');
        modalContent.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        modalContent.style.margin = '5% auto';
        modalContent.style.padding = '20px';
        modalContent.style.width = '80%';
        modalContent.style.height = 'auto';
        modalContent.style.minHeight = '30%';
        modalContent.style.borderRadius = '8px';
        modalContent.style.display = 'flex';
        modalContent.style.flexDirection = 'column';
        modalContent.style.justifyContent = 'space-between';

        let closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.color = '#aaa';
        closeBtn.style.marginLeft = 'auto';
        closeBtn.style.fontSize = '28px';
        closeBtn.style.fontWeight = 'bold';
        closeBtn.onclick = function() {
            document.body.removeChild(modal);
            resolve(false);
        };
        closeBtn.onmouseover = function() {
            closeBtn.style.color = 'black';
            closeBtn.style.cursor = 'pointer';
        };
        closeBtn.onmouseout = function() {
            closeBtn.style.color = '#aaa';
        };

        let text = document.createElement('p');
        text.innerText = textConfirm;

        let okBtn = document.createElement('button');
        okBtn.innerText = acceptButton;
        okBtn.style.marginTop = 'auto';
        okBtn.style.border = 'none';
        okBtn.style.borderRadius = '8px';
        okBtn.style.height = '5vh';
        okBtn.style.fontWeight = 'bold';
        okBtn.style.color = 'white';
        okBtn.style.background = 'linear-gradient(190deg, #00a5f7 0%, #0052f6 100%)';
        okBtn.onclick = function() {
            document.body.removeChild(modal);
            resolve(true);
        };

        modalContent.appendChild(closeBtn);
        modalContent.appendChild(text);
        modalContent.appendChild(okBtn);
        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        window.onclick = function(event) {
            if (event.target == modal) {
                document.body.removeChild(modal);
                resolve(false);
            }
        };
    });
}


function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.position = 'fixed';
    notification.style.top = '10px';
    notification.style.left = '50%';
    notification.style.transform = 'translateX(-50%)';
    notification.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    notification.style.color = 'white';
    notification.style.borderRadius = '5px';
    notification.style.zIndex = '9999';
    notification.style.display = 'flex';
    notification.style.alignItems = 'center';
    notification.style.justifyContent = 'space-between';
    notification.style.width = '90%';
    notification.style.height = 'auto';
    notification.style.minHeight = '3%';
    notification.style.padding = '8px';
    notification.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.5)';

    const messageText = document.createElement('span');
    messageText.innerText = message;
    messageText.style.wordBreak = 'break-word';
    messageText.style.whiteSpace = 'pre-wrap';
    messageText.style.width = '80%';
    notification.appendChild(messageText);

    const closeButton = document.createElement('button');
    closeButton.innerText = '×';
    closeButton.style.marginLeft = '20px';
    closeButton.style.backgroundColor = 'transparent';
    closeButton.style.color = 'white';
    closeButton.style.border = 'none';
    closeButton.style.fontSize = '20px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.width = '5%';
    notification.appendChild(closeButton);

    document.body.appendChild(notification);

    const removeNotification = () => {
        if (notification) {
            notification.remove();
        }
    };

    const timeoutId = setTimeout(removeNotification, 3000);

    closeButton.addEventListener('click', () => {
        clearTimeout(timeoutId);
        removeNotification();
    });
}

function giveBalance(sum) {
    const balance = document.querySelectorAll('.user_balance');

    balance.forEach(item => {
        item.innerHTML = Number(item.innerHTML) + sum;
    })
}

function takeBalance(sum) {
    const balance = document.querySelectorAll('.user_balance');

    balance.forEach(item => {
        item.innerHTML = Number(item.innerHTML) - sum;
    })
}

function copyText() {
    navigator.clipboard.writeText('https://t.me/labozahyshator_bot?start=kentId' + userData.tgID);
}

document.addEventListener('DOMContentLoaded', function() {
    topProgressBar = document.getElementById('top_progress');
    requireScore = document.getElementById('require_score');
    currentLeague = document.getElementById('current_league');

    topProgressBar.style.width = (userData.townPopulation / towns[userData.townRank][1] * 100) + '%';
    requireScore.innerHTML = towns[userData.townRank][1];
    currentLeague.innerHTML = towns[userData.townRank - 1][0];
})