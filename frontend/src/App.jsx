import { useState } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [videoId, setVideoId] = useState('')
  const [loadedVideoId, setLoadedVideoId] = useState('')
  const [status, setStatus] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [isAsking, setIsAsking] = useState(false)

  const handleLoadVideo = async () => {
    if (!videoId.trim()) return

    setIsLoading(true)
    setStatus('Indexing... this can take a minute for longer videos.')
    setAnswer('')
    setQuestion('')

    try {
      const response = await fetch(`${API_BASE}/index`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_id: videoId }),
      })
      const data = await response.json()

      if (!response.ok) {
        setStatus(`Error: ${data.detail}`)
        setLoadedVideoId('')
      } else {
        setStatus(`Ready — video loaded (${data.status})`)
        setLoadedVideoId(videoId)
      }
    } catch (error) {
      setStatus(`Error: ${error.message}`)
      setLoadedVideoId('')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAskQuestion = async () => {
    if (!loadedVideoId) {
      setAnswer('Please load a video first.')
      return
    }
    if (!question.trim()) return

    setIsAsking(true)
    setAnswer('')

    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_id: loadedVideoId, question }),
      })
      const data = await response.json()
      setAnswer(response.ok ? data.answer : `Error: ${data.detail}`)
    } catch (error) {
      setAnswer(`Error: ${error.message}`)
    } finally {
      setIsAsking(false)
    }
  }

  return (
    <div className="app">
      <h1>AskTheVideo</h1>
      <p className="subtitle">Ask questions about any YouTube video's content.</p>

      <div className="card">
        <div className="input-row">
          <input
            type="text"
            placeholder="Enter a YouTube video ID"
            value={videoId}
            onChange={(e) => setVideoId(e.target.value)}
          />
          <button type="button" onClick={handleLoadVideo} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Load Video'}
          </button>
        </div>
        {status && <p className="status">{status}</p>}
      </div>

      <div className="card">
        <div className="input-row">
          <input
            type="text"
            placeholder="Ask a question about this video"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button type="button" onClick={handleAskQuestion} disabled={isAsking}>
            {isAsking ? 'Thinking...' : 'Ask'}
          </button>
        </div>

        {answer && (
          <div className="answer-box">
            <strong>Answer:</strong>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App