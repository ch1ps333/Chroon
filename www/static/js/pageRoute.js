document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section');
    const navItems = document.querySelectorAll('.nav_items');
    const earnGames = document.querySelectorAll('.earn_games');
    const blockGames = document.getElementById('earn_games');
    const games = document.querySelectorAll('.games');
    const townMenu = document.getElementById('town_menu');

    function showSection(targetId) {
        sections.forEach(section => {
            section.style.display = section.id === targetId ? 'block' : 'none';
            if (targetId == 'earn_container') {
                blockGames.style.display = 'flex';
            }
        })
        games.forEach(game => {
            game.style.display = 'none';
        })
    }

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            var targetId = this.getAttribute('data-target');
            showSection(targetId);
        })
    })

    function runGame(targetId) {
        blockGames.style.display = 'none';
        games.forEach(game => {
            game.style.display = game.id === targetId ? 'block' : 'none';
        })
    }

    earnGames.forEach(item => {
        item.addEventListener('click', function() {
            var targetId = this.getAttribute('data-target');
            runGame(targetId)
        })
    })

    townMenu.addEventListener('click', function openTown() {
        fetch('/town', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
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

    })
})
