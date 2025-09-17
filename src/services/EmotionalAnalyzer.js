/**
 * Serviço de Análise Emocional
 * Detecta emoções e estados emocionais baseado em texto do usuário
 */

class EmotionalAnalyzer {
  constructor() {
    // Dicionário de palavras-chave emocionais
    this.emotionalKeywords = {
      ansiedade: ['ansioso', 'preocupado', 'nervoso', 'tenso', 'estressado', 'inquieto', 'apreensivo'],
      tristeza: ['triste', 'melancólico', 'deprimido', 'desanimado', 'abatido', 'solitário', 'vazio'],
      raiva: ['irritado', 'furioso', 'bravo', 'zangado', 'indignado', 'revoltado', 'frustrado'],
      alegria: ['feliz', 'alegre', 'contente', 'animado', 'eufórico', 'radiante', 'satisfeito'],
      medo: ['medo', 'assustado', 'aterrorizado', 'amedrontado', 'receoso', 'temeroso', 'inseguro'],
      gratidão: ['grato', 'agradecido', 'reconhecido', 'abençoado', 'privilegiado', 'sortudo'],
      esperança: ['esperançoso', 'otimista', 'confiante', 'positivo', 'animado', 'motivado'],
      paz: ['calmo', 'tranquilo', 'sereno', 'pacífico', 'relaxado', 'equilibrado', 'centrado'],
      confusão: ['confuso', 'perdido', 'desorientado', 'incerto', 'indeciso', 'atordoado'],
      energia: ['energético', 'vibrante', 'dinâmico', 'ativo', 'entusiasmado', 'vivaz']
    };

    // Intensidades emocionais
    this.intensityWords = {
      baixa: ['um pouco', 'levemente', 'meio', 'ligeiramente'],
      média: ['bastante', 'bem', 'muito'],
      alta: ['extremamente', 'profundamente', 'intensamente', 'completamente']
    };
  }

  /**
   * Analisa o texto e retorna as emoções detectadas
   * @param {string} text - Texto a ser analisado
   * @returns {Object} Objeto com emoções detectadas e suas intensidades
   */
  analyzeText(text) {
    if (!text || typeof text !== 'string') {
      return { emotions: [], dominantEmotion: null, intensity: 'baixa' };
    }

    const normalizedText = text.toLowerCase();
    const detectedEmotions = [];
    let maxScore = 0;
    let dominantEmotion = null;

    // Detectar emoções
    for (const [emotion, keywords] of Object.entries(this.emotionalKeywords)) {
      let score = 0;
      const foundKeywords = [];

      keywords.forEach(keyword => {
        if (normalizedText.includes(keyword)) {
          score++;
          foundKeywords.push(keyword);
        }
      });

      if (score > 0) {
        detectedEmotions.push({
          emotion,
          score,
          keywords: foundKeywords,
          confidence: Math.min(score / keywords.length, 1)
        });

        if (score > maxScore) {
          maxScore = score;
          dominantEmotion = emotion;
        }
      }
    }

    // Detectar intensidade
    const intensity = this.detectIntensity(normalizedText);

    return {
      emotions: detectedEmotions.sort((a, b) => b.score - a.score),
      dominantEmotion,
      intensity,
      textLength: text.length,
      analysisTimestamp: new Date().toISOString()
    };
  }

  /**
   * Detecta a intensidade emocional no texto
   * @param {string} normalizedText - Texto normalizado
   * @returns {string} Intensidade detectada
   */
  detectIntensity(normalizedText) {
    for (const [intensity, words] of Object.entries(this.intensityWords)) {
      for (const word of words) {
        if (normalizedText.includes(word)) {
          return intensity;
        }
      }
    }
    return 'média'; // Intensidade padrão
  }

