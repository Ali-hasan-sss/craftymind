function sendMessage() {
    const msgInput = document.getElementById('user-message');
    const message = msgInput.value.trim();
    if (!message) return;

    const chatBox = document.getElementById('chat-box');

    // رسالة المستخدم
    const userDiv = document.createElement('div');
    userDiv.className = 'chat-message user-msg';
    userDiv.innerText = message;
    chatBox.appendChild(userDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // إرسال البيانات للـ Flask
    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'message=' + encodeURIComponent(message)
    })
    .then(response => response.text())
    .then(data => {
        // عرض رد البوت
        const botDiv = document.createElement('div');
        botDiv.className = 'chat-message bot-msg';
        botDiv.innerText = data;
        chatBox.appendChild(botDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => {
        console.error("خطأ في إرسال الرسالة:", err);
    });

    // مسح حقل الإدخال والتركيز
    msgInput.value = '';
    msgInput.focus();
}
