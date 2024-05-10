document.getElementById('question').addEventListener('click', function(event) {
    event.preventDefault();

    // Get the user's query
    const query = document.getElementById('chat-input').value;
    const chatContainer = document.getElementById('chat-container');

    if (query != ""){
        const request = {
            msg: query
        }
    
        const chatMessage = document.createElement('div');
    
        chatMessage.classList.add('my-3');
        chatMessage.classList.add('chat-ques')
        chatMessage.classList.add('chat-message')
        chatMessage.innerHTML = `<strong>You:</strong> ${query}`
        // Add the new chat message to the chat container   
        chatContainer.appendChild(chatMessage);
        // Clear the input field
        document.getElementById('chat-input').value = '';
    
        const apiEndpoint = "/question";
    
        fetch(apiEndpoint, {
            method: "POST",
            headers: {
                'Content-Type':
                    'application/json;charset=utf-8'
            },
            body: JSON.stringify(request)
        })
            .then(response => response.json())
            .then(data => {
                resp = data.resp
    
                console.log(resp)
                if(data.ok == "True"){
                    // Create a new chat message element
                    const chatMessage = document.createElement('div');
                    chatMessage.classList.add('chat-resp')
                    chatMessage.classList.add('chat-message')
                    chatMessage.innerHTML = `<p class="airesp"><strong>Brix:</strong> ${resp}</p>`
                    // Add the new chat message to the chat container   
                    chatContainer.appendChild(chatMessage);
                
                    // Scroll to the bottom of the chat container
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            })
    
        // Here you can implement the logic to send the query to the university virtual assistant
        // and display the assistant's response
    }
});