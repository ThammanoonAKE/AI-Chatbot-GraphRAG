import { useState } from 'react'
import { chatAPI } from '../services/api'

export const useChatAPI = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendMessage = async (message, searchType = 'combined', caseType = null, judgeName = null) => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await chatAPI.sendMessage({
        message,
        search_type: searchType,
        case_type: caseType,
        judge_name: judgeName,
      })
      
      return response
    } catch (err) {
      setError(err.message || 'เกิดข้อผิดพลาดในการส่งข้อความ')
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  return {
    sendMessage,
    isLoading,
    error,
  }
}