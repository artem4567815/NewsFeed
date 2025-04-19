# 📚 EduFeed — Школьные новости, как они есть

**EduFeed** — это новостная платформа для школ и других образовательных учреждений.  
Сервис позволяет ученикам, учителям и организаторам публиковать и просматривать свежие объявления, события и важные новости, связанные с жизнью школы.

Проект ориентирован на простоту, чистый интерфейс и удобный фильтр по категориям.

![Главная страница](./screenshots/main.png)

---

## 🚀 Основной функционал

- 📰 **Лента новостей** — отображает все актуальные события и публикации.
- 🗂️ **Фильтрация по параметрам**
- ⏳ **Таймлайн** — визуальное представление истории новостей.
- 🧾 **Создание публикаций** — добавляйте текст, изображения и теги.
- 🙋‍♂️ **Личный профиль** — редактируйте свои данные и следите за своими публикациями.
- ❤️ **Лайки и взаимодействие** — оценивайте посты и участвуйте в школьной жизни.
- 🔒 **Авторизация и безопасность** — защита данных с помощью JWT-токенов.
- 📷 **Загрузка изображений** — оформление постов красивыми обложками.
- 🛡️ **Модерация** — только проверенные пользователи могут публиковать контент.

---

## 🛠️ Стек технологий

### Frontend:

- **Vue 3 + Composition API** — быстрый, реактивный интерфейс.
- **Tailwind CSS** — адаптивная и кастомизируемая стилизация.
- **Vite** — сверхбыстрая сборка и HMR.

### Backend:

- **Python + Flask** — лёгкий и мощный REST API.
- **PostgreSQL** — надёжная СУБД для хранения пользователей и постов.
- **Tavern** — API-тестирование (покрытие основных endpoint'ов).
- **Docker** — изолированная среда, быстрое развертывание.

---

## ⚙️ Локальный запуск

1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/yourusername/edufeed.git
   cd edufeed
   ```

2. **Создать `.env` файл** (пример доступен в `.env.example`)

3. **Собрать и запустить через Docker**
   ```bash
   docker-compose up --build
   ```

4. **Frontend доступен по адресу:** `http://localhost:5173`  
   **Backend (API):** `http://localhost:8081`

---

## 🧑‍💻 Команда

| Участник | Роль           |
|----------|----------------|
| Krcha    | Frontend-разработка |
| arttuy   | Backend и DevOps   |

---

## 📷 Галерея

| 📥 Лента | ✍️ Создание | 🙎‍♂️ Профиль |
|----------|-------------|-------------|
| ![](./screenshots/feed.png) | ![](./screenshots/create.png) | ![](./screenshots/profile.png) |

---

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. [LICENSE](./LICENSE).

---

## 📌 Статус проекта

> ✅ Почти завершено!  
Добавляем финальные правки, тестируем функциональность и готовим проект к деплою 🚀