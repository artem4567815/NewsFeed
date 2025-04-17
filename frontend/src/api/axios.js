// src/api/axios.js
import axios from 'axios'
import { useRouter } from 'vue-router'


const api = axios.create({
    baseURL: import.meta.env.VITE_BASE_URL,
    withCredentials: true, // ⚠️ обязательно для отправки cookie
})

// Вставляем access токен из localStorage
api.interceptors.request.use(config => {
    const token = localStorage.getItem('authToken')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// Перехватываем 401 и отправляем refresh-запрос
api.interceptors.response.use(
    res => res,
    async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            try {
                // ⚠️ НИЧЕГО НЕ ПЕРЕДАЁМ — куки пойдут сами
                const res = await axios.post(
                    `${import.meta.env.VITE_BASE_URL}/auth/refresh`,
                    {},
                    {withCredentials: true
                    }
                )

                const newToken = res.data.access_token
                localStorage.setItem('authToken', newToken)

                originalRequest.headers.Authorization = `Bearer ${newToken}`
                return api(originalRequest)
            } catch (refreshError) {

                window.location.href = '/auth'
                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    }
)

export default api
