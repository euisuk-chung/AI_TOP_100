import { useState, useEffect } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import './App.css'

function App() {
  const [questions, setQuestions] = useState([])
  const [selectedQuestion, setSelectedQuestion] = useState(null)
  const [language, setLanguage] = useState('kr') // 'kr' or 'en'

  // New state structure
  const [intro, setIntro] = useState('')
  const [subQuestions, setSubQuestions] = useState([])
  const [answers, setAnswers] = useState({}) // { "Q1": { code: "...", language: "python" } }
  const [status, setStatus] = useState('')
  const [showSolution, setShowSolution] = useState(false)
  const [solutionContent, setSolutionContent] = useState('')
  const [solutionLoading, setSolutionLoading] = useState(false)
  const [parsedSolutions, setParsedSolutions] = useState({}) // { "Q1": "...", "Q2": "..." }
  const [visibleSolutions, setVisibleSolutions] = useState({}) // { "Q1": true, "Q2": false }

  useEffect(() => {
    fetchQuestions()
  }, [language]) // Re-fetch when language changes

  const fetchQuestions = async () => {
    try {
      const response = await axios.get(`/api/questions?lang=${language}`)
      setQuestions(response.data)
      setSelectedQuestion(null) // Reset selection when changing language
    } catch (error) {
      console.error('Error fetching questions:', error)
    }
  }

  const handleSelectQuestion = async (filename) => {
    try {
      setSelectedQuestion(filename)
      const response = await axios.get(`/api/questions/${filename}?lang=${language}`)

      setIntro(response.data.intro)
      setSubQuestions(response.data.questions)

      // Initialize answers if needed, or reset
      const initialAnswers = {}
      response.data.questions.forEach(q => {
        initialAnswers[q.id] = { code: '', language: 'markdown' }
      })
      setAnswers(initialAnswers)

      setStatus('')
      setShowSolution(false)
      setSolutionContent('')
      setParsedSolutions({})
      setVisibleSolutions({})

      // Fetch solutions for this question
      try {
        const solResponse = await axios.get(`/api/solutions/${filename}?lang=${language}`)
        if (solResponse.data.parsed && solResponse.data.parsed.questions) {
          setParsedSolutions(solResponse.data.parsed.questions)
        }
      } catch (err) {
        console.log('No solution available for this question')
      }
    } catch (error) {
      console.error('Error fetching question content:', error)
    }
  }

  const toggleQuestionSolution = (qId) => {
    setVisibleSolutions(prev => ({
      ...prev,
      [qId]: !prev[qId]
    }))
  }

  const handleShowSolution = async () => {
    if (!selectedQuestion) return

    if (showSolution) {
      setShowSolution(false)
      return
    }

    try {
      setSolutionLoading(true)
      const response = await axios.get(`/api/solutions/${selectedQuestion}?lang=${language}`)
      setSolutionContent(response.data.content)
      setShowSolution(true)
    } catch (error) {
      console.error('Error fetching solution:', error)
      setSolutionContent(language === 'kr' ? '해설을 찾을 수 없습니다.' : 'Solution not found.')
      setShowSolution(true)
    } finally {
      setSolutionLoading(false)
    }
  }

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'kr' ? 'en' : 'kr')
  }

  const handleCodeChange = (qId, newCode) => {
    setAnswers(prev => ({
      ...prev,
      [qId]: { ...prev[qId], code: newCode }
    }))
  }

  const handleLanguageChange = (qId, newLang) => {
    setAnswers(prev => ({
      ...prev,
      [qId]: { ...prev[qId], language: newLang }
    }))
  }

  const handleSave = async () => {
    if (!selectedQuestion) return

    try {
      // Convert answers object to list for backend
      const answersList = Object.entries(answers).map(([id, data]) => ({
        id,
        code: data.code,
        language: data.language
      }))

      await axios.post(`/api/solve/${selectedQuestion}`, {
        answers: answersList
      })
      setStatus('Solutions saved successfully!')
      setTimeout(() => setStatus(''), 3000)
    } catch (error) {
      console.error('Error saving solution:', error)
      setStatus('Failed to save solutions.')
    }
  }

  const MarkdownRenderer = ({ content }) => (
    <ReactMarkdown
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '')
          return !inline && match ? (
            <SyntaxHighlighter
              style={materialDark}
              language={match[1]}
              PreTag="div"
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          )
        }
      }}
    >
      {content}
    </ReactMarkdown>
  )

  return (
    <div className="container">
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Questions</h2>
          <button onClick={toggleLanguage} className="lang-toggle">
            {language === 'kr' ? 'EN' : 'KR'}
          </button>
        </div>
        <ul>
          {questions.map((q) => (
            <li
              key={q.filename}
              onClick={() => handleSelectQuestion(q.filename)}
              className={selectedQuestion === q.filename ? 'active' : ''}
            >
              {q.title}
            </li>
          ))}
        </ul>
      </div>
      <div className="main">
        {selectedQuestion ? (
          <div className="content-wrapper">
            <div className="intro-section">
              <MarkdownRenderer content={intro} />
            </div>

            {subQuestions.map(q => (
              <div key={q.id} className="question-block">
                <div className="question-header">
                  <h3>{q.title}</h3>
                  {parsedSolutions[q.id] && (
                    <button
                      onClick={() => toggleQuestionSolution(q.id)}
                      className="hint-btn"
                    >
                      {visibleSolutions[q.id]
                        ? (language === 'kr' ? '해설 닫기' : 'Hide Hint')
                        : (language === 'kr' ? '해설 보기' : 'Show Hint')
                      }
                    </button>
                  )}
                </div>
                <div className="question-text">
                  <MarkdownRenderer content={q.content} />
                </div>

                {visibleSolutions[q.id] && parsedSolutions[q.id] && (
                  <div className="question-solution">
                    <div className="question-solution-header">
                      {language === 'kr' ? '💡 해설' : '💡 Solution'}
                    </div>
                    <MarkdownRenderer content={parsedSolutions[q.id]} />
                  </div>
                )}

                <div className="editor-section">
                  <div className="controls">
                    <select
                      value={answers[q.id]?.language || 'python'}
                      onChange={(e) => handleLanguageChange(q.id, e.target.value)}
                    >
                      <option value="python">Python</option>
                      <option value="javascript">JavaScript</option>
                      <option value="c">C</option>
                      <option value="cpp">C++</option>
                      <option value="markdown">Markdown</option>
                    </select>
                    <span>{q.id} Solution</span>
                  </div>
                  <textarea
                    value={answers[q.id]?.code || ''}
                    onChange={(e) => handleCodeChange(q.id, e.target.value)}
                    placeholder={`Write your solution for ${q.id} here...`}
                    className="code-editor"
                  />
                </div>
              </div>
            ))}

            <div className="global-controls">
              <button onClick={handleSave} className="save-btn">
                {language === 'kr' ? '모든 답안 저장' : 'Save All Solutions'}
              </button>
              <button onClick={handleShowSolution} className="solution-btn" disabled={solutionLoading}>
                {solutionLoading
                  ? (language === 'kr' ? '로딩...' : 'Loading...')
                  : showSolution
                    ? (language === 'kr' ? '해설 닫기' : 'Hide Solution')
                    : (language === 'kr' ? '해설 보기' : 'Show Solution')
                }
              </button>
              {status && <span className="status">{status}</span>}
            </div>

            {showSolution && (
              <div className="solution-modal">
                <div className="solution-header">
                  <h3>{language === 'kr' ? '모범 답안' : 'Model Solution'}</h3>
                  <button onClick={() => setShowSolution(false)} className="close-btn">×</button>
                </div>
                <div className="solution-content">
                  <MarkdownRenderer content={solutionContent} />
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="placeholder">
            Select a question to start solving.
          </div>
        )}
      </div>
    </div>
  )
}

export default App
