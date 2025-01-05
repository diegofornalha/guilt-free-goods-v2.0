'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Message {
  id: number;
  sender: string;
  content: string;
  createdAt: string;
}

interface Conversation {
  id: number;
  messages: Message[];
}

export default function Conversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<number | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const router = useRouter();

  useEffect(() => {
    // Fetch conversations on component mount
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const response = await fetch('/api/customer/conversations');
      if (response.ok) {
        const data = await response.json();
        setConversations(data);
      }
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedConversation || !newMessage.trim()) return;

    try {
      const response = await fetch('/api/customer/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: selectedConversation,
          sender: 'user',
          content: newMessage,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // Update conversation with new messages (both user message and auto-response)
        setConversations(prevConversations =>
          prevConversations.map(conv =>
            conv.id === selectedConversation
              ? {
                  ...conv,
                  messages: [...conv.messages, data.user_message, data.auto_response],
                }
              : conv
          )
        );
        setNewMessage('');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="flex h-screen">
      {/* Conversation List */}
      <div className="w-1/4 border-r p-4">
        <h2 className="text-xl font-bold mb-4">Conversations</h2>
        <div className="space-y-2">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => setSelectedConversation(conv.id)}
              className={`w-full p-2 text-left rounded ${
                selectedConversation === conv.id
                  ? 'bg-blue-100'
                  : 'hover:bg-gray-100'
              }`}
            >
              Conversation {conv.id}
            </button>
          ))}
        </div>
      </div>

      {/* Message Board */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 p-4 overflow-y-auto">
          {selectedConversation && (
            <div className="space-y-4">
              {conversations
                .find((conv) => conv.id === selectedConversation)
                ?.messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`p-2 rounded max-w-[80%] ${
                      msg.sender === 'user'
                        ? 'ml-auto bg-blue-100'
                        : 'bg-gray-100'
                    }`}
                  >
                    <p className="text-sm font-semibold">{msg.sender}</p>
                    <p>{msg.content}</p>
                  </div>
                ))}
            </div>
          )}
        </div>

        {/* Message Input */}
        <form onSubmit={handleSendMessage} className="p-4 border-t">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 p-2 border rounded"
              disabled={!selectedConversation}
            />
            <button
              type="submit"
              disabled={!selectedConversation || !newMessage.trim()}
              className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
