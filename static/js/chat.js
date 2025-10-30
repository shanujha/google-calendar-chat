// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');

    // Load events on page load
    loadEvents();

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        messageInput.value = '';
        
        // Disable send button
        sendBtn.disabled = true;
        sendBtn.textContent = 'Sending...';

        try {
            // Send message to server
            const response = await fetch('/api/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (response.ok) {
                // Add bot response
                addMessage(data.response, 'bot');
                
                // Refresh events list (server-side can include metadata in future)
                setTimeout(loadEvents, 1000);
            } else {
                addMessage(`Error: ${data.error || 'Something went wrong'}`, 'bot');
            }
        } catch (error) {
            addMessage(`Error: ${error.message}`, 'bot');
        } finally {
            // Re-enable send button
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send';
        }
    });

    // Add message to chat
    function addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (type === 'user') {
            contentDiv.innerHTML = `<strong>You:</strong> ${escapeHtml(content)}`;
        } else {
            contentDiv.innerHTML = `<strong>Assistant:</strong> ${formatBotMessage(content)}`;
        }
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Format bot message (convert newlines to <br>, etc.)
    function formatBotMessage(content) {
        // Escape HTML first
        let formatted = escapeHtml(content);
        
        // Convert newlines to <br>
        formatted = formatted.replace(/\n/g, '<br>');
        
        // Convert markdown-style bullets
        formatted = formatted.replace(/^- (.+)$/gm, '• $1');
        
        return formatted;
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Load calendar events
    async function loadEvents() {
        const eventsList = document.getElementById('events-list');
        eventsList.innerHTML = '<div class="loading">Loading events...</div>';

        try {
            const response = await fetch('/api/events');
            const data = await response.json();

            if (response.ok) {
                displayEvents(data.events);
            } else {
                eventsList.innerHTML = `<div class="loading">${data.error || 'Error loading events'}</div>`;
            }
        } catch (error) {
            eventsList.innerHTML = `<div class="loading">Error: ${error.message}</div>`;
        }
    }

    // Display events in sidebar
    function displayEvents(events) {
        const eventsList = document.getElementById('events-list');
        
        if (!events || events.length === 0) {
            eventsList.innerHTML = '<div class="loading">No upcoming events</div>';
            return;
        }

        eventsList.innerHTML = '';
        
        events.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.className = 'event-item';
            
            const timeDiv = document.createElement('div');
            timeDiv.className = 'event-time';
            timeDiv.textContent = formatEventTime(event.start);
            
            const titleDiv = document.createElement('div');
            titleDiv.className = 'event-title';
            titleDiv.textContent = event.summary;
            
            eventDiv.appendChild(timeDiv);
            eventDiv.appendChild(titleDiv);
            eventsList.appendChild(eventDiv);
        });
    }

    // Format event time
    function formatEventTime(dateTimeStr) {
        try {
            const date = new Date(dateTimeStr);
            const options = { 
                month: 'short', 
                day: 'numeric', 
                hour: '2-digit', 
                minute: '2-digit' 
            };
            return date.toLocaleString('en-US', options);
        } catch (error) {
            return dateTimeStr;
        }
    }

    // Make refreshEvents available globally
    window.refreshEvents = loadEvents;
});
