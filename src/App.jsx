import React from 'react'
import { Box } from '@mui/material'
import ChatInterface from './components/ChatInterface'

function App() {
  return (
    <Box
      sx={{
        width: '100%',
        maxWidth: '900px',
        height: '85vh',
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(20px)',
        borderRadius: '20px',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        boxShadow: '0 25px 50px rgba(0, 0, 0, 0.2)',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
          pointerEvents: 'none',
        },
        '@media (max-width: 768px)': {
          height: '100vh',
          borderRadius: 0,
          maxWidth: '100%',
        },
      }}
    >
      <ChatInterface />
    </Box>
  )
}

export default App