  /**
   * Gera um ambiente visual baseado na emoção dominante
   * @param {string} emotion - Emoção dominante
   * @param {string} intensity - Intensidade emocional
   * @returns {Object} Descrição do ambiente visual
   */
  generateVisualEnvironment(emotion, intensity = 'média') {
    const environments = {
      ansiedade: {
        baixa: "Gentle mist clearing in a quiet forest, soft sunlight filtering through leaves",
        média: "Calm lake with gentle ripples, surrounded by peaceful mountains",
        alta: "Deep breathing space with flowing water sounds and warm, soft lighting"
      },
      tristeza: {
        baixa: "Soft rain on a window, cozy indoor space with warm tea",
        média: "Quiet lakeside at dusk with gentle waves and soft clouds",
        alta: "Healing garden with gentle rain, rainbow appearing through clouds"
      },
      raiva: {
        baixa: "Cool breeze through tall grass, distant mountains",
        média: "Powerful waterfall with mist, surrounded by strong trees",
        alta: "Storm clouds clearing to reveal bright sunshine and open sky"
      },
      alegria: {
        baixa: "Sunny meadow with wildflowers and butterflies",
        média: "Bright beach with gentle waves and seagulls",
        alta: "Vibrant sunrise over blooming fields, birds singing"
      },
      medo: {
        baixa: "Safe cabin with warm firelight and soft blankets",
        média: "Protected garden with high walls and gentle fountain",
        alta: "Bright lighthouse on a hill, beacon of safety and guidance"
      },
      gratidão: {
        baixa: "Golden hour in a peaceful garden with blooming flowers",
        média: "Warm sunrise over a fertile valley with abundant harvest",
        alta: "Magnificent cathedral of light with floating golden particles"
      },
      esperança: {
        baixa: "Dawn breaking over a quiet hill with morning dew",
        média: "Rainbow after rain, sun breaking through clouds",
        alta: "Brilliant sunrise over endless possibilities, birds soaring"
      },
      paz: {
        baixa: "Still pond reflecting sky, surrounded by bamboo",
        média: "Zen garden with raked sand and balanced stones",
        alta: "Infinite starry sky with gentle cosmic sounds and floating meditation"
      },
      confusão: {
        baixa: "Gentle fog slowly clearing to reveal a clear path",
        média: "Maze garden with clear signs and helpful guides",
        alta: "Lighthouse beam cutting through fog, revealing safe harbor"
      },
      energia: {
        baixa: "Fresh morning air with gentle breeze and bird songs",
        média: "Dynamic waterfall with rainbow mist and vibrant plants",
        alta: "Electric aurora dancing over snow-capped peaks, pure energy"
      }
    };

    const environment = environments[emotion]?.[intensity] || environments.paz.média;
    
    return {
      description: environment,
      emotion,
      intensity,
      suggestedDuration: this.getSuggestedDuration(emotion, intensity),
      breathingPattern: this.getBreathingPattern(emotion),
      colors: this.getEmotionalColors(emotion),
      sounds: this.getAmbientSounds(emotion)
    };
  }

  /**
   * Retorna duração sugerida para a experiência
   * @param {string} emotion - Emoção
   * @param {string} intensity - Intensidade
   * @returns {number} Duração em minutos
   */
  getSuggestedDuration(emotion, intensity) {
    const baseDuration = {
      ansiedade: 5,
      tristeza: 7,
      raiva: 3,
      alegria: 3,
      medo: 8,
      gratidão: 5,
      esperança: 4,
      paz: 10,
      confusão: 6,
      energia: 2
    };

    const intensityMultiplier = {
      baixa: 0.7,
      média: 1,
      alta: 1.5
    };

    return Math.round(baseDuration[emotion] * intensityMultiplier[intensity]);
  }

  /**
   * Retorna padrão de respiração recomendado
   * @param {string} emotion - Emoção
   * @returns {Object} Padrão de respiração
   */
  getBreathingPattern(emotion) {
    const patterns = {
      ansiedade: { inhale: 4, hold: 4, exhale: 6, name: "Respiração Calmante" },
      tristeza: { inhale: 4, hold: 2, exhale: 4, name: "Respiração Suave" },
      raiva: { inhale: 3, hold: 1, exhale: 5, name: "Respiração Liberadora" },
      alegria: { inhale: 3, hold: 1, exhale: 3, name: "Respiração Energizante" },
      medo: { inhale: 4, hold: 4, exhale: 4, name: "Respiração Equilibrante" },
      gratidão: { inhale: 5, hold: 2, exhale: 5, name: "Respiração Expansiva" },
      esperança: { inhale: 4, hold: 2, exhale: 4, name: "Respiração Elevadora" },
      paz: { inhale: 6, hold: 2, exhale: 6, name: "Respiração Profunda" },
      confusão: { inhale: 4, hold: 4, exhale: 4, name: "Respiração Clarificadora" },
      energia: { inhale: 3, hold: 1, exhale: 2, name: "Respiração Vitalizante" }
    };

    return patterns[emotion] || patterns.paz;
  }

  /**
   * Retorna cores associadas à emoção
   * @param {string} emotion - Emoção
   * @returns {Array} Array de cores
   */
  getEmotionalColors(emotion) {
    const colors = {
      ansiedade: ['#87CEEB', '#E6F3FF', '#B0E0E6'], // Azul claro, calmante
      tristeza: ['#708090', '#D3D3D3', '#F0F8FF'], // Cinza suave, azul muito claro
      raiva: ['#FF6B6B', '#FFB6C1', '#FFF0F5'], // Vermelho suave, rosa
      alegria: ['#FFD700', '#FFA500', '#FFFFE0'], // Dourado, laranja, amarelo claro
      medo: ['#DDA0DD', '#E6E6FA', '#F8F8FF'], // Roxo suave, lavanda
      gratidão: ['#32CD32', '#98FB98', '#F0FFF0'], // Verde, verde claro
      esperança: ['#87CEFA', '#B0C4DE', '#F0F8FF'], // Azul céu, azul claro
      paz: ['#F5F5DC', '#FFFAF0', '#FFFFFF'], // Bege, branco
      confusão: ['#D2B48C', '#F5DEB3', '#FFF8DC'], // Marrom claro, bege
      energia: ['#FF4500', '#FF6347', '#FFE4E1'] // Laranja vibrante, vermelho tomate
    };

    return colors[emotion] || colors.paz;
  }

