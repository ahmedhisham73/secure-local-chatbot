import React, { useState } from 'react';
import axiosClient from '../api/axiosClient';

const Chat = ({ token }) => {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt) return;  // Don't send empty messages

    setLoading(true);
    // Add user message to the chat
    setMessages((prevMessages) => [...prevMessages, { sender: 'user', text: prompt }]);
    setPrompt('');

    try {
      const res = await axiosClient.post('/chat', { prompt }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const llamaResponse = res.data.response;
      // Add Llama's response to the chat
      setMessages((prevMessages) => [...prevMessages, { sender: 'llama', text: llamaResponse }]);
      setResponse(llamaResponse);
    } catch (err) {
      console.error('Error:', err);
      setMessages((prevMessages) => [...prevMessages, { sender: 'error', text: 'Something went wrong.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.chatContainer}>
      <div style={styles.chatBox}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={msg.sender === 'user' ? styles.userMessage : msg.sender === 'llama' ? styles.llamaMessage : styles.errorMessage}
          >
            <p>{msg.text}</p>
          </div>
        ))}
        {loading && <div style={styles.loading}>Llama is thinking...</div>}
      </div>
      
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your message..."
          style={styles.input}
          autoFocus
        />
        <button type="submit" style={styles.button} disabled={loading}>Send</button>
      </form>
    </div>
  );
};

const styles = {
  chatContainer: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    justifyContent: 'flex-end',
    padding: '10px',
  },
  chatBox: {
    flex: 1,
    overflowY: 'auto',
    padding: '10px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    backgroundColor: '#f9f9f9',
    marginBottom: '10px',
  },
  userMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#d1e7dd',
    padding: '8px',
    borderRadius: '10px',
    margin: '5px 0',
    maxWidth: '80%',
  },
  llamaMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#e2e3e5',
    padding: '8px',
    borderRadius: '10px',
    margin: '5px 0',
    maxWidth: '80%',
  },
  errorMessage: {
    alignSelf: 'center',
    backgroundColor: '#f8d7da',
    padding: '8px',
    borderRadius: '10px',
    margin: '5px 0',
    maxWidth: '80%',
    color: '#721c24',
  },
  loading: {
    textAlign: 'center',
    fontStyle: 'italic',
    color: '#6c757d',
  },
  form: {
    display: 'flex',
    marginTop: '10px',
  },
  input: {
    flex: 1,
    padding: '8px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    marginRight: '10px',
  },
  button: {
    padding: '8px 16px',
    borderRadius: '4px',
    border: '1px solid #007bff',
    backgroundColor: '#007bff',
    color: '#fff',
    cursor: 'pointer',
  },
};

export default Chat;

