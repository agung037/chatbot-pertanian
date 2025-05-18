import $ from 'jquery';
import 'jquery-ui/ui/widgets/button';
import '../styles/index.css';

$(document).ready(function() {
    let nextId = 0;

    // Theme toggling functionality
    function initTheme() {
        // Check for saved theme preference or prefer-color-scheme
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            document.documentElement.classList.add('dark');
            document.documentElement.classList.remove('light');
            updateThemeToggle(true);
        } else {
            document.documentElement.classList.add('light');
            document.documentElement.classList.remove('dark');
            updateThemeToggle(false);
        }
    }

    function updateThemeToggle(isDark) {
        if (isDark) {
            $('#toggleCircle').css('transform', 'translateX(16px)');
            $('#themeText').text('Light Mode');
            $('#darkIcon').addClass('hidden');
            $('#lightIcon').removeClass('hidden');
        } else {
            $('#toggleCircle').css('transform', 'translateX(0)');
            $('#themeText').text('Dark Mode');
            $('#darkIcon').removeClass('hidden');
            $('#lightIcon').addClass('hidden');
        }
    }

    $('#themeToggle').on('click', function() {
        const isDark = document.documentElement.classList.contains('dark');
        
        if (isDark) {
            document.documentElement.classList.remove('dark');
            document.documentElement.classList.add('light');
            localStorage.setItem('theme', 'light');
            updateThemeToggle(false);
        } else {
            document.documentElement.classList.remove('light');
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
            updateThemeToggle(true);
        }
    });

    // Initialize theme on page load
    initTheme();

    // Bot info toggle
    $('#botInfoToggle').on('click', function() {
        const content = $('#botInfoContent');
        const icon = $('#botInfoIcon');
        
        content.toggleClass('hidden');
        icon.toggleClass('rotate-180');
        
        // Save state to localStorage
        localStorage.setItem('aboutState', content.hasClass('hidden') ? 'collapsed' : 'expanded');
    });

    // Load about section state from localStorage
    const aboutState = localStorage.getItem('aboutState');
    if (aboutState === 'collapsed') {
        $('#botInfoContent').addClass('hidden');
        $('#botInfoIcon').addClass('rotate-180');
    }

    // Load chat history from localStorage
    function loadChatHistory() {
        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        const chatMessages = $('#chatMessages');
        
        history.forEach(msg => {
            const messageClass = msg.isUser ? 'user-message' : 'bot-message';
            const messageHtml = `<div class="message ${messageClass}" id="${msg.id}">${msg.text}</div>`;
            chatMessages.append(messageHtml);
        });

        if (history.length > 0) {
            nextId = history.length;
        }
        scrollToBottom();
    }

    function appendMessage(text, isUser) {
        const messageId = 'msg-' + nextId++;
        const messageClass = isUser ? 'user-message' : 'bot-message';
        const messageHtml = `<div class="message ${messageClass}" id="${messageId}">${text}</div>`;
        
        $('#chatMessages').append(messageHtml);
        
        // Save message to localStorage
        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        history.push({
            id: messageId,
            text: text,
            isUser: isUser
        });
        localStorage.setItem('chatHistory', JSON.stringify(history));
        
        scrollToBottom();
    }

    // Clear chat history function
    function clearChatHistory() {
        localStorage.removeItem('chatHistory');
        $('#chatMessages').empty();
        nextId = 0;
    }

    function scrollToBottom() {
        const chatMessages = $('#chatMessages');
        chatMessages.scrollTop(chatMessages.prop("scrollHeight"));
    }

    function sendMessage(event) {
        event.preventDefault();
        const userInput = $('#userInput');
        const message = userInput.val().trim();
        
        if (message === '') return;

        appendMessage(message, true);
        userInput.val('').focus();

        fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || 'Network response was not ok.');
                }).catch(() => {
                    throw new Error('Network response was not ok and error details are unavailable.');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.response) {
                appendMessage(data.response, false);
            } else if (data.error) {
                appendMessage('Error: ' + data.error, false);
            }
        })
        .catch(error => {
            console.error('Error sending message:', error);
            appendMessage('Maaf, terjadi kesalahan: ' + error.message, false);
        });
    }

    // Event listeners
    $('#chatForm').on('submit', sendMessage);
    $('#clearHistory').on('click', function() {
        if (confirm('Are you sure you want to clear all chat history?')) {
            clearChatHistory();
        }
    });

    // Load chat history when page loads
    loadChatHistory();
    scrollToBottom();
}); 