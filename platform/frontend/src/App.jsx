import { useState, useEffect } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkBreaks from 'remark-breaks'
import rehypeRaw from 'rehype-raw'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import './App.css'

const ZoomableImage = ({ src, alt }) => {
  const [scale, setScale] = useState(1)

  const handleZoomIn = () => setScale(prev => Math.min(prev + 0.2, 3))
  const handleZoomOut = () => setScale(prev => Math.max(prev - 0.2, 0.5))
  const handleReset = () => setScale(1)

  return (
    <div className="zoomable-image-container">
      <div className="zoom-controls">
        <button onClick={handleZoomOut} title="Zoom Out">-</button>
        <span className="zoom-level">{Math.round(scale * 100)}%</span>
        <button onClick={handleZoomIn} title="Zoom In">+</button>
        <button onClick={handleReset} title="Reset">Reset</button>
      </div>
      <div className="image-wrapper" style={{ overflow: 'auto' }}>
        <img
          src={src}
          alt={alt}
          className="source-image"
          style={{ transform: `scale(${scale})`, transformOrigin: 'top center', transition: 'transform 0.2s' }}
        />
      </div>
    </div>
  )
}

// Helper component to fetch and display text content
const TextSourceViewer = ({ path }) => {
  const [content, setContent] = useState('Loading...')

  useEffect(() => {
    axios.get(`/${path}`)
      .then(res => {
        if (typeof res.data === 'string') {
          setContent(res.data)
        } else {
          setContent(JSON.stringify(res.data, null, 2))
        }
      })
      .catch(err => setContent('Error loading file content.'))
  }, [path])

  return (
    <div className="text-source-container">
      <pre className="text-source-content">{content}</pre>
    </div>
  )
}

