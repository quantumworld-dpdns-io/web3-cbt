import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

// Import translation files
import cognitiveEn from './i18n/cognitive_distortions_en.json'
import cognitiveZhTw from './i18n/cognitive_distortions_zh-tw.json'
import irrationalEn from './i18n/irrational_beliefs_en.json'
import irrationalZhTw from './i18n/irrational_beliefs_zh-tw.json'

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        cognitive: cognitiveEn,
        irrational: irrationalEn,
      },
      'zh-TW': {
        cognitive: cognitiveZhTw,
        irrational: irrationalZhTw,
      },
    },
    fallbackLng: 'zh-TW',
    defaultNS: 'cognitive',
    ns: ['cognitive', 'irrational'],
    interpolation: {
      escapeValue: false,
    },
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
  })

export default i18n