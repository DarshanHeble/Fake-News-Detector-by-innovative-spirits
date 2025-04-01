import { useState } from "react";
import styles from "./Chat.module.css";
import chatbotIcon from "@assets/bot-logo.png"; // Bot logo
import clientIcon from "@assets/client.png";
import refreshIcon from "@assets/refresh-icon.png"; // Add a refresh icon in your assets folder

const Chat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{ user: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false); // State to track if the bot is typing

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = () => {
    if (!input.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { user: "You", text: input }]);
    setInput("");

    // Simulate bot typing
    setIsTyping(true);
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          user: "Bot",
          text: `Hi, I'm Milo - your Fake News virtual assistant! 😊
I am here to help you detect and analyze fake news effectively. 📰
How can I assist you today?`,
        },
      ]);
      setIsTyping(false); // Stop typing after the response is added
    }, 1000);
  };

  const handleRefresh = () => {
    setMessages([]); // Clear all messages
  };

  return (
    <div>
      {/* Circular Chatbot Icon */}
      {!isOpen && (
        <div className={styles.chatIcon} onClick={toggleChat}>
          <img src={chatbotIcon} alt="Chatbot Icon" />
        </div>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.chatHeader}>
            <div className={styles.headerLeft}>
              <img
                src={chatbotIcon}
                alt="Bot Icon"
                className={styles.botStatusIcon}
              />
              <span className={styles.botStatus}>Bot is online</span>
            </div>
            <div className={styles.headerRight}>
              <img
                src={refreshIcon}
                alt="Refresh"
                className={styles.refreshIcon}
                onClick={handleRefresh}
              />
              <button className={styles.closeButton} onClick={toggleChat}>
                ✕
              </button>
            </div>
          </div>
          <div className={styles.chatMessages}>
            {messages.map((msg, index) => (
              <div
                key={index}
                className={
                  msg.user === "You"
                    ? styles.userMessageContainer
                    : styles.botMessageContainer
                }
              >
                <img
                  src={msg.user === "You" ? clientIcon : chatbotIcon}
                  alt={`${msg.user} Icon`}
                  className={styles.messageIcon}
                />
                <div
                  className={
                    msg.user === "You" ? styles.userMessage : styles.botMessage
                  }
                >
                  <strong>{msg.user}:</strong> {msg.text}
                </div>
              </div>
            ))}
            {/* Bot Typing Indicator */}
            {isTyping && (
              <div className={styles.botMessageContainer}>
                <img
                  src={chatbotIcon}
                  alt="Bot Icon"
                  className={styles.messageIcon}
                />
                <div className={styles.botMessage}>
                  <em>Bot is typing...</em>
                </div>
              </div>
            )}
          </div>
          <div className={styles.chatInput}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chat;