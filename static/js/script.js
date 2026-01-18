// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `flash-message ${type}`;

    const icons = {
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'warning': '⚠️'
    };

    notification.innerHTML = `${icons[type] || '💡'} ${message}`;
    notification.style.animation = 'slideIn 0.3s ease';

    const container = document.querySelector('.flash-messages') || createNotificationContainer();
    container.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Функция для открытия страницы фильма
function openMovieDetail(movieId) {
    window.location.href = `/movie/${movieId}`;
}

// Функция для показа опций просмотра
function showWatchOptions(movieTitle, platforms) {
    if (platforms && platforms.length > 0) {
        const message = `"${movieTitle}" доступен на:\n\n${platforms.join('\n')}\n\n🎬 Функция перехода к просмотру скоро будет доступна!`;
        showNotification(`Доступен на: ${platforms.join(', ')}`, 'info');
    } else {
        showNotification('Этот контент временно недоступен для онлайн-просмотра', 'warning');
    }
}

// Автодополнение поиска
function initSearchAutocomplete() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    let timeoutId;
    let suggestionsContainer = null;

    searchInput.addEventListener('input', function() {
        clearTimeout(timeoutId);

        // Удаляем старые подсказки
        if (suggestionsContainer) {
            suggestionsContainer.remove();
            suggestionsContainer = null;
        }

        const query = this.value.trim();
        if (query.length >= 2) {
            timeoutId = setTimeout(() => fetchSuggestions(query), 300);
        }
    });

    // Скрываем подсказки при клике вне поля
    document.addEventListener('click', function(e) {
        if (suggestionsContainer && !searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.remove();
            suggestionsContainer = null;
        }
    });

    // Обработка клавиш в поле поиска
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && suggestionsContainer) {
            suggestionsContainer.remove();
            suggestionsContainer = null;
        }
    });
}

async function fetchSuggestions(query) {
    try {
        const response = await fetch(`/api/search_suggestions?q=${encodeURIComponent(query)}`);
        const suggestions = await response.json();
        showSuggestions(suggestions, query);
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}

function showSuggestions(suggestions, query) {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput || suggestions.length === 0) return;

    // Создаем контейнер для подсказок
    suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions';

    // Позиционируем подсказки под полем поиска
    const rect = searchInput.getBoundingClientRect();
    suggestionsContainer.style.position = 'absolute';
    suggestionsContainer.style.top = `${rect.bottom + window.scrollY}px`;
    suggestionsContainer.style.left = `${rect.left + window.scrollX}px`;
    suggestionsContainer.style.width = `${rect.width}px`;

    // Добавляем подсказки
    suggestions.forEach(suggestion => {
        const suggestionElement = document.createElement('div');
        suggestionElement.className = 'suggestion-item';
        suggestionElement.innerHTML = `
            <div class="suggestion-content">
                <div class="suggestion-header">
                    <div class="suggestion-title">${highlightMatch(suggestion.title, query)}</div>
                    <div class="suggestion-rating">⭐ ${suggestion.rating}</div>
                </div>
                <div class="suggestion-meta">${suggestion.year} • ${suggestion.type === 'movie' ? '🎞️ Фильм' : '📺 Сериал'}</div>
                <div class="suggestion-genre">${suggestion.genre.split(',')[0]}</div>
            </div>
            <div class="suggestion-actions">
                <button type="button" class="suggestion-btn" onclick="openMovieDetail(${suggestion.id})">
                    Подробнее
                </button>
            </div>
        `;

        suggestionElement.addEventListener('click', function(e) {
            if (!e.target.classList.contains('suggestion-btn')) {
                openMovieDetail(suggestion.id);
            }
        });

        suggestionsContainer.appendChild(suggestionElement);
    });

    document.body.appendChild(suggestionsContainer);
}

