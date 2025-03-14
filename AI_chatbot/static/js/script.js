document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
  
    // Helper: add new message to chat window
    function appendMessage(text, sender) {
      const msgDiv = document.createElement('div');
      msgDiv.classList.add('message', sender);
      msgDiv.textContent = text;
      chatBox.appendChild(msgDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    // Send the user's message to the backend, then display the AI's response
    function sendMessage() {
      const text = userInput.value.trim();
      if (!text) return;
      appendMessage(text, 'user');
      userInput.value = '';
  
      fetch('/get_response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          appendMessage(data.message, 'ai');
        } else {
          appendMessage('Error: ' + data.message, 'ai');
        }
      })
      .catch(error => {
        appendMessage('Error: ' + error, 'ai');
      });
    }
  
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  });
  