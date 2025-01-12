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

    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    console.log(diff)
    if (seconds < 60) {
        return `${seconds} секунд назад`;
    } else if (minutes < 60) {
        return `${minutes} минут назад`;
    } else if (hours < 24) {
        return `${hours} часов назад`;
    } else {
        return `${days} дней назад`;
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
    
    if (days < 1) {
        return `Сегодня`;
    } else if (days >= 1 && days < 2) {
        return `Вчера`;
    } else{
        return `${day}.${month}.${year}`;
    }
}

setInterval(updateTime, 43200000);

updateTime();