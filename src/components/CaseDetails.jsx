import React, { useState } from 'react'
import { 
  Box, 
  Typography, 
  Paper, 
  Chip, 
  Button,
  Collapse,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Card,
  CardContent
} from '@mui/material'
import { 
  ExpandMore, 
  ExpandLess, 
  Gavel, 
  AccountBalance, 
  Article, 
  Person,
  Assignment,
  DateRange
} from '@mui/icons-material'

const CaseDetails = ({ caseData, onViewFullCase }) => {
  const [expanded, setExpanded] = useState(false)
  const [fullCase, setFullCase] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleViewFullCase = async () => {
    if (fullCase) {
      setExpanded(!expanded)
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`http://localhost:8000/case/full/${caseData.decision_id}`)
      const data = await response.json()
      
      if (data.found) {
        setFullCase(data.case)
        setExpanded(true)
      } else {
        alert('ไม่พบข้อมูลคดีแบบเต็ม')
      }
    } catch (error) {
      console.error('Error fetching full case:', error)
      alert('เกิดข้อผิดพลาดในการดึงข้อมูลคดี')
    } finally {
      setLoading(false)
    }
  }

  const formatSections = (sections) => {
    if (!sections || typeof sections !== 'object') return []
    
    const formatted = []
    Object.entries(sections).forEach(([law, articles]) => {
      if (Array.isArray(articles)) {
        articles.forEach(article => {
          formatted.push(`${law} ${article}`)
        })
      }
    })
    return formatted
  }

  const renderBasicInfo = () => (
    <Card 
      elevation={0}
      sx={{
        mb: 2,
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
        backdropFilter: 'blur(15px)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: '15px',
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Gavel sx={{ mr: 1, color: '#4fc3f7' }} />
          <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600 }}>
            {caseData.title || caseData.decision_id}
          </Typography>
        </Box>
        
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Assignment sx={{ mr: 1, color: '#81c784', fontSize: 18 }} />
              <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                หมายเลขคดี: {caseData.decision_id}
              </Typography>
            </Box>
          </Grid>
          
          {caseData.case_type && (
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AccountBalance sx={{ mr: 1, color: '#ffb74d', fontSize: 18 }} />
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                  ประเภท: {caseData.case_type}
                </Typography>
              </Box>
            </Grid>
          )}
          
          {caseData.year && (
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <DateRange sx={{ mr: 1, color: '#e57373', fontSize: 18 }} />
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                  ปี: {caseData.year}
                </Typography>
              </Box>
            </Grid>
          )}
        </Grid>

        {caseData.judges && caseData.judges.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Person sx={{ mr: 1, color: '#ba68c8', fontSize: 18 }} />
              <Typography variant="body2" sx={{ color: '#fff', fontWeight: 500 }}>
                ผู้พิพากษา:
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {caseData.judges.map((judge, index) => (
                <Chip
                  key={index}
                  label={judge}
                  size="small"
                  sx={{
                    backgroundColor: 'rgba(186, 104, 200, 0.3)',
                    color: '#fff',
                    border: '1px solid rgba(186, 104, 200, 0.5)',
                  }}
                />
              ))}
            </Box>
          </Box>
        )}

        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
          <Button
            onClick={handleViewFullCase}
            disabled={loading}
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: '#fff',
              borderRadius: '25px',
              px: 3,
              py: 1,
              fontWeight: 600,
              textTransform: 'none',
              '&:hover': {
                background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                transform: 'translateY(-2px)',
              },
              transition: 'all 0.3s ease',
            }}
            startIcon={expanded ? <ExpandLess /> : <ExpandMore />}
          >
            {loading ? 'กำลังโหลด...' : (fullCase ? (expanded ? 'ซ่อนรายละเอียด' : 'แสดงรายละเอียด') : 'ดูข้อมูลเต็ม')}
          </Button>
        </Box>
      </CardContent>
    </Card>
  )

  const renderFullDetails = () => {
    if (!fullCase) return null

    return (
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <Card 
          elevation={0}
          sx={{
            mt: 2,
            background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%)',
            backdropFilter: 'blur(15px)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: '15px',
          }}
        >
          <CardContent>
            {/* Summary Section */}
            {fullCase.summary && (
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Article sx={{ mr: 1, color: '#4fc3f7' }} />
                  <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600 }}>
                    สรุปคดี
                  </Typography>
                </Box>
                <Paper
                  elevation={0}
                  sx={{
                    p: 2,
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '10px',
                  }}
                >
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: 'rgba(255, 255, 255, 0.9)',
                      lineHeight: 1.6,
                      textAlign: 'justify'
                    }}
                  >
                    {fullCase.summary}
                  </Typography>
                </Paper>
              </Box>
            )}

            {/* Litigants Section */}
            {fullCase.litigants && Object.keys(fullCase.litigants).length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600, mb: 2 }}>
                  คู่ความ
                </Typography>
                <Grid container spacing={2}>
                  {Object.entries(fullCase.litigants).map(([role, name], index) => (
                    <Grid item xs={12} md={6} key={index}>
                      <Paper
                        elevation={0}
                        sx={{
                          p: 2,
                          background: 'rgba(255, 255, 255, 0.05)',
                          border: '1px solid rgba(255, 255, 255, 0.1)',
                          borderRadius: '10px',
                        }}
                      >
                        <Typography variant="subtitle2" sx={{ color: '#4fc3f7', mb: 1 }}>
                          {role}
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                          {name}
                        </Typography>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}

            {/* Related Sections */}
            {fullCase.related_sections && Object.keys(fullCase.related_sections).length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600, mb: 2 }}>
                  มาตราที่เกี่ยวข้อง
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {formatSections(fullCase.related_sections).map((section, index) => (
                    <Chip
                      key={index}
                      label={section}
                      size="small"
                      sx={{
                        backgroundColor: 'rgba(76, 195, 247, 0.3)',
                        color: '#fff',
                        border: '1px solid rgba(76, 195, 247, 0.5)',
                      }}
                    />
                  ))}
                </Box>
              </Box>
            )}

            {/* Source */}
            {fullCase.source && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600, mb: 2 }}>
                  แหล่งที่มา
                </Typography>
                <Paper
                  elevation={0}
                  sx={{
                    p: 2,
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '10px',
                  }}
                >
                  <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                    {fullCase.source}
                  </Typography>
                </Paper>
              </Box>
            )}

            {/* Lower and Appeal Courts */}
            {fullCase.lower_and_appeal_courts && fullCase.lower_and_appeal_courts.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ color: '#fff', fontWeight: 600, mb: 2 }}>
                  ศาลชั้นต้นและอุทธรณ์
                </Typography>
                <List>
                  {fullCase.lower_and_appeal_courts.map((court, index) => (
                    <ListItem key={index} sx={{ py: 0.5 }}>
                      <ListItemIcon>
                        <AccountBalance sx={{ color: '#81c784', fontSize: 18 }} />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                            {court}
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}
          </CardContent>
        </Card>
      </Collapse>
    )
  }

  return (
    <Box sx={{ mb: 2 }}>
      {renderBasicInfo()}
      {renderFullDetails()}
    </Box>
  )
}

export default CaseDetails