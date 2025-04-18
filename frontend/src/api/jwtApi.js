import axios from 'axios';

const jwtApi = axios.create({
    baseURL: import.meta.env.VITE_BASE_URL,
});

// Добавляем интерцептор для вставки токена
jwtApi.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken'); // или из хранилища
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default jwtApi;