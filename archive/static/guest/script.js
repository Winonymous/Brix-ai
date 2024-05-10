document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the user's query
    const query = document.getElementById('chat-input').value;

    const resp = "The boy is okay"

    // Create a new chat message element
    const chatMessage = document.createElement('div');
    chatMessage.classList.add('my-3');
    chatMessage.innerHTML = `<strong>You:</strong> ${query} <p class="text-right"><strong>Brix:</strong> ${resp}</p>`;

    // Add the new chat message to the chat container
    const chatContainer = document.getElementById('chat-container');
    chatContainer.appendChild(chatMessage);

    // Clear the input field
    document.getElementById('chat-input').value = '';

    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Here you can implement the logic to send the query to the university virtual assistant
    // and display the assistant's response
});