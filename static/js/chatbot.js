// ==========================================
// FoodExpress AI Chatbot
// ==========================================

const chatToggle = document.getElementById("chat-toggle");
const chatWindow = document.getElementById("chat-window");
const sendButton = document.getElementById("send-message");
const userInput = document.getElementById("user-message");
const chatMessages = document.getElementById("chat-messages");

// ==========================================
// Open / Close Chat
// ==========================================

chatToggle.addEventListener("click", () => {

    if (chatWindow.style.display === "flex") {
        chatWindow.style.display = "none";
    } else {
        chatWindow.style.display = "flex";
    }

});

// ==========================================
// Send Message
// ==========================================

async function sendMessage() {

    const message = userInput.value.trim();

    if (message === "") return;

    // User Message
    chatMessages.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    userInput.value = "";

    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Loading Message
    chatMessages.innerHTML += `
        <div class="bot-message" id="loading">
            Typing...
        </div>
    `;

    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {

        const response = await fetch("/api/ai/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

document.getElementById("loading").remove();

// Format AI response
const formattedReply = data.data.reply
    .replace(/\n/g, "<br>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

const metrics = data.data.metrics;

chatMessages.innerHTML += `
<div class="bot-message">

${formattedReply}

<hr>

<b>📊 Evaluation Metrics</b><br><br>

<b>Expected Answer:</b><br>
${data.data.expected}<br><br>

<b>Accuracy:</b> ${metrics.accuracy}%<br>

<b>Precision:</b> ${metrics.precision}%<br>

<b>Recall:</b> ${metrics.recall}%<br>

<b>F1 Score:</b> ${metrics.f1_score}%<br>

<b>Total Questions:</b> ${metrics.total_questions}<br>

<b>Correct:</b> ${metrics.correct}<br>

<b>Incorrect:</b> ${metrics.incorrect}

</div>
`;

chatMessages.scrollTop = chatMessages.scrollHeight;

    }

    catch (error) {

        document.getElementById("loading").remove();

        chatMessages.innerHTML += `
            <div class="bot-message">
                Sorry, AI Server is unavailable.
            </div>
        `;

    }

}

// ==========================================
// Button Click
// ==========================================

sendButton.addEventListener("click", sendMessage);

// ==========================================
// Enter Key
// ==========================================

userInput.addEventListener("keypress", function(event){

    if(event.key === "Enter"){

        sendMessage();

    }

});