function App() {
  const [questions, setQuestions] = useState([])
  const [selectedQuestion, setSelectedQuestion] = useState(null)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  // New state structure
  const [intro, setIntro] = useState('')
  const [subQuestions, setSubQuestions] = useState([])
  const [sourceInfo, setSourceInfo] = useState(null)
  const [answers, setAnswers] = useState({}) // { "Q1": { code: "...", language: "markdown" } }
  const [status, setStatus] = useState('')

  useEffect(() => {
    fetchQuestions()
  }, [])

  const fetchQuestions = async () => {
    try {
      const response = await axios.get(`/api/questions`)
      setQuestions(response.data)
    } catch (error) {
      console.error('Error fetching questions:', error)
    }
  }

  const handleSelectQuestion = async (filename) => {
    try {
      setSelectedQuestion(filename)
      const response = await axios.get(`/api/questions/${filename}`)

      setIntro(response.data.intro)
      setSubQuestions(response.data.questions)
      setSourceInfo(response.data.source)

      // Initialize answers if needed, or reset
      const initialAnswers = {}
      response.data.questions.forEach(q => {
        initialAnswers[q.id] = { code: '', language: 'markdown' }
      })

      // Fetch user saved answers
      try {
        const userSolResponse = await axios.get(`/api/solve/${filename}`)
        const userAnswers = userSolResponse.data.answers || []

        userAnswers.forEach(ans => {
          if (initialAnswers[ans.id]) {
            initialAnswers[ans.id] = {
              code: ans.code,
              language: 'markdown' // Force markdown
            }
          }
        })
      } catch (err) {
        console.log('No user solutions found')
      }

      setAnswers(initialAnswers)

      setStatus('')
    } catch (error) {
      console.error('Error fetching question content:', error)
    }
  }

  /* Removed toggleQuestionSolution, handleShowSolution, handleLanguageChange */

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen)
  }

  const handleCodeChange = (qId, newCode) => {
    setAnswers(prev => ({
      ...prev,
      [qId]: { ...prev[qId], code: newCode }
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
      remarkPlugins={[remarkGfm, remarkBreaks]}
      rehypePlugins={[rehypeRaw]}
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
        },
        img({ node, ...props }) {
          return <ZoomableImage src={props.src} alt={props.alt} />
        }
      }}
    >
      {content}
    </ReactMarkdown>
  )

  return (
    <div className="container">
      <div className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2>Questions</h2>
          <button className="toggle-sidebar-btn" onClick={toggleSidebar} title="Close Sidebar">
            &lt;
          </button>
        </div>
        {/* 예선 (Preliminary) - Questions 1-5 */}
        <div className="question-section">
          <div className="section-title preliminary">
            예선
          </div>
          <ul>
            {questions.slice(0, 5).map((q) => (
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

        {/* 본선 (Final) - Questions 6-9 */}
        <div className="question-section">
          <div className="section-title final">
            본선
          </div>
          <ul>
            {questions.slice(5).map((q) => (
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
      </div>
      <div className="main">
        {!isSidebarOpen && (
          <button className="open-sidebar-btn" onClick={toggleSidebar} title="Open Sidebar">
            &gt;
          </button>
        )}
        {selectedQuestion ? (
          <div className="content-wrapper">
            <div className="intro-section">
              <MarkdownRenderer content={intro} />

              {/* Source Viewer */}
              {sourceInfo && (sourceInfo.type !== 'gallery' || (sourceInfo.images && sourceInfo.images.length > 0)) && (
                <div className="source-viewer">
                  <h3>Source Material</h3>
                  {(() => {
                    if (sourceInfo.type === 'gallery' && sourceInfo.images) {
                      return (
                        <div className="source-gallery">
                          {sourceInfo.images.map((img, idx) => (
                            <div key={idx} className="gallery-item">
                              <ZoomableImage src={`/${img}`} alt={`${sourceInfo.label} ${idx + 1}`} />
                              <div className="gallery-caption">{img.split('/').pop()}</div>
                            </div>
                          ))}
                        </div>
                      );
                    } else if (sourceInfo.type === 'image' || sourceInfo.path.match(/\.(png|jpg|jpeg|gif)$/i)) {
                      return <ZoomableImage src={`/${sourceInfo.path}`} alt={sourceInfo.label} />;
                    } else if (sourceInfo.type === 'file' || sourceInfo.path.match(/\.(txt|md)$/i)) {
                      return (
                        <div className="source-text-container">
                          <a href={`/${sourceInfo.path}`} target="_blank" rel="noopener noreferrer" className="source-link">
                            Open {sourceInfo.label} in new tab
                          </a>
                        </div>
                      );
                    } else if (sourceInfo.type === 'directory' && sourceInfo.files) {
                      return (
                        <div className="source-directory-list">
                          <div className="directory-label">📁 {sourceInfo.label}</div>
                          <ul>
                            {sourceInfo.files.map((file, idx) => (
                              <li key={idx}>
                                <a href={`/${file}`} target="_blank" rel="noopener noreferrer">
                                  📄 {file.split('/').pop()}
                                </a>
                              </li>
                            ))}
                          </ul>
                        </div>
                      );
                    } else {
                      return (
                        <div className="source-link-container">
                          <a href={`/${sourceInfo.path}`} target="_blank" rel="noopener noreferrer" className="source-link-btn">
                            📂 Open {sourceInfo.label} Folder
                          </a>
                        </div>
                      );
                    }
                  })()}
                </div>
              )}
            </div>

            {subQuestions.map(q => (
              <div key={q.id} className="question-block">
                <div className="question-header">
                  <h3>{q.title}</h3>
                </div>
                <div className="question-text">
                  <MarkdownRenderer content={q.content} />
                </div>

                {/* Per-Question Source Viewer */}
                {q.source && (
                  <div className="source-viewer">
                    <h3>Source Material</h3>
                    {(() => {
                      if (q.source.type === 'gallery' && q.source.images) {
                        return (
                          <div className="source-gallery">
                            {q.source.images.map((img, idx) => (
                              <div key={idx} className="gallery-item">
                                <ZoomableImage src={`/${img}`} alt={`${q.source.label} ${idx + 1}`} />
                                <div className="gallery-caption">{img.split('/').pop()}</div>
                              </div>
                            ))}
                          </div>
                        );
                      } else if (
                        q.source.type === 'image' ||
                        ['.png', '.jpg', '.jpeg', '.gif'].some(ext => q.source.path.toLowerCase().endsWith(ext))
                      ) {
                        return <ZoomableImage src={`/${q.source.path}`} alt={q.source.label} />;
                      } else if (q.source.type === 'directory' && q.source.files) {
                        // Interactive File List
                        return (
                          <div className="source-directory-list">
                            <div className="directory-label">Folder: {q.source.label}</div>
                            <ul>
                              {q.source.files.map((file, idx) => (
                                <li key={idx}>
                                  <a href={`/${file}`} target="_blank" rel="noopener noreferrer">
                                    📄 {file.split('/').pop()}
                                  </a>
                                </li>
                              ))}
                            </ul>
                          </div>
                        );
                      } else if (
                        q.source.type === 'file' ||
                        ['.txt', '.md'].some(ext => q.source.path.toLowerCase().endsWith(ext))
                      ) {
                        // Inline Text Fetcher
                        return <TextSourceViewer path={q.source.path} />;
                      } else {
                        return (
                          <div className="source-link-container">
                            {/* Fallback */}
                            <a href={`/${q.source.path}`} target="_blank" rel="noopener noreferrer" className="source-link-btn">
                              📂 Open {q.source.label}
                            </a>
                          </div>
                        );
                      }
                    })()}
                  </div>
                )}

                <div className="editor-section">
                  <div className="controls">
                    <span>{q.id} Solution (Markdown)</span>
                  </div>
                  <div className="editor-container split-view">
                    <textarea
                      value={answers[q.id]?.code || ''}
                      onChange={(e) => handleCodeChange(q.id, e.target.value)}
                      placeholder={`Write your solution for ${q.id} here...`}
                      className="code-editor"
                    />
                    <div className="markdown-preview">
                      <div className="preview-label">Preview</div>
                      <MarkdownRenderer content={answers[q.id]?.code || ''} />
                    </div>
                  </div>
                </div>
              </div>
            ))}

            <div className="global-controls">
              <button onClick={handleSave} className="save-btn">
                모든 답안 저장
              </button>
              {status && <span className="status">{status}</span>}
            </div>
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
