import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import './App.css'

// Assessment components
const CognitiveDistortions: React.FC = () => {
  const { t, i18n } = useTranslation('cognitive')
  const [selectedItems, setSelectedItems] = useState<string[]>([])
  const [score, setScore] = useState(0)
  const [showResult, setShowResult] = useState(false)

  const items = t('cognitive_distortions', { returnObjects: true }) as Array<{
    id: string
    label: string
    description: string
    weight: number
    importance_score: number
  }>

  const handleToggle = (id: string) => {
    setSelectedItems(prev => 
      prev.includes(id) 
        ? prev.filter(item => item !== id)
        : [...prev, id]
    )
  }

  const calculateScore = () => {
    const total = items
      .filter(item => selectedItems.includes(item.id))
      .reduce((sum, item) => sum + (item.weight * 2), 0)
    setScore(total)
    setShowResult(true)
  }

  return (
    <div className="assessment-section">
      <h2>{t('metadata.cognitive') || 'Cognitive Distortions Checklist'}</h2>
      <div className="items-list">
        {items.map(item => (
          <label key={item.id} className="item-label">
            <input
              type="checkbox"
              checked={selectedItems.includes(item.id)}
              onChange={() => handleToggle(item.id)}
            />
            <div className="item-content">
              <span className="item-label-text">{item.label}</span>
              <span className="item-description">{item.description}</span>
            </div>
          </label>
        ))}
      </div>
      <button className="assess-btn" onClick={calculateScore}>
        {t('assess') || 'Assess Now'}
      </button>
      {showResult && (
        <div className="result">
          <h3>Result: {score} / {items.reduce((sum, item) => sum + item.weight * 2, 0)}</h3>
          <p>{score > 20 ? 'Consider professional consultation' : 'Within normal range'}</p>
        </div>
      )}
    </div>
  )
}

const IrrationalBeliefs: React.FC = () => {
  const { t } = useTranslation('irrational')
  const [responses, setResponses] = useState<Record<string, number>>({})
  const [score, setScore] = useState(0)
  const [showResult, setShowResult] = useState(false)

  const items = t('irrational_beliefs', { returnObjects: true }) as Array<{
    id: string
    label: string
    description: string
    weight: number
    relevance_score: number
  }>

  const handleChange = (id: string, value: number) => {
    setResponses(prev => ({ ...prev, [id]: value }))
  }

  const calculateScore = () => {
    const total = items.reduce((sum, item) => {
      const response = responses[item.id] || 0
      return sum + (response * item.weight)
    }, 0)
    setScore(total)
    setShowResult(true)
  }

  return (
    <div className="assessment-section">
      <h2>{t('metadata.irrational') || 'Irrational Beliefs Test'}</h2>
      <div className="items-list">
        {items.map(item => (
          <div key={item.id} className="belief-item">
            <div className="belief-label">{item.label}</div>
            <div className="belief-description">{item.description}</div>
            <div className="slider-container">
              <span>0 - Never</span>
              <input
                type="range"
                min="0"
                max="10"
                value={responses[item.id] || 0}
                onChange={e => handleChange(item.id, parseInt(e.target.value))}
              />
              <span>10 - Always</span>
            </div>
            <span className="current-value">{responses[item.id] || 0}/10</span>
          </div>
        ))}
      </div>
      <button className="assess-btn" onClick={calculateScore}>
        Calculate Score
      </button>
      {showResult && (
        <div className="result">
          <h3>Total Score: {score.toFixed(1)}</h3>
          <p>{score > 50 ? 'High irrational beliefs - Consider professional help' : 'Moderate range'}</p>
        </div>
      )}
    </div>
  )
}

const LanguageSelector: React.FC = () => {
  const { i18n } = useTranslation()
  
  return (
    <div className="language-selector">
      <span>Language: </span>
      <select 
        value={i18n.language} 
        onChange={e => i18n.changeLanguage(e.target.value)}
      >
        <option value="en">English</option>
        <option value="zh-TW">繁體中文</option>
      </select>
    </div>
  )
}

const App: React.FC = () => {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Mental Health Assessment Tools</h1>
        <LanguageSelector />
      </header>
      <main className="app-main">
        <CognitiveDistortions />
        <IrrationalBeliefs />
      </main>
      <footer className="app-footer">
        <p>⚠️ This tool is for self-awareness only. Not a substitute for professional diagnosis.</p>
      </footer>
    </div>
  )
}

export default App