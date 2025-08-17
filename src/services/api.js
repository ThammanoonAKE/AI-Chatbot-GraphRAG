import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data?.error || 'เกิดข้อผิดพลาดจากเซิร์ฟเวอร์')
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้')
    } else {
      // Something else happened
      throw new Error('เกิดข้อผิดพลาดไม่ทราบสาเหตุ')
    }
  }
)

export const chatAPI = {
  sendMessage: async (messageData) => {
    return await apiClient.post('/chat', messageData)
  },
}

export const searchAPI = {
  advancedSearch: async (searchData) => {
    return await apiClient.post('/search', searchData)
  },
  
  searchByCase: async (caseNumber, k = 5) => {
    return await apiClient.get(`/search/case/${encodeURIComponent(caseNumber)}`, {
      params: { k }
    })
  },
  
  searchByJudge: async (judgeName, k = 5) => {
    return await apiClient.get(`/search/judge/${encodeURIComponent(judgeName)}`, {
      params: { k }
    })
  },
  
  searchByType: async (caseType, k = 5) => {
    return await apiClient.get(`/search/type/${encodeURIComponent(caseType)}`, {
      params: { k }
    })
  },
  
  getRelatedCases: async (decisionId, k = 5) => {
    return await apiClient.get(`/search/related/${encodeURIComponent(decisionId)}`, {
      params: { k }
    })
  },
  
  getFullCaseDetails: async (caseNumber) => {
    return await apiClient.get(`/case/full/${encodeURIComponent(caseNumber)}`)
  },
}

export const infoAPI = {
  getCaseTypes: async () => {
    return await apiClient.get('/info/case-types')
  },
  
  getJudges: async () => {
    return await apiClient.get('/info/judges')
  },
  
  getStatistics: async () => {
    return await apiClient.get('/info/statistics')
  },
}

export default apiClient