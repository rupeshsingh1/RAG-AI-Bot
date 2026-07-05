document.addEventListener("DOMContentLoaded", () => {
  const messagesContainer = document.getElementById("messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const fileInput = document.getElementById("file-upload");
  const fileButton = document.getElementById("file-upload-button");

  let pendingFile = null;

  // 🔥 Prevent any accidental form submission (extra safety)
  document.addEventListener("submit", (e) => {
    e.preventDefault();
  });

  // ✅ Send message button
  sendButton.addEventListener("click", (e) => {
    e.preventDefault();
    handleSend();
  });

  // ✅ Enter key (no reload)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });

  // ✅ Open file picker
  fileButton.addEventListener("click", () => {
    fileInput.click();
  });

  // ✅ File selection
  fileInput.addEventListener("change", (e) => {
    pendingFile = e.target.files[0];

    if (pendingFile) {
      addMessage("user", `📄 Selected file: ${pendingFile.name}`);
    }
  });

  // 🚀 MAIN SEND FUNCTION
  async function handleSend() {
    const message = userInput.value.trim();

    if (!message && !pendingFile) return;

    if (message) {
      addMessage("user", message);
    }

    userInput.value = "";

    try {
      // 📄 Upload file first
      if (pendingFile) {
        await uploadFile(pendingFile);
        pendingFile = null;
      }

      // 💬 Send message
      if (message) {
        addMessage("ai", "Typing...");

        const response = await fetch("http://localhost:8000/api/v1/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question: message
          })
        });

        if (!response.ok) {
          throw new Error("Server error");
        }

        const data = await response.json();

        removeLastMessage(); // remove "Typing..."
        addMessage("ai", data.answer || "No response");
      }

    } catch (error) {
      removeLastMessage();
      addMessage("ai", "❌ Error: " + error.message);
    }
  }

  // 📄 Upload PDF
  async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    addMessage("ai", "Uploading PDF...");

    const response = await fetch("http://localhost:8000/api/v1/upload-pdf", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("File upload failed");
    }

    const data = await response.json();

    removeLastMessage();
    addMessage("ai", `✅ ${data.message || "File uploaded"}`);
  }

  // 💬 Add message to UI
  function addMessage(sender, text) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;

    if (sender === "ai") {
    // ✅ Convert Markdown
    const htmlContent = marked.parse(text, { gfm: true, breaks: true });
    
    // ✅ Create content wrapper FIRST
    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'message-content';
    contentWrapper.innerHTML = htmlContent;
    
    // 🔥 FORCE BOLD WITH INLINE STYLES (overrides all CSS)
    const strongs = contentWrapper.querySelectorAll('strong, b');
    strongs.forEach(s => {
      s.style.fontWeight = '800';
      s.style.color = 'inherit';
      s.style.fontSize = 'inherit';
    });
    
    // ✅ Highlight code AFTER styling
    const codeBlocks = contentWrapper.querySelectorAll('pre code');
    codeBlocks.forEach(block => hljs.highlightElement(block));
    
    // ✅ Add table classes
    contentWrapper.querySelectorAll('table').forEach(t => t.classList.add('markdown-table'));
    
    div.appendChild(contentWrapper);
  } else {
    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'message-content';
    contentWrapper.textContent = text;
    div.appendChild(contentWrapper);
  }

    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // ❌ Remove last message (Typing...)
  function removeLastMessage() {
    const last = messagesContainer.lastChild;
    if (last) last.remove();
  }
});