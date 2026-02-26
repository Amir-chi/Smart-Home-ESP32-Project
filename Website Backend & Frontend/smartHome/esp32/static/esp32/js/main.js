
        // ============================================
        // STATE MANAGEMENT
        // ============================================
        const state = {
            theme: 'dark',
            lamps: {
                1: false,
                2: false,
                3: false
            },
            espLed: false,
            flash: false,
            cameraSettings: {
                brightness: 0,
                contrast: 0,
                resolution: 'SVGA'
            },
            commandHistory: [],
            isRecording: false,
            currentAudioBlob: null,
        };

        // ============================================
        // INITIALIZATION
        // ============================================
        document.addEventListener('DOMContentLoaded', () => {
            initTheme();
            startClock();
            loadCommandHistory();
            checkLedStatus();
            addToHistory();

            // Enter key listener
            document.getElementById('commandInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    // sendCommand();
                    sendCommandToServer();
                }
            });

            // Image preview close button
            document.getElementById('closePreview').addEventListener('click', () => {
                document.getElementById('imagePreview').classList.remove('active');
            });
        });

        // ============================================
        // THEME MANAGEMENT
        // ============================================
        function initTheme() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            state.theme = savedTheme;
            document.documentElement.setAttribute('data-theme', savedTheme);
            updateThemeIcon();
        }

        function toggleTheme() {
            state.theme = state.theme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', state.theme);
            localStorage.setItem('theme', state.theme);
            updateThemeIcon();
            showToast(
                `Switched to ${state.theme === 'dark' ? 'Dark' : 'Light'} Mode`,
                'success'
            );
        }

        function updateThemeIcon() {
            const icon = document.querySelector('#themeToggle i');
            icon.className = state.theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }

        document.getElementById('themeToggle').addEventListener('click', toggleTheme);

        // ============================================
        // CLOCK
        // ============================================
        function startClock() {
            updateClock();
            setInterval(updateClock, 1000);
        }

        function updateClock() {
            const now = new Date();
            const options = {
                weekday: 'short',
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            };
            document.getElementById('clock').textContent = now.toLocaleString('en-US', options);
        }

        // ============================================
        // LAMP CONTROL
        // ============================================
        function toggleLamp(lampNumber) {
            state.lamps[lampNumber] = !state.lamps[lampNumber];
            const lampCard = document.getElementById(`lamp${lampNumber}`);
            const status = lampCard.querySelector('.lamp-status');

            if (state.lamps[lampNumber]) {
                lampCard.classList.add('on');
                status.textContent = 'ON';
                showToast(`Lamp ${lampNumber} turned ON`, 'success');
                fetch('/api/receive_message/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN 
                    },
                    body: JSON.stringify({
                        'type' : 'command',
                        'action': `flash${lampNumber}_on`
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP Error: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Server response:', data);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showToast('Error sending command to ESP32', 'error');
                    });
            } else {
                lampCard.classList.remove('on');
                status.textContent = 'OFF';
                showToast(`Lamp ${lampNumber} turned OFF`, 'success');
                fetch('/api/receive_message/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN 
                    },
                    body: JSON.stringify({
                        'type' : 'command',
                        'action': `flash${lampNumber}_off`
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP Error: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Server response:', data);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showToast('Error sending command to ESP32', 'error');
                    });
            }
        }

        function toggleEspLed() {
            state.espLed = !state.espLed;

            const espCard = document.getElementById('espLed');
            const status = espCard.querySelector('.lamp-status');

            const action = state.espLed ? 'flash_on' : 'flash_off';

            // UI
            if (state.espLed) {
                espCard.classList.add('on');
                status.textContent = 'ON';
                showToast('ESP32 LED turned ON', 'success');
            } else {
                espCard.classList.remove('on');
                status.textContent = 'OFF';
                showToast('ESP32 LED turned OFF', 'success');
            }


            fetch('/api/receive_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN 
                },
                body: JSON.stringify({
                    'type' : 'command',
                    'action': action
                })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP Error: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Server response:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    showToast('Error sending command to ESP32', 'error');
                });
            // state.espLed = !state.espLed;
            // const espCard = document.getElementById('espLed');
            // const status = espCard.querySelector('.lamp-status');

            // if (state.espLed) {
            //     espCard.classList.add('on');
            //     status.textContent = 'ON';
            //     showToast('ESP32 LED turned ON', 'success');
            // } else {
            //     espCard.classList.remove('on');
            //     status.textContent = 'OFF';
            //     showToast('ESP32 LED turned OFF', 'success');
            // }
        }

        // ============================================
        // CAMERA SETTINGS
        // ============================================
        function updateSetting(setting, value) {
            state.cameraSettings[setting] = parseInt(value);
            document.getElementById(`${setting}Value`).textContent = value;
            showToast(`${setting.charAt(0).toUpperCase() + setting.slice(1)} set to ${value}`, 'success');
        }

        function updateResolution(value) {
            state.cameraSettings.resolution = value;
            showToast(`Resolution changed to ${value}`, 'success');
        }

        // ============================================
        // FLASH CONTROL
        // ============================================
        function toggleFlash() {
            state.flash = !state.flash;
            const flashBtn = document.getElementById('flashToggle');

            if (state.flash) {
                flashBtn.classList.add('active');
                flashBtn.innerHTML = '<i class="fas fa-bolt"></i><span>Flash: ON</span>';
                showToast('Flash enabled', 'success');
            } else {
                flashBtn.classList.remove('active');
                flashBtn.innerHTML = '<i class="fas fa-bolt"></i><span>Flash: OFF</span>';
                showToast('Flash disabled', 'success');
            }
        }

        // ============================================
        // CAMERA CAPTURE
        // ============================================
        async function capturePhoto() {
            const captureBtn = document.getElementById('captureBtn');
            const preview = document.getElementById('cameraPreview');
            const caption = document.getElementById('imageCaption');

            captureBtn.disabled = true;
            captureBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Capturing...</span>';

            try {
                const response = await fetch('get_picture'); 
                const data = await response.json();

                if (data.status === 'success') {
                    const timestamp = new Date().toLocaleString();
                    
                    preview.innerHTML = `<img src="${data.image_url}?t=${Date.now()}" alt="Captured Photo">`;
                    
                    document.getElementById('captureTime').textContent = timestamp;
                    caption.style.display = 'block';
                    showToast('Photo received from ESP32!', 'success');
                } else {
                    showToast('Camera is offline or error occurred', 'error');
                }
            } catch (error) {
                console.error('Error fetching photo:', error);
                showToast('Server error', 'error');
            } finally {
                captureBtn.disabled = false;
                captureBtn.innerHTML = '<i class="fas fa-camera"></i><span>Capture Photo</span>';
            }
        }

        // ============================================
        // VOICE COMMAND
        // ============================================
        let mediaRecorder;
        let audioChunks = [];

        document.getElementById('voiceBtn').addEventListener('click', async () => {
            const voiceBtn = document.getElementById('voiceBtn');

            if (!state.isRecording) {
                try {
                    // 1. درخواست دسترسی به میکروفون
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    
                    // 2. تنظیمات MediaRecorder
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];

                    mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            audioChunks.push(event.data);
                        }
                    };

                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

                        state.currentAudioBlob = audioBlob;

                        showToast('در حال ارسال فایل صوتی...', 'success');
                        await sendCommandToServer(); 
                        
                        stream.getTracks().forEach(track => track.stop());
                    };

                    mediaRecorder.start();
                    state.isRecording = true;
                    voiceBtn.classList.add('recording');
                    voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
                    showToast('در حال ضبط صدا...', 'success');

                } catch (err) {
                    console.error("خطا در دسترسی به میکروفون:", err);
                    showToast('دسترسی به میکروفون امکان‌پذیر نیست', 'error');
                }
            } else {
                mediaRecorder.stop();
                resetVoiceButton();
            }
        });
        function resetVoiceButton() {
            state.isRecording = false;
            document.getElementById('voiceBtn').classList.remove('recording');
            document.getElementById('voiceBtn').innerHTML = '<i class="fas fa-microphone"></i>';
        }

        // ============================================
        // IMAGE UPLOAD
        // ============================================
        document.getElementById('imageBtn').addEventListener('click', () => {
            document.getElementById('imageInput').click();
        });

        document.getElementById('imageInput').addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    document.getElementById('previewImg').src = e.target.result;
                    document.getElementById('imagePreview').classList.add('active');
                    showToast('Image uploaded successfully!', 'success');
                };
                reader.readAsDataURL(file);
            }
        });

        function fillCommand(command) {
            document.getElementById('commandInput').value = command;
        }

        function showStatus() {
            const status = `
                🔆 Lamps: ${state.lamps[1] ? '1-ON' : '1-OFF'} | ${state.lamps[2] ? '2-ON' : '2-OFF'} | ${state.lamps[3] ? '3-ON' : '3-OFF'}
                🔌 ESP32 LED: ${state.espLed ? 'ON' : 'OFF'}
                ⚡ Flash: ${state.flash ? 'ON' : 'OFF'}
                📷 Resolution: ${state.cameraSettings.resolution}
            `;
            showToast(status, 'success');
        }

        document.getElementById('sendBtn').addEventListener('click', sendCommandToServer);

        // ============================================
        // COMMAND HISTORY
        // ============================================
        async function addToHistory() { // اضافه کردن async
            const url = '/api/get_history/';

            try {
                const response = await fetch(url, { // اضافه کردن await
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                // ۱. دریافت داده‌ها از سرور (حتما با await)
                const serverHistory = await response.json(); 
                
                console.log("History from server:", serverHistory);

                // ۲. به‌روزرسانی وضعیت (State)
                state.commandHistory = serverHistory;

                // ۳. رندر کردن و ذخیره
                saveCommandHistory();
                renderHistory();

            } catch (error) {
                console.error('Could not fetch history:', error);
                showToast('خطا در دریافت تاریخچه', 'error');
            }
        }

        function saveCommandHistory() {
            localStorage.setItem('commandHistory', JSON.stringify(state.commandHistory));
        }

        function loadCommandHistory() {
            const saved = localStorage.getItem('commandHistory');
            if (saved) {
                state.commandHistory = JSON.parse(saved);
                renderHistory();
            }
        }

        function renderHistory() {
            const historyList = document.getElementById('historyList');

            if (state.commandHistory.length === 0) {
                historyList.innerHTML = `
                    <div class="history-empty">
                        <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                        <p>No commands yet</p>
                    </div>
                `;
                return;
            }

            historyList.innerHTML = state.commandHistory.map(item => `
                <div class="history-item" onclick="fillCommand('${item.command.replace(/'/g, "\\'")}')">
                    <div class="history-item-command">
                        <i class="fas fa-terminal"></i> ${item.command}
                    </div>
                    <div class="history-item-meta">
                        <span><i class="far fa-clock"></i> ${item.timestamp}</span>
                    </div>
                </div>
            `).join('');
        }

        function clearHistory() {
            if (confirm('Are you sure you want to clear all command history?')) {
                state.commandHistory = [];
                saveCommandHistory();
                renderHistory();
                showToast('Command history cleared', 'success');
            }
        }

        // ============================================
        // TOAST NOTIFICATIONS
        // ============================================
        function showToast(message, type = 'success') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;

            const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';

            toast.innerHTML = `
                <i class="fas ${icon} toast-icon"></i>
                <span>${message}</span>
            `;

            container.appendChild(toast);

            setTimeout(() => {
                toast.style.animation = 'slideIn 0.3s ease reverse';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }


        async function checkLedStatus() {
            try {
                const response = await fetch("/get_led_status/");
                
                if (!response.ok) {
                    throw new Error("connection error");
                }

                const data = await response.json();

                if (data.led0 === "on" && !state.espLed) {
                    toggleEspLed()
                }
                if (data.led0 === "off" && state.espLed) {
                    toggleEspLed()
                }

                if (data.led1 === "on" && !state.lamps[1]) {
                    toggleLamp(1);
                }
                
                if (data.led1 === "off" && state.lamps[1]) {
                    toggleLamp(1);
                }

                if (data.led2 === "on" && !state.lamps[2]) {
                    toggleLamp(2);
                }
                
                if (data.led2 === "off" && state.lamps[2]) {
                    toggleLamp(2);
                }

                if (data.led3 === "on" && !state.lamps[3]) {
                    toggleLamp(3);
                }
                
                if (data.led3 === "off" && state.lamps[3]) {
                    toggleLamp(3);
                }
                

            } catch (error) {
                
            }
        }


        async function sendCommandToServer() {
            const commandInput = document.getElementById('commandInput').value;
            const imageInput = document.getElementById('imageInput').files[0];

            if (!commandInput && !imageInput && !state.currentAudioBlob) {
                showToast('Please enter a command or image or voice', 'error');
                return;
            }


            const formData = new FormData();
            formData.append('command', commandInput);
            
            if (imageInput) {
                formData.append('image', imageInput);
            }
            
            if (state.currentAudioBlob) {
                formData.append('audio', state.currentAudioBlob, 'voice_command.wav');
                
                state.currentAudioBlob = null; 
            }
            
            formData.append('csrfmiddlewaretoken', CSRF_TOKEN); 
            
            try {
                
                const response = await fetch('', {
                    method: 'POST',
                    body: formData, 
                });
                showToast("Command sent successfully!", "success");
                document.getElementById('commandInput').value = '';
                document.getElementById('imagePreview').classList.remove('active');
                document.getElementById('previewImg').src = '';
                document.getElementById('imageInput').value = "";
                checkLedStatus();
                addToHistory();
                
            } catch (error) {
                showToast("Error sending data", "error");
            }
        }