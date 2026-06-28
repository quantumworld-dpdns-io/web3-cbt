import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'

import cogEn from './i18n/cognitive_distortions_en.json'
import cogZhTw from './i18n/cognitive_distortions_zh-tw.json'
import irrEn from './i18n/irrational_beliefs_en.json'
import irrZhTw from './i18n/irrational_beliefs_zh-tw.json'

interface AssessmentItem {
  id: string
  label: string
  description: string
  weight: number
  importance_score?: number
  relevance_score?: number
  original_source: string
}

interface AssessmentComponentProps {
  type: 'cognitive' | 'irrational'
  items: AssessmentItem[]
  onComplete: (score: number, answers: Record<string, number>) => void
}

const AssessmentForm: React.FC<AssessmentComponentProps> = ({ type, items, onComplete }) => {
  const { t } = useTranslation()
  const [answers, setAnswers] = useState<Record<string, number>>({})
  const [showResult, setShowResult] = useState(false)
  const [score, setScore] = useState(0)

  const handleAnswer = (itemId: string, value: number) => {
    setAnswers(prev => ({ ...prev, [itemId]: value }))
  }

  const calculateScore = () => {
    let totalScore = 0
    items.forEach(item => {
      const answer = answers[item.id] || 0
      totalScore += answer * item.weight
    })
    setScore(totalScore)
    setShowResult(true)
    onComplete(totalScore, answers)
  }

  const reset = () => {
    setAnswers({})
    setShowResult(false)
    setScore(0)
  }

  const getSeverity = (s: number) => {
    if (type === 'cognitive') {
      if (s <= 15) return { label: t('severity.mild'), color: '#4caf50' }
      if (s <= 30) return { label: t('severity.moderate'), color: '#ff9800' }
      return { label: t('severity.severe'), color: '#f44336' }
    }
    if (s <= 20) return { label: t('severity.mild'), color: '#4caf50' }
    if (s <= 40) return { label: t('severity.moderate'), color: '#ff9800' }
    return { label: t('severity.severe'), color: '#f44336' }
  }

  if (!items.length) return null

  const severity = getSeverity(score)

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>
        {type === 'cognitive' ? t('cognitive.title') : t('irrational.title')}
      </h2>
      <p style={styles.subtitle}>
        {type === 'cognitive' ? t('cognitive.subtitle') : t('irrational.subtitle')}
      </p>

      <div style={styles.form}>
        {items.map(item => (
          <div key={item.id} style={styles.item}>
            <div style={styles.question}>
              <strong>{item.label}</strong>
              <p style={styles.description}>{item.description}</p>
            </div>
            <div style={styles.scale}>
              {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(val => (
                <label key={val} style={styles.scaleLabel}>
                  <input
                    type="radio"
                    name={`item-${item.id}`}
                    value={val}
                    checked={answers[item.id] === val}
                    onChange={() => handleAnswer(item.id, val)}
                    style={styles.radio}
                  />
                  <span style={styles.scaleValue}>{val}</span>
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>

      {!showResult ? (
        <button style={styles.submitButton} onClick={calculateScore}>
          {t('submit')}
        </button>
      ) : (
        <div style={styles.result}>
          <h3>{t('result.title')}</h3>
          <div style={{ ...styles.score, color: severity.color }}>
            {t('result.score')}: {score.toFixed(1)}
          </div>
          <div style={{ ...styles.severity, color: severity.color }}>
            {t('result.severity')}: {severity.label}
          </div>
          <p style={styles.recommendation}>{t('result.recommendation')}</p>
          <button style={styles.resetButton} onClick={reset}>
            {t('reset')}
          </button>
        </div>
      )}
    </div>
  )
}

const Header: React.FC = () => {
  const { t, i18n } = useTranslation()

  return (
    <header style={styles.header}>
      <h1 style={styles.logo}>
        {t('app.name')}
      </h1>
      <div style={styles.langSwitcher}>
        <select
          value={i18n.language}
          onChange={(e) => i18n.changeLanguage(e.target.value)}
          style={styles.langSelect}
        >
          <option value="en">English</option>
          <option value="zh-TW">繁體中文</option>
        </select>
      </div>
    </header>
  )
}

const App: React.FC = () => {
  const { t, i18n } = useTranslation()
  const [cognitiveItems, setCognitiveItems] = useState<AssessmentItem[]>([])
  const [irrationalItems, setIrrationalItems] = useState<AssessmentItem[]>([])
  const [cognitiveScore, setCognitiveScore] = useState(0)
  const [irrationalScore, setIrrationalScore] = useState(0)

  useEffect(() => {
    const lang = i18n.language
    if (lang === 'zh-TW') {
      setCognitiveItems(cogZhTw.cognitive_distortions || [])
      setIrrationalItems(irrZhTw.irrational_beliefs || [])
    } else {
      setCognitiveItems(cogEn.cognitive_distortions || [])
      setIrrationalItems(irrEn.irrational_beliefs || [])
    }
  }, [i18n.language])

  const handleCognitiveComplete = (score: number) => setCognitiveScore(score)
  const handleIrrationalComplete = (score: number) => setIrrationalScore(score)

  return (
    <div style={styles.app}>
      <Header />
      <main style={styles.main}>
        <section style={styles.section}>
          <AssessmentForm
            type="cognitive"
            items={cognitiveItems}
            onComplete={handleCognitiveComplete}
          />
        </section>
        <section style={styles.section}>
          <AssessmentForm
            type="irrational"
            items={irrationalItems}
            onComplete={handleIrrationalComplete}
          />
        </section>

        {(cognitiveScore > 0 || irrationalScore > 0) && (
          <div style={styles.summary}>
            <h2>{t('summary.title')}</h2>
            <div style={styles.summaryGrid}>
              <div style={styles.summaryCard}>
                <h3>{t('cognitive.title')}</h3>
                <p style={styles.summaryScore}>{cognitiveScore.toFixed(1)}</p>
              </div>
              <div style={styles.summaryCard}>
                <h3>{t('irrational.title')}</h3>
                <p style={styles.summaryScore}>{irrationalScore.toFixed(1)}</p>
              </div>
            </div>
          </div>
        )}
      </main>
      <footer style={styles.footer}>
        <p>{t('app.disclaimer')}</p>
        <p style={styles.sources}>
          {t('app.sources')}
        </p>
      </footer>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  app: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1rem 2rem',
    backgroundColor: '#fff',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  logo: {
    margin: 0,
    fontSize: '1.5rem',
    color: '#2c3e50'
  },
  langSwitcher: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem'
  },
  langSelect: {
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #ddd',
    backgroundColor: '#fff'
  },
  main: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '2rem'
  },
  section: {
    marginBottom: '2rem',
    backgroundColor: '#fff',
    borderRadius: '8px',
    padding: '1.5rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
  },
  container: {
    width: '100%'
  },
  title: {
    marginTop: 0,
    marginBottom: '0.5rem',
    color: '#2c3e50'
  },
  subtitle: {
    color: '#666',
    marginBottom: '1.5rem'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem'
  },
  item: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    padding: '1rem',
    backgroundColor: '#fafafa',
    borderRadius: '8px'
  },
  question: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.25rem'
  },
  description: {
    color: '#666',
    fontSize: '0.9rem',
    margin: 0
  },
  scale: {
    display: 'flex',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: '0.5rem'
  },
  scaleLabel: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    cursor: 'pointer',
    padding: '0.25rem 0.5rem',
    borderRadius: '4px',
    transition: 'background-color 0.2s'
  },
  radio: {
    marginBottom: '0.25rem',
    transform: 'scale(1.2)'
  },
  scaleValue: {
    fontSize: '0.8rem',
    color: '#333'
  },
  submitButton: {
    alignSelf: 'center',
    padding: '0.75rem 2rem',
    fontSize: '1rem',
    backgroundColor: '#2c3e50',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginTop: '1rem'
  },
  result: {
    textAlign: 'center',
    padding: '1.5rem',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    marginTop: '1rem'
  },
  score: {
    fontSize: '2rem',
    fontWeight: 'bold',
    margin: '0.5rem 0'
  },
  severity: {
    fontSize: '1.2rem',
    fontWeight: 'bold',
    marginBottom: '1rem'
  },
  recommendation: {
    color: '#666',
    marginBottom: '1rem'
  },
  resetButton: {
    padding: '0.5rem 1.5rem',
    backgroundColor: '#6c757d',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  summary: {
    marginTop: '2rem',
    padding: '1.5rem',
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '1rem',
    marginTop: '1rem'
  },
  summaryCard: {
    textAlign: 'center',
    padding: '1rem',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px'
  },
  summaryScore: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#2c3e50',
    margin: '0.5rem 0'
  },
  footer: {
    textAlign: 'center',
    padding: '2rem',
    color: '#666',
    fontSize: '0.85rem'
  },
  sources: {
    marginTop: '0.5rem'
  }
}

export default App