function highlightMatch(text, query) {
    const lowerText = text.toLowerCase();
    const lowerQuery = query.toLowerCase();
    const matchIndex = lowerText.indexOf(lowerQuery);

    if (matchIndex === -1) return text;

    const before = text.substring(0, matchIndex);
    const match = text.substring(matchIndex, matchIndex + query.length);
    const after = text.substring(matchIndex + query.length);

    return `${before}<mark class="search-highlight">${match}</mark>${after}`;
}

// Streaming Availability Check
async function checkStreamingAvailability(movieId, button) {
    const originalText = button.innerHTML;

    button.innerHTML = '🔄 Проверяем...';
    button.disabled = true;

    try {
        const response = await fetch(`/api/check_streaming/${movieId}`);
        const data = await response.json();

        if (response.ok) {
            showNotification(`✅ Доступность для "${data.title}" обновлена!`, 'success');
            updateMovieCard(movieId, data.streaming_platforms);
        } else {
            showNotification('❌ Ошибка при проверке доступности', 'error');
        }
    } catch (error) {
        console.error('Error checking streaming:', error);
        showNotification('❌ Ошибка при проверке доступности', 'error');
    } finally {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

function updateMovieCard(movieId, streamingData) {
    const movieCard = document.querySelector(`.movie-card[data-movie-id="${movieId}"]`);
    if (!movieCard) return;

    // Update badges
    const badgesContainer = movieCard.querySelector('.streaming-badges');
    if (badgesContainer) {
        badgesContainer.innerHTML = '';

        if (streamingData.netflix) {
            badgesContainer.innerHTML += '<span class="streaming-badge netflix">N</span>';
        }
        if (streamingData.amazon) {
            badgesContainer.innerHTML += '<span class="streaming-badge amazon">A</span>';
        }
        if (streamingData.disney) {
            badgesContainer.innerHTML += '<span class="streaming-badge disney">D</span>';
        }
        if (streamingData.hbo) {
            badgesContainer.innerHTML += '<span class="streaming-badge hbo">H</span>';
        }
    }

    // Update platform indicators
    const platformsList = movieCard.querySelector('.platforms-list');
    if (platformsList) {
        platformsList.innerHTML = '';

        if (streamingData.netflix) {
            platformsList.innerHTML += '<span class="platform-indicator netflix">Netflix</span>';
        }
        if (streamingData.amazon) {
            platformsList.innerHTML += '<span class="platform-indicator amazon">Amazon Prime</span>';
        }
        if (streamingData.disney) {
            platformsList.innerHTML += '<span class="platform-indicator disney">Disney+</span>';
        }
        if (streamingData.hbo) {
            platformsList.innerHTML += '<span class="platform-indicator hbo">HBO Max</span>';
        }

        if (!streamingData.netflix && !streamingData.amazon && !streamingData.disney && !streamingData.hbo) {
            platformsList.innerHTML = '<span class="platform-indicator none">Не доступен онлайн</span>';
        }
    }
}

// Управление фильтрами
function toggleFilters() {
    const panel = document.getElementById('filtersPanel');
    if (panel) {
        panel.classList.toggle('active');
    }
}

function removeFilter(filterName) {
    const url = new URL(window.location.href);
    url.searchParams.delete(filterName);
    window.location.href = url.toString();
}

// Умная система поиска
class SmartSearch {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.suggestionsContainer = document.getElementById('searchSuggestions');
        this.currentRequest = null;
        this.init();
    }

    init() {
        if (!this.searchInput) return;

        this.setupEventListeners();
        this.setupQuickSearch();
    }

    setupEventListeners() {
        // Ввод текста
        this.searchInput.addEventListener('input', this.handleInput.bind(this));

        // Фокус
        this.searchInput.addEventListener('focus', this.handleFocus.bind(this));

        // Клавиши
        this.searchInput.addEventListener('keydown', this.handleKeydown.bind(this));

        // Клик вне поля
        document.addEventListener('click', this.handleClickOutside.bind(this));
    }

    setupQuickSearch() {
        // Быстрый поиск при вводе (без отправки формы)
        this.searchInput.addEventListener('input', this.debounce(() => {
            this.performQuickSearch();
        }, 300));
    }

    handleInput(e) {
        const query = e.target.value.trim();

        // Отменяем предыдущий запрос
        if (this.currentRequest) {
            this.currentRequest.abort();
        }

        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }

        this.showLoading();
        this.fetchSuggestions(query);
    }

    handleFocus() {
        const query = this.searchInput.value.trim();
        if (query.length >= 2) {
            this.fetchSuggestions(query);
        }
    }

    handleKeydown(e) {
        switch(e.key) {
            case 'Escape':
                this.hideSuggestions();
                break;
            case 'ArrowDown':
                e.preventDefault();
                this.navigateSuggestions(1);
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.navigateSuggestions(-1);
                break;
            case 'Enter':
                if (this.hasVisibleSuggestions()) {
                    e.preventDefault();
                    this.selectHighlightedSuggestion();
                }
                break;
        }
    }

    handleClickOutside(e) {
        if (!this.searchInput.contains(e.target) && !this.suggestionsContainer.contains(e.target)) {
            this.hideSuggestions();
        }
    }

    async fetchSuggestions(query) {
        try {
            this.currentRequest = new AbortController();

            const response = await fetch(`/api/search_suggestions?q=${encodeURIComponent(query)}`, {
                signal: this.currentRequest.signal
            });

            const suggestions = await response.json();
            this.displaySuggestions(suggestions, query);
            this.currentRequest = null;

        } catch (error) {
            if (error.name !== 'AbortError') {
                console.error('Search error:', error);
                this.showError();
            }
        }
    }

    displaySuggestions(suggestions, query) {
        if (!suggestions.length) {
            this.showNoResults();
            return;
        }

        const html = suggestions.map(suggestion => this.createSuggestionHTML(suggestion, query)).join('');
        this.suggestionsContainer.innerHTML = html;
        this.suggestionsContainer.style.display = 'block';

        // Добавляем обработчики для элементов
        this.addSuggestionEventListeners();
    }

    createSuggestionHTML(suggestion, query) {
        const title = this.highlightMatch(suggestion.title, query);
        const typeIcon = suggestion.type === 'movie' ? '🎞️' : '📺';
        const meta = `${suggestion.year} • ${typeIcon} • ⭐ ${suggestion.rating}`;

        return `
            <div class="suggestion-item" data-title="${suggestion.title}" data-id="${suggestion.id}">
                <div class="suggestion-content">
                    <div class="suggestion-header">
                        <div class="suggestion-title">${title}</div>
                        <div class="suggestion-rating">⭐ ${suggestion.rating}</div>
                    </div>
                    <div class="suggestion-meta">${meta}</div>
                    <div class="suggestion-genre">${suggestion.genre.split(',')[0]}</div>
                </div>
                <div class="suggestion-actions">
                    <button type="button" class="suggestion-btn" onclick="openMovieDetail(${suggestion.id})">
                        Подробнее
                    </button>
                </div>
            </div>
        `;
    }

    highlightMatch(text, query) {
        const lowerText = text.toLowerCase();
        const lowerQuery = query.toLowerCase();
        const matchIndex = lowerText.indexOf(lowerQuery);

        if (matchIndex === -1) return text;

        const before = text.substring(0, matchIndex);
        const match = text.substring(matchIndex, matchIndex + query.length);
        const after = text.substring(matchIndex + query.length);

        return `${before}<mark class="search-highlight">${match}</mark>${after}`;
    }

    addSuggestionEventListeners() {
        const items = this.suggestionsContainer.querySelectorAll('.suggestion-item');

        items.forEach(item => {
            item.addEventListener('mouseenter', () => {
                this.removeHighlight();
                item.classList.add('highlighted');
            });

            item.addEventListener('click', (e) => {
                if (!e.target.classList.contains('suggestion-btn')) {
                    const movieId = item.dataset.id;
                    openMovieDetail(movieId);
                }
            });
        });
    }

    selectSuggestion(title) {
        this.searchInput.value = title;
        this.hideSuggestions();
        this.searchInput.focus();

        // Автоматический поиск
        setTimeout(() => {
            this.searchInput.form.submit();
        }, 200);
    }

    navigateSuggestions(direction) {
        const items = this.suggestionsContainer.querySelectorAll('.suggestion-item');
        if (!items.length) return;

        const currentIndex = Array.from(items).findIndex(item => item.classList.contains('highlighted'));
        let newIndex;

        if (currentIndex === -1) {
            newIndex = direction === 1 ? 0 : items.length - 1;
        } else {
            newIndex = currentIndex + direction;
            if (newIndex < 0) newIndex = items.length - 1;
            if (newIndex >= items.length) newIndex = 0;
        }

        this.removeHighlight();
        items[newIndex].classList.add('highlighted');
        items[newIndex].scrollIntoView({ block: 'nearest' });
    }

    selectHighlightedSuggestion() {
        const highlighted = this.suggestionsContainer.querySelector('.suggestion-item.highlighted');
        if (highlighted) {
            const movieId = highlighted.dataset.id;
            openMovieDetail(movieId);
        }
    }

    removeHighlight() {
        const highlighted = this.suggestionsContainer.querySelector('.suggestion-item.highlighted');
        if (highlighted) {
            highlighted.classList.remove('highlighted');
        }
    }

    showLoading() {
        this.suggestionsContainer.innerHTML = '<div class="suggestion-loading">🔍 Ищем лучшие варианты...</div>';
        this.suggestionsContainer.style.display = 'block';
    }

    showNoResults() {
        this.suggestionsContainer.innerHTML = `
            <div class="suggestion-no-results">
                <div>😔 Не найдено</div>
                <small>Попробуйте изменить запрос</small>
            </div>
        `;
        this.suggestionsContainer.style.display = 'block';
    }

    showError() {
        this.suggestionsContainer.innerHTML = '<div class="suggestion-error">⚠️ Ошибка поиска</div>';
        this.suggestionsContainer.style.display = 'block';
    }

    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
    }

    hasVisibleSuggestions() {
        return this.suggestionsContainer.style.display === 'block';
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async performQuickSearch() {
        // Для будущего использования - быстрый поиск без перезагрузки
        const query = this.searchInput.value.trim();
        if (query.length < 3) return;

        // Можно добавить AJAX поиск с предпросмотром
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎬 CineSearch initialized successfully!');

    // Инициализация автодополнения
    initSearchAutocomplete();

    // Инициализация умного поиска
    window.smartSearch = new SmartSearch();

    // Добавляем обработчики кликов на карточки фильмов
    const movieCards = document.querySelectorAll('.movie-card');

    movieCards.forEach(card => {
        card.style.cursor = 'pointer';

        // Обработка клика на всю карточку
        card.addEventListener('click', function(e) {
            // Если клик не на кнопке внутри карточки
            if (!e.target.closest('.quick-view-btn') &&
                !e.target.closest('.suggestion-btn') &&
                !e.target.closest('.card-actions')) {
                const movieId = this.dataset.movieId;
                if (movieId) {
                    openMovieDetail(movieId);
                }
            }
        });
    });

    // Автоматическое скрытие flash сообщений
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Добавляем анимации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        @keyframes fadeOut {
            from { opacity: 1; transform: translateX(0); }
            to { opacity: 0; transform: translateX(100%); }
        }
    `;
    document.head.appendChild(style);
});

// Make functions globally available
window.checkStreamingAvailability = checkStreamingAvailability;
window.showNotification = showNotification;
window.toggleFilters = toggleFilters;
window.removeFilter = removeFilter;
window.openMovieDetail = openMovieDetail;
window.showWatchOptions = showWatchOptions;