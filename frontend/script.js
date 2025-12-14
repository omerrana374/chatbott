const API_BASE_URL = "http://127.0.0.1:8000/api";

const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

// Add message to chat
function addMessage(text, isUser = false) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";

  const p = document.createElement("p");
  p.textContent = text;

  contentDiv.appendChild(p);
  messageDiv.appendChild(contentDiv);
  chatMessages.appendChild(messageDiv);

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return messageDiv;
}

// Add loading indicator
function addLoadingMessage() {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot-message";
  messageDiv.id = "loadingMessage";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";

  const loadingDiv = document.createElement("div");
  loadingDiv.className = "loading";
  loadingDiv.innerHTML = "<span></span><span></span><span></span>";

  contentDiv.appendChild(loadingDiv);
  messageDiv.appendChild(contentDiv);
  chatMessages.appendChild(messageDiv);

  chatMessages.scrollTop = chatMessages.scrollHeight;

  return messageDiv;
}

// Remove loading indicator
function removeLoadingMessage() {
  const loadingMessage = document.getElementById("loadingMessage");
  if (loadingMessage) {
    loadingMessage.remove();
  }
}

// Handle form submission
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = messageInput.value.trim();
  if (!message) return;

  // Add user message
  addMessage(message, true);

  // Clear input
  messageInput.value = "";

  // Disable input and button
  messageInput.disabled = true;
  sendButton.disabled = true;

  // Add loading indicator
  addLoadingMessage();

  try {
    // Call API
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: message }),
    });

    removeLoadingMessage();

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to get response");
    }

    const data = await response.json();

    // Add bot response
    if (data.final_answer) {
      addMessage(data.final_answer, false);
    } else {
      addMessage(
        "Sorry, I couldn't generate a response. Please try again.",
        false
      );
    }
  } catch (error) {
    removeLoadingMessage();
    console.error("Error:", error);

    // Add error message
    const errorDiv = document.createElement("div");
    errorDiv.className = "message bot-message";
    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content error-message";
    contentDiv.textContent = `Error: ${error.message}. Please make sure the backend server is running.`;
    errorDiv.appendChild(contentDiv);
    chatMessages.appendChild(errorDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
  } finally {
    // Re-enable input and button
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
  }
});

// Focus input on load
messageInput.focus();
