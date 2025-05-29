// main.js
document.addEventListener('DOMContentLoaded', () => {
    // --- 1. DOM References ---
    const chatMessages      = document.getElementById('chat-messages');
    const messageInput      = document.getElementById('message-input');
    const sendButton        = document.getElementById('send-button');
    const toggleVoiceButton = document.getElementById('toggle-voice-input');
    const recordingIndicator= document.getElementById('recording-indicator');
    const stopRecordingBtn  = document.getElementById('stop-recording');
    const settingsButton    = document.querySelector('.settings-btn');
    const settingsModal     = document.getElementById('settings-modal');
    const closeModalButton  = document.querySelector('.close-modal');
    const saveSettingsBtn   = document.getElementById('save-settings');
    // (Currently not using loadUserInfo to intercept `/api/get-memory`)

    // --- 2. User Preferences (Optional) ---
    let userInfo = {
      name: '',
      birthday: '',
      interests: '',
      outputPreference: 'auto'
    };

    // --- 3. Chat History Loading & Rendering ---
    function loadChatHistory() {
      fetch('/api/get-memory')
        .then(res => res.json())
        .then(history => {
          if (!history.length) {
            appendMessage('嗨～我是Lyra！很高兴认识你哦。❤️', 'received', null, new Date().toISOString());
          } else {
            history.forEach(entry => {
              const role      = entry.role === 'lyra' ? 'received' : 'sent';
              const content   = entry.content   || '';
              const audioUrl  = entry.output_type === 'voice' ? entry.audio_url : null;
              const timestamp = entry.timestamp;
              appendMessage(content, role, audioUrl, timestamp);
            });
          }
          // Make sure to scroll to bottom after rendering all history
          scrollToBottom();
        })
        .catch(err => console.error('加载聊天记录失败：', err));
    }
  
    // --- 4. Send Message ---
    function sendMessage(message, isVoice = false, userAudioUrl = null) {
      if (!message.trim() && !isVoice) return;

      // 1. Instantly render local message
      appendMessage(message, 'sent', userAudioUrl, new Date().toISOString());
      messageInput.value = '';
      scrollToBottom();
      showTypingIndicator();

      // 2. Send to backend
      fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
          message, 
          user_name: userInfo.name,
          preferred_output: userInfo.outputPreference,
          is_voice: isVoice
        })
      })
      .then(res => res.json())
      .then(data => {
        removeTypingIndicator();
        appendMessage(
          data.message,
          'received',
          data.audio_url,
          data.timestamp || new Date().toISOString()
        );
        scrollToBottom();
      })
      .catch(err => {
        console.error(err);
        removeTypingIndicator();
        appendMessage('抱歉，出了一些问题，请稍后再试。', 'received', null, new Date().toISOString());
        scrollToBottom();
      });
    }
  
    // --- 5. Render Single Message ---
    // message: text/transcription content
    // type: 'sent' | 'received'
    // audioUrl: URL if voice message, null otherwise
    // timestamp: ISO time
    function appendMessage(message, type, audioUrl = null, timestamp = null) {
      // Container div with class message-container
      const container = document.createElement('div');
      container.className = 'message-container';

      // Bubble with class message ${type}
      const bubble = document.createElement('div');
      bubble.className = `message ${type}`;
      
      // Text message
      if (!audioUrl) {
        const textDiv = document.createElement('div');
        textDiv.className = 'message-content';
        textDiv.textContent = message;
        bubble.appendChild(textDiv);

      } else {
        // --- Voice Message ---
        // Controls section
        const controls = document.createElement('div');
        controls.className = 'voice-controls';

        const playBtn = document.createElement('button');
        playBtn.className = 'voice-play';
        playBtn.textContent = '▶';

        const pauseBtn = document.createElement('button');
        pauseBtn.className = 'voice-pause';
        pauseBtn.textContent = '⏸';

        controls.append(playBtn, pauseBtn);
        bubble.appendChild(controls);

        // Hidden <audio> element for loading and playback
        const audioElem = document.createElement('audio');
        audioElem.src = audioUrl;
        audioElem.preload = 'metadata';
        audioElem.style.display = 'none';
        bubble.appendChild(audioElem);

        // Play/Pause controls
        playBtn.onclick  = () => audioElem.play();
        pauseBtn.onclick = () => audioElem.pause();

        // Load metadata and update dimensions
        audioElem.addEventListener('loadedmetadata', () => {});
        // Force metadata loading
        audioElem.load();

        // Transcribe button
        const btnWrapper = document.createElement('div');
        btnWrapper.className = `trans-btn-container ${type}`;

        const toggleBtn = document.createElement('div');
        toggleBtn.className = 'toggle-transcript';
        toggleBtn.textContent = '转文字';
        btnWrapper.appendChild(toggleBtn);

        // Transcription area
        const transcript = document.createElement('div');
        transcript.className = 'transcript hidden';
        transcript.textContent = message;

        toggleBtn.onclick = () => {
          const showing = !transcript.classList.toggle('hidden');
          toggleBtn.textContent = showing ? '取消转文字' : '转文字';
                  

        };

        // Mount to container (after bubble and timestamp to ensure transcript is below)
        bubble.appendChild(btnWrapper);
        container.appendChild(transcript);
      }

      // Timestamp
      const timeDiv = document.createElement('div');
      timeDiv.className = `message-time ${type}`;
      timeDiv.textContent = formatTime(new Date(timestamp));

      // Assemble & insert
      container.appendChild(bubble);
      container.appendChild(timeDiv);
      chatMessages.appendChild(container);
    }
  
    // --- 6. Helper Functions ---
    function showTypingIndicator() {
      const tpl = document.createElement('div');
      tpl.className = 'message-container typing-indicator';
      tpl.innerHTML = `<div class="message received"><div class="typing-animation"><span></span><span></span><span></span></div></div>`;
      chatMessages.appendChild(tpl);
      scrollToBottom();
    }
    function removeTypingIndicator() {
      const el = document.querySelector('.typing-indicator');
      if (el) el.remove();
    }
    function scrollToBottom() {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    function formatTime(date) {
      const d = new Date(date);
      return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
    }

    // --- 7. Event Bindings ---
    sendButton.addEventListener('click', () => sendMessage(messageInput.value));
    messageInput.addEventListener('keypress', e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(messageInput.value);
      }
    });
    toggleVoiceButton.addEventListener('click', () => startRecording());
    stopRecordingBtn   .addEventListener('click', stopRecording);
    settingsButton     .addEventListener('click', () => settingsModal.style.display = 'flex');
    closeModalButton   .addEventListener('click', () => settingsModal.style.display = 'none');
    saveSettingsBtn    .addEventListener('click', saveUserInfo);
    window.addEventListener('click', e => {
      if (e.target === settingsModal) settingsModal.style.display = 'none';
    });
  
    // --- 8. Recording Related ---
    let mediaRecorder, audioChunks = [], isRecording = false;
    function startRecording() {
      if (isRecording) return;
      isRecording = true;
      audioChunks = [];
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
          mediaRecorder.onstop = () => {
            recordingIndicator.style.display = 'none';
            const blob = new Blob(audioChunks, { type: 'audio/webm' });
            const form = new FormData();
            form.append('audio', blob);
            fetch('/api/speech-to-text', { method:'POST', body: form })
              .then(r => r.json())
              .then(res => {
                if (res.text) {
                  const url = URL.createObjectURL(blob);
                  sendMessage(res.text, true, url);
                }
              });
          };
          mediaRecorder.start();
          recordingIndicator.style.display = 'flex';
        });
    }
    function stopRecording() {
      if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(t => t.stop());
        isRecording = false;
      }
    }
  
    // --- 9. Settings Panel (Reserved) ---
    function loadUserInfo() {/* future: fetch('/api/get-user-info') */}
    function saveUserInfo() {
      // Your original POST /api/set-memory
      settingsModal.style.display = 'none';
    }
  
    // --- 10. Initialize on Load ---
    loadChatHistory();
  });
