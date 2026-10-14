/**
 * Course FAQ Chatbot — frontend giữ giao diện gốc của cloud.zip.
 * Chỉ gọi AWS HTTP API Gateway (GET /health, POST /chat).
 * Không mô phỏng phản hồi và không gọi LLM hoặc web search.
 * Lịch sử sidebar chỉ được giữ trong phiên trình duyệt đang mở.
 */
document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const welcomeScreen = document.getElementById('welcomeScreen');
  const messagesContainer = document.getElementById('messagesContainer');
  const chatViewport = document.getElementById('chatViewport');
  const newChatBtn = document.getElementById('newChatBtn');
  const chatHistoryList = document.getElementById('chatHistoryList');
  const sidebar = document.getElementById('sidebar');
  const healthBtn = document.getElementById('healthBtn');
  const apiStatus = document.getElementById('apiStatus');
  const promptChips = document.querySelectorAll('.prompt-chip');

  const CONFIG = window.CHATBOT_CONFIG || {};
  const TIMEOUT_MS = 15000;
  const MAX_QUESTION_LENGTH = 500;
  const sessions = [];
  let nextSessionId = 1;
  let activeId = null;
  let isSending = false;
  let checkedHealth = false;

  function apiBase() {
    const value = typeof CONFIG.apiBaseUrl === 'string' ? CONFIG.apiBaseUrl.trim() : '';
    if (!value || value.includes('YOUR_API_ID') || value.includes('THAY_')) {
      throw new Error('Chưa cấu hình API. Mở config.js và điền Invoke URL thật của course-faq-api.');
    }
    if (!/^https:\/\/[a-zA-Z0-9.-]+(?::\d+)?(?:\/[^?#]*)?$/.test(value) &&
        !/^http:\/\/localhost(?::\d+)?(?:\/[^?#]*)?$/.test(value)) {
      throw new Error('Invoke URL không hợp lệ. Cần URL HTTPS của API Gateway.');
    }
    const base = value.replace(/\/+$/, '');
    if (/\/(chat|health)$/.test(base)) {
      throw new Error('config.js chỉ cần Invoke URL gốc (hoặc có stage), không thêm /chat hay /health.');
    }
    return base;
  }

  function createSession() {
    const session = { id: nextSessionId++, title: 'Đoạn chat mới', messages: [] };
    sessions.unshift(session);
    activeId = session.id;
    return session;
  }

  function activeSession() {
    return sessions.find(session => session.id === activeId);
  }

  function updateSendState() {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 160) + 'px';
    const canSend = chatInput.value.trim().length > 0 && !isSending;
    sendBtn.disabled = !canSend;
    sendBtn.classList.toggle('active', canSend);
    newChatBtn.disabled = isSending;
  }

  function hideSidebarMobile() {
    sidebar.classList.remove('open');
  }

  function showToast(message) {
    let toast = document.getElementById('chatToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'chatToast';
      toast.className = 'chat-toast';
      toast.setAttribute('role', 'status');
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(showToast.timeout);
    showToast.timeout = setTimeout(() => toast.classList.remove('visible'), 3200);
  }

  function renderHistory() {
    chatHistoryList.replaceChildren();
    const items = sessions.filter(s => s.messages.length > 0);
    if (!items.length) {
      const empty = document.createElement('p');
      empty.className = 'history-empty';
      empty.textContent = 'Chưa có cuộc hội thoại';
      chatHistoryList.appendChild(empty);
      return;
    }
    for (const session of items) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'history-item';
      button.classList.toggle('active', session.id === activeId);
      button.disabled = isSending;
      button.title = session.title;
      const name = document.createElement('span');
      name.className = 'history-title';
      name.textContent = session.title;
      button.appendChild(name);
      button.addEventListener('click', () => {
        if (isSending) return;
        activeId = session.id;
        renderHistory();
        renderConversation();
        hideSidebarMobile();
      });
      chatHistoryList.appendChild(button);
    }
  }

  function createUserBubble(text) {
    const row = document.createElement('div');
    row.className = 'message-row user';
    const bubble = document.createElement('div');
    bubble.className = 'user-bubble';
    bubble.textContent = text;
    row.appendChild(bubble);
    return row;
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    // S3 website endpoint chỉ HTTP nên Clipboard API có thể không khả dụng.
    const input = document.createElement('textarea');
    input.value = text;
    input.setAttribute('readonly', '');
    input.style.position = 'fixed';
    input.style.left = '-9999px';
    document.body.appendChild(input);
    input.select();
    const copied = document.execCommand('copy');
    input.remove();
    return copied ? Promise.resolve() : Promise.reject(new Error('Không thể sao chép'));
  }

  function createBotBubble(message) {
    const row = document.createElement('div');
    row.className = 'message-row ai';
    const avatar = document.createElement('div');
    avatar.className = 'ai-avatar';
    avatar.textContent = 'FAQ';
    const wrapper = document.createElement('div');
    wrapper.className = 'ai-content-wrapper';
    const bubble = document.createElement('div');
    bubble.className = 'ai-bubble';
    if (message.pending) {
      bubble.classList.add('loading-answer');
      bubble.textContent = 'Đang tìm trong kho FAQ trên S3...';
    } else {
      bubble.textContent = message.text;
    }
    if (message.error) bubble.classList.add('answer-error');
    wrapper.appendChild(bubble);

    if (!message.pending && !message.error) {
      const meta = document.createElement('div');
      meta.className = 'answer-meta';
      if (message.matched) {
        const score = typeof message.similarity === 'number'
          ? ` · Độ tương đồng: ${(message.similarity * 100).toFixed(1)}%`
          : '';
        meta.textContent = `FAQ: ${message.matchedFaqId || 'Không rõ'}${score} · TF-IDF`;
      } else {
        meta.textContent = 'Không tìm thấy FAQ đủ tương đồng';
      }
      wrapper.appendChild(meta);
      if (message.logSaved === false) {
        const note = document.createElement('div');
        note.className = 'log-warning';
        note.textContent = 'Đã trả lời nhưng không ghi được lịch sử lên DynamoDB. Kiểm tra CloudWatch / quyền LabRole.';
        wrapper.appendChild(note);
      }
      const actions = document.createElement('div');
      actions.className = 'message-actions';
      const copy = document.createElement('button');
      copy.type = 'button';
      copy.className = 'msg-text-btn';
      copy.textContent = 'Sao chép';
      copy.addEventListener('click', async () => {
        try {
          await copyText(message.text);
          showToast('Đã sao chép câu trả lời');
        } catch (_) {
          showToast('Trình duyệt không hỗ trợ sao chép trên trang này');
        }
      });
      actions.appendChild(copy);
      wrapper.appendChild(actions);
    }
    row.append(avatar, wrapper);
    return row;
  }

  function renderConversation() {
    const session = activeSession();
    const hasMessages = !!session && session.messages.length > 0;
    welcomeScreen.style.display = hasMessages ? 'none' : 'flex';
    messagesContainer.style.display = hasMessages ? 'flex' : 'none';
    messagesContainer.replaceChildren();
    if (hasMessages) {
      for (const m of session.messages) {
        messagesContainer.appendChild(m.type === 'user' ? createUserBubble(m.text) : createBotBubble(m));
      }
    }
    requestAnimationFrame(() => { chatViewport.scrollTop = chatViewport.scrollHeight; });
  }

  async function fetchJSON(path, options = {}) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);
    try {
      const response = await fetch(`${apiBase()}${path}`, {
        ...options,
        signal: controller.signal,
        headers: { ...(options.headers || {}) }
      });
      const raw = await response.text();
      let data;
      try { data = raw ? JSON.parse(raw) : {}; }
      catch (_) { throw new Error(`API trả dữ liệu không phải JSON (HTTP ${response.status}).`); }
      if (!response.ok) {
        throw new Error(typeof data.error === 'string' ? data.error : `Lỗi API HTTP ${response.status}.`);
      }
      return data;
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('API phản hồi quá lâu (>15 giây). Kiểm tra Lambda, API Gateway và mạng.');
      }
      if (error instanceof TypeError) {
        throw new Error('Không kết nối được API. Kiểm tra Invoke URL, route /chat hoặc /health và CORS trong API Gateway.');
      }
      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  async function sendQuestion() {
    const question = chatInput.value.trim();
    if (!question || isSending) return;
    if (question.length > MAX_QUESTION_LENGTH) {
      showToast('Câu hỏi dài tối đa 500 ký tự.');
      return;
    }
    const session = activeSession();
    if (!session) return;
    if (session.messages.length === 0) {
      session.title = question.slice(0, 50);
    }
    session.messages.push({ type: 'user', text: question });
    const reply = { type: 'bot', pending: true, text: '' };
    session.messages.push(reply);
    chatInput.value = '';
    isSending = true;
    updateSendState();
    renderHistory();
    renderConversation();
    hideSidebarMobile();

    try {
      const data = await fetchJSON('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      if (!data || typeof data.answer !== 'string') {
        throw new Error('API /chat thiếu trường answer. Kiểm tra code Lambda đã triển khai.');
      }
      Object.assign(reply, {
        pending: false,
        text: data.answer,
        matched: data.matched === true,
        matchedFaqId: data.matchedFaqId,
        similarity: Number.isFinite(Number(data.similarity)) ? Number(data.similarity) : null,
        logSaved: data.logSaved
      });
    } catch (err) {
      Object.assign(reply, { pending: false, error: true, text: `Không gửi được câu hỏi: ${err.message}` });
    } finally {
      isSending = false;
      updateSendState();
      renderHistory();
      renderConversation();
      chatInput.focus();
    }
  }

  async function checkHealth() {
    if (checkedHealth) return;
    checkedHealth = true;
    healthBtn.disabled = true;
    apiStatus.className = 'api-state is-checking';
    apiStatus.textContent = 'Đang kiểm tra...';
    try {
      const data = await fetchJSON('/health');
      if (data.status !== 'ok') {
        throw new Error('API trả phản hồi nhưng status không phải ok.');
      }
      apiStatus.className = 'api-state is-ok';
      apiStatus.textContent = 'API hoạt động';
      showToast('Kết nối GET /health thành công');
    } catch (err) {
      apiStatus.className = 'api-state is-error';
      apiStatus.textContent = 'API gặp lỗi';
      showToast(err.message);
    } finally {
      checkedHealth = false;
      healthBtn.disabled = false;
    }
  }

  chatInput.addEventListener('input', updateSendState);
  chatInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendQuestion();
    }
  });
  sendBtn.addEventListener('click', sendQuestion);
  healthBtn.addEventListener('click', checkHealth);

  newChatBtn.addEventListener('click', () => {
    if (isSending) return;
    const current = activeSession();
    if (!current || current.messages.length > 0) createSession();
    chatInput.value = '';
    updateSendState();
    renderHistory();
    renderConversation();
    chatInput.focus();
    hideSidebarMobile();
  });

  promptChips.forEach(chip => chip.addEventListener('click', () => {
    if (isSending) return;
    chatInput.value = chip.dataset.prompt || '';
    updateSendState();
    sendQuestion();
  }));
  document.getElementById('collapseSidebarBtn').addEventListener('click', () => {
    sidebar.classList.add('collapsed');
    sidebar.classList.remove('open');
    document.getElementById('appLayout').classList.add('sidebar-is-collapsed');
  });
  document.getElementById('openSidebarBtn').addEventListener('click', () => {
    sidebar.classList.remove('collapsed');
    sidebar.classList.add('open');
    document.getElementById('appLayout').classList.remove('sidebar-is-collapsed');
  });
  createSession();
  updateSendState();
  renderHistory();
  renderConversation();
  if (!CONFIG.apiBaseUrl || String(CONFIG.apiBaseUrl).includes('YOUR_API_ID')) {
    apiStatus.className = 'api-state is-error';
    apiStatus.textContent = 'Chưa cấu hình API';
  }
});
