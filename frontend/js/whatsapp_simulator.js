/**
 * CheckLocal - WhatsApp Bot Interactive Simulator
 * Powers the embedded smartphone preview for judges and users
 */

const WhatsAppSimulator = {
    userId: "+23480" + Math.floor(10000000 + Math.random() * 90000000),
    messagesContainer: null,
    inputEl: null,
    typingIndicator: null,
    userPointsEl: null,
    userBadgeEl: null,
    isTyping: false,

    init() {
        this.messagesContainer = document.getElementById("waMessagesContainer");
        this.inputEl = document.getElementById("waMessageInput");
        this.typingIndicator = document.getElementById("waTypingIndicator");
        this.userPointsEl = document.getElementById("waUserPoints");
        this.userBadgeEl = document.getElementById("waUserBadge");

        if (!this.messagesContainer || !this.inputEl) return;

        // Attach Enter key listener
        this.inputEl.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                this.sendCurrentMessage();
            }
        });

        // Attach Quick Chips
        document.querySelectorAll(".sim-chip").forEach(chip => {
            chip.addEventListener("click", () => {
                const prompt = chip.getAttribute("data-prompt") || chip.textContent.trim();
                this.sendMessage(prompt);
            });
        });
    },

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },

    formatWhatsAppMarkdown(text) {
        if (!text) return "";
        let formatted = text
            .replace(/\*(.*?)\*/g, "<strong>$1</strong>")
            .replace(/_(.*?)_/g, "<em>$1</em>")
            .replace(/~(.*?)~/g, "<del>$1</del>")
            .replace(/```(.*?)```/gs, "<code>$1</code>")
            .replace(/\n/g, "<br>");
        return formatted;
    },

    appendMessage(text, isOutgoing = true, mediaType = "text") {
        const bubble = document.createElement("div");
        bubble.className = `wa-bubble ${isOutgoing ? 'wa-bubble-outgoing' : 'wa-bubble-incoming'}`;

        let mediaHtml = "";
        if (mediaType === "voice_note") {
            mediaHtml = `<div style="display:flex;align-items:center;gap:6px;background:rgba(0,0,0,0.04);padding:4px 8px;border-radius:4px;margin-bottom:4px;font-size:0.75rem;color:#047857;font-family:var(--font-mono);font-weight:700;">[VOICE NOTE TRANSCRIBED]</div>`;
        } else if (mediaType === "screenshot") {
            mediaHtml = `<div style="display:flex;align-items:center;gap:6px;background:rgba(0,0,0,0.04);padding:4px 8px;border-radius:4px;margin-bottom:4px;font-size:0.75rem;color:#0369A1;font-family:var(--font-mono);font-weight:700;">[SCREENSHOT FORWARD ANALYZED]</div>`;
        }

        bubble.innerHTML = `
            ${mediaHtml}
            <div class="wa-msg-content">${this.formatWhatsAppMarkdown(text)}</div>
            <div class="wa-msg-meta">
                <span>${this.getCurrentTime()}</span>
                ${isOutgoing ? '<span style="color:#38BDF8;">✓✓</span>' : ''}
            </div>
        `;

        this.messagesContainer.appendChild(bubble);
        this.scrollToBottom();
    },

    showTyping(show = true) {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = show ? "block" : "none";
            this.scrollToBottom();
        }
    },

    scrollToBottom() {
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    },

    sendCurrentMessage() {
        const text = this.inputEl.value.trim();
        if (!text) return;
        this.inputEl.value = "";
        this.sendMessage(text);
    },

    async sendMessage(text, mediaType = "text") {
        if (this.isTyping) return;
        this.isTyping = true;

        // Render user bubble
        this.appendMessage(text, true, mediaType);
        this.showTyping(true);

        try {
            const response = await fetch("/api/simulate-chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: this.userId,
                    message: text,
                    media_type: mediaType
                })
            });

            const data = await response.json();

            // Simulate realistic WhatsApp transmission delay (450ms - 800ms)
            setTimeout(() => {
                this.showTyping(false);
                this.appendMessage(data.reply, false);

                // Update user points and badge
                if (this.userPointsEl) {
                    this.userPointsEl.textContent = `${data.total_points} pts`;
                }
                if (this.userBadgeEl) {
                    this.userBadgeEl.textContent = data.user_badge;
                }

                // If this report generated or updated trending cards, trigger a feed refresh
                if (window.CheckLocalApp && typeof window.CheckLocalApp.loadTrendingFacts === "function") {
                    window.CheckLocalApp.loadTrendingFacts();
                }

                this.isTyping = false;
            }, 600);

        } catch (err) {
            console.error("Error in simulator:", err);
            this.showTyping(false);
            this.appendMessage("Connection error. Please verify the backend server is active.", false);
            this.isTyping = false;
        }
    }
};

window.WhatsAppSimulator = WhatsAppSimulator;
