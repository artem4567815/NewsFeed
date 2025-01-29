document.addEventListener('DOMContentLoaded', () => {
    const currentUrl = window.location.pathname;
    console.log(currentUrl)
    const links = document.querySelectorAll('.filter-button');

    links.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        }
    });
});

function getWord(count, forms) {
    const mod100 = count % 100;
    const mod10 = count % 10;

    if (mod100 >= 11 && mod100 <= 19) {
        return forms[2];
    }

    if (mod10 === 1) {
        return forms[0];
    }

    if (mod10 >= 2 && mod10 <= 4) {
        return forms[1];
    }

    return forms[2];
}

const units = {
    seconds: ['секунда', 'секунды', 'секунд'],
    minutes: ['минута', 'минуты', 'минут'],
    hours: ['час', 'часа', 'часов'],
    days: ['день', 'дня', 'дней'],
};


function updateTimeAgo() {
    const timeElements = document.querySelectorAll('.time-passed');
    timeElements.forEach(timeElement => {
        const createdAt = timeElement.dataset.createdAt; 
        const timeAgo = calculateTimeAgo(new Date(createdAt));
        timeElement.textContent = timeAgo;
    });
}

function calculateTimeAgo(createdAt) {
    const now = new Date();
    const diff = now - createdAt;
    const now_days = now.getDate();

    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const dif_days = now_days - createdAt.getDate();
    console.log(units["seconds"]);
    if (seconds < 60) {
        return `${seconds} ${getWord(seconds, units["seconds"])} назад`;
    } else if (minutes < 60) {
        return `${minutes} ${getWord(minutes, units["minutes"])} назад`;
    } else if (hours < 24) {
        return `${hours} ${getWord(hours, units["hours"])} назад`;
    } else {
        return `${dif_days} ${getWord(dif_days, units["days"])} назад`;
    }
}

setInterval(updateTimeAgo, 30000);

updateTimeAgo();

function updateTime() {
    const timeElements = document.querySelectorAll('.time');
    timeElements.forEach(timeElement => {
        const createdAt = timeElement.dataset.createdAt; 
        const time = calculateTime(new Date(createdAt));
        timeElement.textContent = time;
    });

}   

function calculateTime(createdAt) {
    const now = new Date();
    const diff = now - createdAt;

    const day = String(createdAt.getDate()).padStart(2, "0");
    const month = String(createdAt.getMonth() + 1).padStart(2, "0");
    const year = String(createdAt.getFullYear()).slice(-2);
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const dif_days = now.getDate() - createdAt.getDate();
    if (days < 1) {
        return `Сегодня`;
    } else if (dif_days == 1) {
        return `Вчера`;
    } else{
        return `${day}.${month}.${year}`;
    }
}

setInterval(updateTime, 43200000);

updateTime();

let oldValue = "";
const searchInput = document.getElementById('search-bar').value;
const last = document.getElementById('prevButton');
const next = document.getElementById('nextButton');

function rewritwText() {
    const searchInput = document.getElementById('search-bar').value;
    if (oldValue !== searchInput){
        oldValue = searchInput
        currentIndex = -1;
        foundPosts = [];
    }

}

function isSearchBarActive() {
    return document.activeElement === searchInput || document.activeElement ===  next || document.activeElement ===  last;
}

document.addEventListener('click', () => {
    if (!isSearchBarActive()) {
        foundPosts.forEach(post => post.classList.remove('highlight'));
    } 
});

document.getElementById('search-bar').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        handleSearch();
    }
});
let currentIndex = -1;

let foundPosts = []; 

function handleSearch() {
    const searchInput = document.getElementById('search-bar').value.toLowerCase().trim();
    const posts = document.querySelectorAll('.news'); 

    if (currentIndex === -1) {
        foundPosts = [];

        posts.forEach(post => {
            const title = post.getAttribute('title')?.toLowerCase() || '';
            const description = post.getAttribute('short_description')?.toLowerCase() || '';

            if (title.includes(searchInput) || description.includes(searchInput)) {
                console.log(title);
                foundPosts.push(post);
            }
            post.classList.remove('highlight');
            
        });

        if (foundPosts.length === 0) {
            alert('Совпадений не найдено!');
            return;
        }
        currentIndex = 0;
    } else{
        currentIndex = (currentIndex + 1) % foundPosts.length;
    }
    

    foundPosts.forEach(post => post.classList.remove('highlight'));
    const currentPost = foundPosts[currentIndex];
    currentPost.scrollIntoView({ behavior: 'smooth', block: 'center' });
    currentPost.classList.add('highlight');
}

document.getElementById('prevButton').addEventListener('click', () => {
    goToPreviousPost();
});

document.getElementById('nextButton').addEventListener('click', () => {
    goToNextPost();
});

function goToNextPost() {
    if (foundPosts.length === 0) return;

    currentIndex = (currentIndex + 1) % foundPosts.length;

    scrollToPost(currentIndex);
}

function goToPreviousPost() {
    if (foundPosts.length === 0) return;

    currentIndex = (currentIndex - 1 + foundPosts.length) % foundPosts.length;

    scrollToPost(currentIndex);
}

function scrollToPost(index) {
    foundPosts.forEach(post => post.classList.remove('highlight'));

    const currentPost = foundPosts[index];
    if (currentPost) {
        console.log(currentPost);
        currentPost.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // Добавляем подсветку
        currentPost.classList.add('highlight');
        console.log('Класс добавлен:', currentPost.classList.contains('highlight')); // Должно быть true
        setTimeout(() => {
            console.log(currentPost.classList);
        }, 100);

    } else {
        console.error('Не удалось найти пост с индексом:', index);
    }
}