  /**
   * Retorna sons ambientais recomendados
   * @param {string} emotion - Emoção
   * @returns {Array} Array de sons
   */
  getAmbientSounds(emotion) {
    const sounds = {
      ansiedade: ['ocean waves', 'gentle rain', 'soft wind'],
      tristeza: ['light rain', 'distant thunder', 'soft piano'],
      raiva: ['waterfall', 'strong wind', 'crackling fire'],
      alegria: ['birds singing', 'children laughing', 'gentle breeze'],
      medo: ['heartbeat', 'protective sounds', 'safe harbor'],
      gratidão: ['temple bells', 'nature sounds', 'harmonious tones'],
      esperança: ['sunrise sounds', 'birds chirping', 'gentle wind'],
      paz: ['meditation bells', 'silence', 'soft breathing'],
      confusão: ['clearing sounds', 'gentle guidance', 'soft chimes'],
      energia: ['energetic music', 'dynamic sounds', 'uplifting tones']
    };

    return sounds[emotion] || sounds.paz;
  }

  /**
   * Gera um mantra personalizado baseado na emoção
   * @param {string} emotion - Emoção dominante
   * @param {string} intensity - Intensidade emocional
   * @returns {string} Mantra personalizado
   */
  generatePersonalizedMantra(emotion, intensity) {
    const mantras = {
      ansiedade: {
        baixa: "Este momento é temporário. Eu respiro e encontro paz.",
        média: "Eu sou maior que minha ansiedade. Cada respiração me traz calma.",
        alta: "Eu me entrego ao fluxo da vida. Estou seguro neste momento presente."
      },
      tristeza: {
        baixa: "É natural sentir. Eu me permito processar com gentileza.",
        média: "Esta tristeza também passará. Eu me acolho com compaixão.",
        alta: "Mesmo na tristeza, há beleza. Eu honro meus sentimentos e me curo."
      },
      raiva: {
        baixa: "Eu reconheço minha raiva e escolho responder com sabedoria.",
        média: "Esta energia pode ser transformada. Eu canalizo minha força para o bem.",
        alta: "Eu sou mais poderoso que minha raiva. Escolho a paz e a compreensão."
      },
      alegria: {
        baixa: "Eu celebro este momento de alegria e gratidão.",
        média: "Minha alegria é contagiante. Eu compartilho luz com o mundo.",
        alta: "Eu sou pura alegria em movimento. Minha felicidade é um presente."
      },
      medo: {
        baixa: "Eu reconheço meu medo e escolho a coragem.",
        média: "Mesmo com medo, eu dou um passo à frente. Sou mais forte do que imagino.",
        alta: "O medo é apenas um sentimento. Eu sou corajoso e protegido."
      },
      gratidão: {
        baixa: "Eu reconheço as bênçãos em minha vida.",
        média: "Meu coração transborda de gratidão por tudo que tenho.",
        alta: "Eu sou gratidão pura. Cada momento é um presente sagrado."
      },
      esperança: {
        baixa: "Eu confio que coisas boas estão por vir.",
        média: "Minha esperança ilumina o caminho à frente.",
        alta: "Eu sou esperança viva. O futuro brilha com possibilidades infinitas."
      },
      paz: {
        baixa: "Eu encontro paz neste momento presente.",
        média: "Paz flui através de mim como água cristalina.",
        alta: "Eu sou paz absoluta. Minha serenidade toca tudo ao meu redor."
      },
      confusão: {
        baixa: "Está tudo bem não saber. Eu confio no processo.",
        média: "A clareza virá no momento certo. Eu me permito não saber.",
        alta: "Na confusão, encontro oportunidade de crescimento. Eu confio em minha sabedoria interior."
      },
      energia: {
        baixa: "Eu canalizo minha energia para o que realmente importa.",
        média: "Minha energia é poderosa e direcionada. Eu crio com propósito.",
        alta: "Eu sou energia pura em movimento. Minha vitalidade transforma o mundo."
      }
    };

    return mantras[emotion]?.[intensity] || mantras.paz.média;
  }
}

export default EmotionalAnalyzer;


