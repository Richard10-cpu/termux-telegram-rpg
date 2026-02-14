// Telegram Web App инициализация
// Проверяем, запущено ли приложение в Telegram
const tg = window.Telegram?.WebApp || {
    // Заглушка для тестирования в браузере
    expand: () => console.log('🔧 Dev mode: expand()'),
    ready: () => console.log('🔧 Dev mode: ready()'),
    themeParams: {
        bg_color: '#ffffff',
        text_color: '#000000',
        button_color: '#3390ec',
        button_text_color: '#ffffff',
        secondary_bg_color: '#f4f4f5'
    },
    initData: '',
    showAlert: (msg) => alert(msg)
};

if (window.Telegram?.WebApp) {
    tg.expand();
    tg.ready();
    console.log('✅ Запущено в Telegram');
} else {
    console.log('🌐 Запущено в браузере (dev mode)');
}

// Главный объект приложения
const app = {
    // Состояние
    player: null,
    currentView: 'profile',
    currentEnemy: null,
    battleInterval: null,

    // API базовый URL
    apiUrl: window.location.origin + '/api',

    // Инициализация
    async init() {
        console.log('🎮 Инициализация Termux RPG Mini App...');

        // Применить тему Telegram
        this.applyTheme();

        // Получить данные игрока
        await this.loadPlayerData();

        // Настроить навигацию
        this.setupNavigation();

        // Загрузить контент
        await this.loadLocations();
        await this.loadEnemies();

        console.log('✅ Приложение готово!');
    },

    // Применить тему Telegram
    applyTheme() {
        const root = document.documentElement;
        root.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
        root.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
        root.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#3390ec');
        root.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
        root.style.setProperty('--tg-theme-secondary-bg-color', tg.themeParams.secondary_bg_color || '#f4f4f5');
    },

    // Загрузить данные игрока
    async loadPlayerData() {
        try {
            const initData = tg.initData || '';
            const response = await fetch(`${this.apiUrl}/player`, {
                headers: {
                    'Authorization': initData
                }
            });

            if (!response.ok) throw new Error('Ошибка загрузки данных игрока');

            this.player = await response.json();
            this.updatePlayerUI();
        } catch (error) {
            console.error('Ошибка:', error);
            // Заглушка для разработки
            this.player = {
                id: 1,
                name: 'Герой',
                level: 1,
                hp: 100,
                max_hp: 100,
                mana: 50,
                max_mana: 50,
                power: 10,
                gold: 100,
                exp: 0,
                exp_to_next_level: 100,
                location: 'village',
                inventory: []
            };
            this.updatePlayerUI();
        }
    },

    // Обновить UI игрока
    updatePlayerUI() {
        if (!this.player) return;

        document.getElementById('player-name').textContent = this.player.name;
        document.getElementById('player-level').textContent = this.player.level;

        document.getElementById('player-hp').textContent = this.player.hp;
        document.getElementById('player-max-hp').textContent = this.player.max_hp;
        const hpPercent = (this.player.hp / this.player.max_hp) * 100;
        document.getElementById('hp-bar').style.width = hpPercent + '%';

        document.getElementById('player-mana').textContent = this.player.mana;
        document.getElementById('player-max-mana').textContent = this.player.max_mana;
        const manaPercent = (this.player.mana / this.player.max_mana) * 100;
        document.getElementById('mana-bar').style.width = manaPercent + '%';

        document.getElementById('player-power').textContent = this.player.power;
        document.getElementById('player-gold').textContent = this.player.gold;
        document.getElementById('shop-gold').textContent = this.player.gold;

        document.getElementById('player-exp').textContent = this.player.exp;
        document.getElementById('player-next-level').textContent = this.player.exp_to_next_level;
        const expPercent = (this.player.exp / this.player.exp_to_next_level) * 100;
        document.getElementById('exp-bar').style.width = expPercent + '%';

        // Локация
        const locationNames = {
            'village': '🏘️ Деревня',
            'forest': '🌲 Тёмный лес',
            'cave': '🕳️ Пещера',
            'mountain': '⛰️ Гора',
            'abyss': '🌊 Морская бездна',
            'ruins': '🏛️ Руины империи',
            'hell': '🔥 Преисподняя',
            'void': '⚡ Пустота'
        };
        document.getElementById('player-location').textContent = locationNames[this.player.location] || this.player.location;
    },

    // Настроить навигацию
    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        navButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.dataset.view;
                this.switchView(view);
            });
        });
    },

    // Переключить вид
    switchView(viewName) {
        // Скрыть все виды
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
        });

        // Показать выбранный
        document.getElementById(viewName + '-view').classList.add('active');

        // Обновить навигацию
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-view="${viewName}"]`).classList.add('active');

        this.currentView = viewName;
    },

    // Загрузить локации
    async loadLocations() {
        const locations = [
            { key: 'village', name: 'Деревня', emoji: '🏘️', level: 0 },
            { key: 'forest', name: 'Тёмный лес', emoji: '🌲', level: 1 },
            { key: 'cave', name: 'Пещера', emoji: '🕳️', level: 5 },
            { key: 'mountain', name: 'Гора', emoji: '⛰️', level: 10 },
            { key: 'abyss', name: 'Морская бездна', emoji: '🌊', level: 20 },
            { key: 'ruins', name: 'Руины империи', emoji: '🏛️', level: 25 },
            { key: 'hell', name: 'Преисподняя', emoji: '🔥', level: 30 },
            { key: 'void', name: 'Пустота', emoji: '⚡', level: 35 }
        ];

        const grid = document.getElementById('locations-grid');
        grid.innerHTML = '';

        locations.forEach(loc => {
            const card = document.createElement('div');
            card.className = 'location-card';
            if (this.player && this.player.location === loc.key) {
                card.classList.add('current');
            }
            card.innerHTML = `
                <div class="location-emoji">${loc.emoji}</div>
                <div class="location-name">${loc.name}</div>
                <div class="location-level">Уровень: ${loc.level}+</div>
            `;
            card.onclick = () => this.travelToLocation(loc.key);
            grid.appendChild(card);
        });
    },

    // Путешествовать в локацию
    async travelToLocation(locationKey) {
        try {
            const response = await fetch(`${this.apiUrl}/travel`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': tg.initData || ''
                },
                body: JSON.stringify({ location: locationKey })
            });

            if (!response.ok) throw new Error('Ошибка перемещения');

            this.player.location = locationKey;
            await this.loadLocations();
            await this.loadEnemies();
            this.updatePlayerUI();

            tg.showAlert('Вы переместились в новую локацию!');
        } catch (error) {
            console.error('Ошибка:', error);
            // Локальное обновление для разработки
            this.player.location = locationKey;
            await this.loadLocations();
            await this.loadEnemies();
            this.updatePlayerUI();
        }
    },

    // Загрузить врагов
    async loadEnemies() {
        const enemiesByLocation = {
            'village': [],
            'forest': [
                { key: 'goblin', name: 'Гоблин', emoji: '👺', hp: 30, power: 5, gold: 10, exp: 20 },
                { key: 'wolf', name: 'Волк', emoji: '🐺', hp: 40, power: 7, gold: 15, exp: 25 }
            ],
            'cave': [
                { key: 'skeleton', name: 'Скелет', emoji: '💀', hp: 60, power: 10, gold: 25, exp: 40 },
                { key: 'orc', name: 'Орк', emoji: '👹', hp: 80, power: 12, gold: 35, exp: 50 }
            ],
            'mountain': [
                { key: 'orc', name: 'Орк', emoji: '👹', hp: 80, power: 12, gold: 35, exp: 50 },
                { key: 'dragon', name: 'Дракон', emoji: '🐉', hp: 150, power: 20, gold: 100, exp: 150 }
            ],
            'abyss': [
                { key: 'sea_serpent', name: 'Морской змей', emoji: '🐍', hp: 250, power: 30, gold: 150, exp: 200 },
                { key: 'kraken', name: 'Кракен', emoji: '🦑', hp: 300, power: 35, gold: 200, exp: 250 }
            ],
            'ruins': [
                { key: 'golem', name: 'Голем', emoji: '🗿', hp: 400, power: 40, gold: 300, exp: 350 },
                { key: 'lich', name: 'Лич', emoji: '💀', hp: 350, power: 45, gold: 350, exp: 400 }
            ],
            'hell': [
                { key: 'demon', name: 'Демон', emoji: '😈', hp: 600, power: 55, gold: 500, exp: 600 },
                { key: 'hellhound', name: 'Адский гончий', emoji: '🐕', hp: 550, power: 50, gold: 450, exp: 550 }
            ],
            'void': [
                { key: 'void_entity', name: 'Сущность Пустоты', emoji: '👻', hp: 800, power: 70, gold: 750, exp: 850 },
                { key: 'chaos_spawn', name: 'Порождение Хаоса', emoji: '💥', hp: 1000, power: 80, gold: 1000, exp: 1000 }
            ]
        };

        const enemies = enemiesByLocation[this.player.location] || [];
        const list = document.getElementById('enemies-list');
        list.innerHTML = '';

        if (enemies.length === 0) {
            list.innerHTML = '<p class="text-center">В этой локации нет врагов. Можно отдохнуть!</p>';
            return;
        }

        enemies.forEach(enemy => {
            const card = document.createElement('div');
            card.className = 'enemy-card';
            card.innerHTML = `
                <div class="enemy-avatar">${enemy.emoji}</div>
                <div class="enemy-info">
                    <h3>${enemy.name}</h3>
                    <div class="enemy-stats">
                        HP: ${enemy.hp} | Сила: ${enemy.power}<br>
                        Награда: ${enemy.gold}💰 ${enemy.exp}📊
                    </div>
                </div>
            `;
            card.onclick = () => this.startBattle(enemy);
            list.appendChild(card);
        });
    },

    // Начать бой
    startBattle(enemy) {
        this.currentEnemy = { ...enemy, current_hp: enemy.hp };

        document.querySelector('.battle-select').style.display = 'none';
        document.getElementById('battle-arena').style.display = 'block';

        document.getElementById('enemy-name').textContent = enemy.name;
        document.querySelector('.combatant.enemy .combatant-avatar').textContent = enemy.emoji;
        document.getElementById('enemy-hp').textContent = enemy.hp;
        document.getElementById('enemy-max-hp').textContent = enemy.hp;
        document.getElementById('enemy-hp-bar').style.width = '100%';

        document.getElementById('battle-player-hp').textContent = this.player.hp;
        document.getElementById('battle-player-max-hp').textContent = this.player.max_hp;
        const playerHpPercent = (this.player.hp / this.player.max_hp) * 100;
        document.getElementById('battle-player-hp-bar').style.width = playerHpPercent + '%';

        this.addBattleLog(`⚔️ Битва с ${enemy.name} начинается!`);
    },

    // Атака
    async attack() {
        if (!this.currentEnemy) return;

        // Атака игрока
        const playerDamage = Math.floor(Math.random() * 10) + this.player.power;
        this.currentEnemy.current_hp -= playerDamage;
        this.addBattleLog(`⚔️ Вы нанесли ${playerDamage} урона!`);

        this.updateEnemyHP();

        if (this.currentEnemy.current_hp <= 0) {
            this.winBattle();
            return;
        }

        // Атака врага
        setTimeout(() => {
            const enemyDamage = Math.floor(Math.random() * 5) + this.currentEnemy.power;
            this.player.hp -= enemyDamage;
            this.addBattleLog(`💥 ${this.currentEnemy.name} нанёс вам ${enemyDamage} урона!`);

            this.updatePlayerHP();

            if (this.player.hp <= 0) {
                this.loseBattle();
            }
        }, 500);
    },

    // Обновить HP врага
    updateEnemyHP() {
        const hp = Math.max(0, this.currentEnemy.current_hp);
        document.getElementById('enemy-hp').textContent = hp;
        const percent = (hp / this.currentEnemy.hp) * 100;
        document.getElementById('enemy-hp-bar').style.width = percent + '%';
    },

    // Обновить HP игрока в бою
    updatePlayerHP() {
        const hp = Math.max(0, this.player.hp);
        document.getElementById('battle-player-hp').textContent = hp;
        document.getElementById('player-hp').textContent = hp;
        const percent = (hp / this.player.max_hp) * 100;
        document.getElementById('battle-player-hp-bar').style.width = percent + '%';
        document.getElementById('hp-bar').style.width = percent + '%';
    },

    // Добавить лог боя
    addBattleLog(message) {
        const log = document.getElementById('battle-log');
        const entry = document.createElement('div');
        entry.className = 'battle-log-entry';
        entry.textContent = message;
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
    },

    // Победа
    async winBattle() {
        this.addBattleLog(`🎉 Победа! Вы получили ${this.currentEnemy.gold}💰 и ${this.currentEnemy.exp}📊`);

        this.player.gold += this.currentEnemy.gold;
        this.player.exp += this.currentEnemy.exp;

        // Проверка на уровень
        if (this.player.exp >= this.player.exp_to_next_level) {
            this.player.level++;
            this.player.exp = 0;
            this.player.max_hp += 20;
            this.player.hp = this.player.max_hp;
            this.player.max_mana += 10;
            this.player.mana = this.player.max_mana;
            this.player.power += 5;
            this.addBattleLog(`✨ ПОВЫШЕНИЕ УРОВНЯ! Теперь вы ${this.player.level} уровня!`);
        }

        this.updatePlayerUI();

        setTimeout(() => {
            this.endBattle();
            tg.showAlert('Победа! 🎉');
        }, 2000);
    },

    // Поражение
    loseBattle() {
        this.addBattleLog('💀 Вы проиграли...');
        this.player.hp = Math.floor(this.player.max_hp / 2);
        this.player.gold = Math.floor(this.player.gold * 0.9);

        setTimeout(() => {
            this.endBattle();
            tg.showAlert('Поражение... Вы потеряли 10% золота.');
        }, 2000);
    },

    // Закончить бой
    endBattle() {
        document.querySelector('.battle-select').style.display = 'block';
        document.getElementById('battle-arena').style.display = 'none';
        document.getElementById('battle-log').innerHTML = '';
        this.currentEnemy = null;
        this.updatePlayerUI();
    },

    // Побег
    flee() {
        const chance = Math.random();
        if (chance > 0.5) {
            this.addBattleLog('🏃 Вы успешно сбежали!');
            setTimeout(() => this.endBattle(), 1000);
        } else {
            this.addBattleLog('❌ Побег не удался!');
            // Враг атакует
            setTimeout(() => {
                const enemyDamage = Math.floor(Math.random() * 5) + this.currentEnemy.power;
                this.player.hp -= enemyDamage;
                this.addBattleLog(`💥 ${this.currentEnemy.name} нанёс вам ${enemyDamage} урона!`);
                this.updatePlayerHP();
                if (this.player.hp <= 0) {
                    this.loseBattle();
                }
            }, 500);
        }
    },

    // Заклинания
    showSpells() {
        tg.showAlert('Система магии будет доступна в следующем обновлении!');
    },

    // Использовать предмет в бою
    useItemInBattle() {
        tg.showAlert('Использование предметов будет доступно в следующем обновлении!');
    },

    // Отдых
    async rest() {
        if (this.player.location !== 'village') {
            tg.showAlert('Отдыхать можно только в деревне!');
            return;
        }

        const cost = 20;
        if (this.player.gold < cost) {
            tg.showAlert(`Недостаточно золота! Нужно ${cost}💰`);
            return;
        }

        this.player.gold -= cost;
        this.player.hp = this.player.max_hp;
        this.player.mana = this.player.max_mana;
        this.updatePlayerUI();

        tg.showAlert('Вы отдохнули и восстановили HP и ману!');
    },

    // Достижения
    showAchievements() {
        this.showModal('🏆 Достижения', 'Система достижений будет доступна в следующем обновлении!');
    },

    // Питомцы
    showPets() {
        this.showModal('🐾 Питомцы', 'Система питомцев будет доступна в следующем обновлении!');
    },

    // Показать модальное окно
    showModal(title, content) {
        const modal = document.getElementById('modal');
        const body = document.getElementById('modal-body');
        body.innerHTML = `<h2>${title}</h2><p>${content}</p>`;
        modal.classList.add('active');
    },

    // Закрыть модальное окно
    closeModal() {
        document.getElementById('modal').classList.remove('active');
    },

    // Вкладки инвентаря
    showInventoryTab(tab) {
        // TODO: Фильтрация инвентаря
        console.log('Вкладка инвентаря:', tab);
    },

    // Вкладки магазина
    showShopTab(tab) {
        // TODO: Фильтрация магазина
        console.log('Вкладка магазина:', tab);
    }
};

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        app.closeModal();
    }
};
