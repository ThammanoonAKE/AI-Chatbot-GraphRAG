import React from 'react'
import { Box, Typography, Paper } from '@mui/material'
import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import CaseDetails from './CaseDetails'

const ChatMessage = ({ message }) => {
  const isUser = message.sender === 'user'
  const isError = message.isError

  // Check if message contains case information
  const extractCaseInfo = (text) => {
    // Look for case number pattern and extract case info
    const caseNumberMatch = text.match(/(\d{4}\/\d{4})/g)
    if (caseNumberMatch && message.caseData) {
      return message.caseData
    }
    return null
  }

  const caseInfo = !isUser ? extractCaseInfo(message.text) : null

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
      className="message-animation"
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          mb: 2,
        }}
      >
        <Paper
          elevation={0}
          sx={{
            maxWidth: '80%',
            padding: '15px 20px',
            borderRadius: '20px',
            position: 'relative',
            backdropFilter: 'blur(15px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            background: isUser
              ? 'linear-gradient(135deg, rgba(108, 99, 255, 0.3) 0%, rgba(116, 75, 162, 0.3) 100%)'
              : isError
              ? 'linear-gradient(135deg, rgba(255, 99, 99, 0.3) 0%, rgba(255, 132, 132, 0.3) 100%)'
              : 'linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%)',
            color: '#fff',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
              borderRadius: '20px',
              pointerEvents: 'none',
            },
            '@media (max-width: 768px)': {
              maxWidth: '90%',
            },
          }}
        >
          <Box sx={{ position: 'relative', zIndex: 1 }}>
            {isUser ? (
              <Typography
                variant="body1"
                sx={{
                  lineHeight: 1.6,
                  wordBreak: 'break-word',
                }}
              >
                {message.text}
              </Typography>
            ) : (
              <ReactMarkdown
                components={{
                  p: ({ children }) => (
                    <Typography
                      variant="body1"
                      sx={{
                        mb: 1,
                        lineHeight: 1.6,
                        color: 'rgba(255, 255, 255, 0.9)',
                        '&:last-child': { mb: 0 },
                      }}
                    >
                      {children}
                    </Typography>
                  ),
                  h1: ({ children }) => (
                    <Typography
                      variant="h6"
                      sx={{
                        mb: 1.5,
                        fontWeight: 600,
                        color: '#fff',
                        textShadow: '0 1px 3px rgba(0, 0, 0, 0.3)',
                        borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
                        pb: 1,
                      }}
                    >
                      {children}
                    </Typography>
                  ),
                  h2: ({ children }) => (
                    <Typography
                      variant="h6"
                      sx={{
                        mb: 1.5,
                        fontWeight: 600,
                        color: '#fff',
                        textShadow: '0 1px 3px rgba(0, 0, 0, 0.3)',
                        borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
                        pb: 1,
                      }}
                    >
                      {children}
                    </Typography>
                  ),
                  h3: ({ children }) => (
                    <Typography
                      variant="subtitle1"
                      sx={{
                        mb: 1,
                        fontWeight: 600,
                        color: '#fff',
                        textShadow: '0 1px 3px rgba(0, 0, 0, 0.3)',
                      }}
                    >
                      {children}
                    </Typography>
                  ),
                  ul: ({ children }) => (
                    <Box
                      component="ul"
                      sx={{
                        mb: 1.5,
                        pl: 2.5,
                        color: 'rgba(255, 255, 255, 0.9)',
                        '& li': {
                          mb: 0.5,
                          lineHeight: 1.5,
                        },
                      }}
                    >
                      {children}
                    </Box>
                  ),
                  ol: ({ children }) => (
                    <Box
                      component="ol"
                      sx={{
                        mb: 1.5,
                        pl: 2.5,
                        color: 'rgba(255, 255, 255, 0.9)',
                        '& li': {
                          mb: 0.5,
                          lineHeight: 1.5,
                        },
                      }}
                    >
                      {children}
                    </Box>
                  ),
                  strong: ({ children }) => (
                    <Typography
                      component="strong"
                      sx={{
                        fontWeight: 600,
                        color: '#fff',
                      }}
                    >
                      {children}
                    </Typography>
                  ),
                  em: ({ children }) => (
                    <Typography
                      component="em"
                      sx={{
                        fontStyle: 'italic',
                        color: 'rgba(255, 255, 255, 0.8)',
                      }}
                    >
                      {children}
                    </Typography>
                  ),
                  code: ({ children }) => (
                    <Box
                      component="code"
                      sx={{
                        background: 'rgba(0, 0, 0, 0.2)',
                        padding: '2px 6px',
                        borderRadius: '4px',
                        fontFamily: 'Courier New, monospace',
                        fontSize: '0.9em',
                      }}
                    >
                      {children}
                    </Box>
                  ),
                  blockquote: ({ children }) => (
                    <Box
                      component="blockquote"
                      sx={{
                        borderLeft: '3px solid rgba(255, 255, 255, 0.3)',
                        pl: 2,
                        mb: 1.5,
                        fontStyle: 'italic',
                        color: 'rgba(255, 255, 255, 0.8)',
                      }}
                    >
                      {children}
                    </Box>
                  ),
                }}
              >
                {message.text}
              </ReactMarkdown>
            )}
          </Box>
        </Paper>
        
        {/* Show case details if available */}
        {caseInfo && (
          <Box sx={{ mt: 2 }}>
            <CaseDetails caseData={caseInfo} />
          </Box>
        )}
      </Box>
    </motion.div>
  )
}

export default ChatMessage