document.addEventListener('DOMContentLoaded', function() {
    const townGoBack = document.getElementById('town_go_back');
    const sections = document.querySelectorAll('.town_section');
    const navItems = document.querySelectorAll('.nav_town_buttons');

    townGoBack.addEventListener('click', function() {
        navTown = document.getElementById('main_container');
        if ( navTown.style.display == 'none' ) {
            sections.forEach(section => {
                section.style.display = section.id === 'main_container' ? 'flex' : 'none';
            })
        } else {
            location.reload();
        }
    })
    
    function showSection(targetId) {
        sections.forEach(section => {
            section.style.display = section.id === targetId ? 'block' : 'none';
        })
    }

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            var targetId = this.getAttribute('data-target');
            showSection(targetId);
        })
    })
})
