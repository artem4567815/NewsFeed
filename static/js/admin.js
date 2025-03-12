const createLink = document.getElementById('create-link');
const moderateLink = document.getElementById('moderate-link');
const createSection = document.getElementById('create-section');
const moderateSection = document.getElementById('moderate-section');
const createType = document.getElementById('create-type');
const wallpaperForm = document.getElementById('wallpaper-form');
const postForm = document.getElementById('post-form');
const createPost = document.getElementById('create-post');

createLink.addEventListener('click', (e) => {
    e.preventDefault();
    createSection.classList.remove('hidden');
    moderateSection.classList.add('hidden');
});

moderateLink.addEventListener('click', (e) => {
    e.preventDefault();
    createSection.classList.add('hidden');
    moderateSection.classList.remove('hidden');
});

createType.addEventListener('change', () => {
    const value = createType.value;

    let route = '';

    if (value === 'wallpaper') {
        route = '/admin/wallpaper';
    } else if (value === 'post') {
        // route = '/admin/post';
        createPost.classList.remove('hidden');
    }

    if (route) {
        window.location.href = route;
    }
});