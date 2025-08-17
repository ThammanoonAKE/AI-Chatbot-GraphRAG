import React, { useState, useRef, useEffect } from 'react'
import {
  Box,
  Typography,
  TextField,
  IconButton,
  Paper,
  Container,
} from '@mui/material'
import { Send as SendIcon, Chat as ChatIcon } from '@mui/icons-material'
import { motion, AnimatePresence } from 'framer-motion'
import ChatMessage from './ChatMessage'
import TypingIndicator from './TypingIndicator'
import { useChatAPI } from '../hooks/useChatAPI'

const ChatInterface = () => {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isFirstMessage, setIsFirstMessage] = useState(true)
  const messagesEndRef = useRef(null)
  const { sendMessage, isLoading } = useChatAPI()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      text: inputValue.trim(),
      sender: 'user',
      timestamp: new Date(),
    }

    if (isFirstMessage) {
      setIsFirstMessage(false)
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')

    try {
      const response = await sendMessage(userMessage.text)
      
      const botMessage = {
        id: Date.now() + 1,
        text: response.reply,
        sender: 'bot',
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'ขอโทษครับ เกิดข้อผิดพลาดในการส่งข้อความ กรุณาลองใหม่อีกครั้ง',
        sender: 'bot',
        timestamp: new Date(),
        isError: true,
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <>
      {/* Header */}
      <Box
        sx={{
          padding: '20px 30px',
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          position: 'relative',
          zIndex: 10,
        }}
      >
        <Typography
          variant="h5"
          component="h1"
          sx={{
            fontWeight: 600,
            color: '#fff',
            textAlign: 'center',
            textShadow: '0 2px 10px rgba(0, 0, 0, 0.3)',
            letterSpacing: '0.5px',
          }}
        >
          ⚖️ Thai Legal GraphRAG
        </Typography>
      </Box>

      {/* Chat Messages */}
      <Box
        sx={{
          flex: 1,
          overflowY: 'auto',
          padding: '20px 30px',
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
          '&::-webkit-scrollbar': {
            width: '6px',
          },
          '&::-webkit-scrollbar-track': {
            background: 'transparent',
          },
          '&::-webkit-scrollbar-thumb': {
            background: 'rgba(255, 255, 255, 0.3)',
            borderRadius: '10px',
          },
          '@media (max-width: 768px)': {
            padding: '15px 20px',
          },
        }}
      >
        {isFirstMessage ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: 'rgba(255, 255, 255, 0.7)',
                textAlign: 'center',
                gap: 3,
              }}
            >
              <ChatIcon sx={{ fontSize: 48, opacity: 0.5 }} />
              <Typography variant="h6" sx={{ fontWeight: 500 }}>
                เริ่มต้นการสนทนา
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.7 }}>
                พิมพ์คำถามเกี่ยวกับคดีกฎหมายไทยเพื่อเริ่มการค้นหา
              </Typography>
            </Box>
          </motion.div>
        ) : (
          <AnimatePresence>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
          </AnimatePresence>
        )}
        
        {isLoading && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </Box>

      {/* Input Area */}
      <Box
        sx={{
          padding: '20px 30px',
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(15px)',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          gap: 2,
          alignItems: 'flex-end',
          '@media (max-width: 768px)': {
            padding: '15px 20px',
          },
        }}
      >
        <TextField
          multiline
          maxRows={4}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="พิมพ์ข้อความของคุณที่นี่..."
          disabled={isLoading}
          sx={{
            flex: 1,
            '& .MuiOutlinedInput-root': {
              borderRadius: '25px',
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              color: '#fff',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              '&:hover': {
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'rgba(255, 255, 255, 0.5)',
                },
              },
              '&.Mui-focused': {
                background: 'rgba(255, 255, 255, 0.15)',
                boxShadow: '0 0 20px rgba(255, 255, 255, 0.1)',
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'rgba(255, 255, 255, 0.5)',
                },
              },
              '& .MuiOutlinedInput-notchedOutline': {
                border: 'none',
              },
            },
            '& .MuiInputBase-input': {
              color: '#fff',
              '&::placeholder': {
                color: 'rgba(255, 255, 255, 0.7)',
                opacity: 1,
              },
            },
          }}
        />
        <IconButton
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isLoading}
          sx={{
            padding: '15px',
            background: 'linear-gradient(135deg, #6c63ff 0%, #5848c2 100%)',
            borderRadius: '25px',
            color: '#fff',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            backdropFilter: 'blur(10px)',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 10px 25px rgba(108, 99, 255, 0.4)',
            },
            '&:active': {
              transform: 'translateY(0)',
            },
            '&:disabled': {
              background: 'rgba(255, 255, 255, 0.1)',
              color: 'rgba(255, 255, 255, 0.5)',
            },
          }}
        >
          <SendIcon />
        </IconButton>
      </Box>
    </>
  )
}

export default ChatInterface