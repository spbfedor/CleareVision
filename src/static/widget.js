(function() {
    let userId = localStorage.getItem('clearvision_user_id');
    if (!userId) {
        userId = 'user_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('clearvision_user_id', userId);
    }

    const BACKEND_URL = 'http://localhost:8080/profile';

    let currentSettings = {
        user_id: userId,
        font_size: 1.0,
        visual_mode: "normal",
        letter_spacing: 0.0
    };

    const host = document.createElement('div');
    host.id = 'clearvision-root';
    document.body.appendChild(host);
    const shadow = host.attachShadow({mode: 'open'});

    shadow.innerHTML = `
        <style>
            .cv-panel { 
              position: fixed;
              bottom: 20px;
              right: 20px;
              background: #111;
              color: #fff;
              z-index: 999999;
              padding: 15px;
              border-radius: 8px;
              font-family: sans-serif;
              box-shadow: 0 4px 12px rgba(0,0,0,0.5);
              display: flex;
              flex-direction: column;
              gap: 10px;
              border: 2px solid #fff;
              min-width: 250px; 
            }
            .cv-title { font-weight: bold; text-align: center; color: #fff; margin-bottom: 5px; font-size: 16px; text-transform: uppercase; letter-spacing: 1px; }
            .cv-btn { 
              background: #fff;
              color: #000;
              border: none;
              padding: 10px 12px;
              cursor: pointer;
              font-weight: bold;
              font-size: 14px;
              border-radius: 4px;
              text-align: left;
              transition: background 0.2s;
              display: flex;
              justify-content: space-between; 
            }
            .cv-btn:hover { background: #e0e0e0; }
            .cv-btn:focus { outline: 3px solid #ff0000; }
        </style>
        <div class="cv-panel" role="toolbar" aria-label="Панель доступности ClearVision">
            <div class="cv-title">ClearVision</div>
            <button class="cv-btn" id="btn-font">Размер шрифта: <span>Стандартный</span></button>
            <button class="cv-btn" id="btn-spacing">Интервал букв: <span>Обычный</span></button>
            <button class="cv-btn" id="btn-mono">Цвет страницы: <span>Цветной</span></button>
        </div>
    `;

    function applyAccessibilitySettings(settings) {
        if (settings.font_size === 1.5) {
            document.documentElement.style.fontSize = '22px';
            shadow.querySelector('#btn-font span').innerText = 'Средний (x1.5)';
        } else if (settings.font_size === 2.0) {
            document.documentElement.style.fontSize = '28px';
            shadow.querySelector('#btn-font span').innerText = 'Большой (x2.0)';
        } else {
            document.documentElement.style.fontSize = '';
            shadow.querySelector('#btn-font span').innerText = 'Стандартный';
        }

        if (settings.letter_spacing === 2.0) {
            document.documentElement.style.letterSpacing = '2px';
            shadow.querySelector('#btn-spacing span').innerText = 'Средний (+2px)';
        } else if (settings.letter_spacing === 4.0) {
            document.documentElement.style.letterSpacing = '4px';
            shadow.querySelector('#btn-spacing span').innerText = 'Большой (+4px)';
        } else {
            document.documentElement.style.letterSpacing = '';
            shadow.querySelector('#btn-spacing span').innerText = 'Обычный';
        }

        if (settings.visual_mode === 'monochrome') {
            document.documentElement.style.filter = 'grayscale(100%)';
            shadow.querySelector('#btn-mono span').innerText = 'Черно-белый';
        } else {
            document.documentElement.style.filter = '';
            shadow.querySelector('#btn-mono span').innerText = 'Цветной';
        }
    }

    fetch(`${BACKEND_URL}/${userId}`)
        .then(res => { if (!res.ok) throw new Error(); return res.json(); })
        .then(data => {
            if (data.user_id) {
                currentSettings = data;
                applyAccessibilitySettings(currentSettings);
            }
        })
        .catch(() => console.log("ClearVision: Запущен новый сеанс пользователя"));

    function sendSettings(payload) {
        fetch(`${BACKEND_URL}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }).catch(err => console.error("ClearVision API Error:", err));
    }

    shadow.getElementById('btn-font').addEventListener('click', () => {
        if (currentSettings.font_size === 1.0) {
            currentSettings.font_size = 1.5;
        } else if (currentSettings.font_size === 1.5) {
            currentSettings.font_size = 2.0;
        } else {
            currentSettings.font_size = 1.0;
        }
        applyAccessibilitySettings(currentSettings);
        sendSettings(currentSettings);
    });

    shadow.getElementById('btn-spacing').addEventListener('click', () => {
        if (currentSettings.letter_spacing === 0.0) {
            currentSettings.letter_spacing = 2.0;
        } else if (currentSettings.letter_spacing === 2.0) {
            currentSettings.letter_spacing = 4.0;
        } else {
            currentSettings.letter_spacing = 0.0;
        }
        applyAccessibilitySettings(currentSettings);
        sendSettings(currentSettings);
    });

    shadow.getElementById('btn-mono').addEventListener('click', () => {
        if (currentSettings.visual_mode === 'normal') {
            currentSettings.visual_mode = 'monochrome';
        } else {
            currentSettings.visual_mode = 'normal';
        }
        applyAccessibilitySettings(currentSettings);
        sendSettings(currentSettings);
    });
})();
