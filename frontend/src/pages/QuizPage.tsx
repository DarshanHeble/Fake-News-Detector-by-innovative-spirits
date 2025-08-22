import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const questions = [
  {
    question: "Which of the following is a sign of fake news?",
    options: [
      "Sensational headlines with excessive punctuation!!!",
      "Citations from verified experts",
      "Links to official sources",
      "Recent publication dates",
    ],
    answer: 0,
    explanation:
      "Excessive punctuation and sensational headlines are common clickbait tactics used in fake news.",
  },
  {
    question:
      "You receive a WhatsApp message about a health emergency. What should you do first?",
    options: [
      "Forward it to all your contacts immediately",
      "Check official health websites for verification",
      "Delete it without reading",
      "Ask the sender for their source",
    ],
    answer: 1,
    explanation:
      "Always verify health-related claims with official sources before sharing.",
  },
  {
    question:
      "A friend shares a political news article on social media. What's the best first step?",
    options: [
      "Share it if you agree with the viewpoint",
      "Check the article's date and source",
      "Comment your opinion immediately",
      "Ignore it completely",
    ],
    answer: 1,
    explanation:
      "Checking the date and source helps verify the article's credibility.",
  },
  {
    question: "Which social media behavior suggests potential fake news?",
    options: [
      "Posts with verified badges",
      "Content from official accounts",
      "Posts demanding immediate sharing",
      "Articles with multiple sources cited",
    ],
    answer: 2,
    explanation:
      "Urgency in sharing is often a tactic used to spread misinformation before fact-checking can occur.",
  },
  {
    question: "What's a red flag in messaging apps regarding news?",
    options: [
      "Messages with official website links",
      "Content with verifiable statistics",
      "Messages claiming to be 'banned' information",
      "Updates from government channels",
    ],
    answer: 2,
    explanation:
      "Claims of 'banned' or 'hidden' information often indicate potential misinformation.",
  },
  {
    question: "How can you verify a viral video's authenticity?",
    options: [
      "Accept it if it looks professional",
      "Trust if many people shared it",
      "Use reverse image/video search tools",
      "Believe if it's emotionally moving",
    ],
    answer: 2,
    explanation:
      "Reverse search tools can help find the original source and context of videos.",
  },
];

const QuizPage = () => {
  const [current, setCurrent] = useState(0);
  const [score, setScore] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [selected, setSelected] = useState<number | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);

  const handleOption = (idx: number) => {
    if (selected !== null) return;
    setSelected(idx);
    if (questions[current].answer === idx) setScore((s) => s + 1);
    setShowExplanation(true);

    setTimeout(() => {
      setShowExplanation(false);
      setSelected(null);
      if (current + 1 < questions.length) {
        setCurrent((c) => c + 1);
      } else {
        setShowResult(true);
      }
    }, 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="quiz-container"
      style={{
        maxWidth: 600,
        margin: "48px auto",
        padding: "32px 24px",
        background: "#ffffff",
        borderRadius: 20,
        boxShadow: "0 8px 32px rgba(0,0,0,0.1)",
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      <h2
        style={{
          textAlign: "center",
          color: "#ff9800",
          fontWeight: 800,
          fontSize: "2rem",
          letterSpacing: "0.5px",
          marginBottom: 8,
        }}
      >
        🧠 Fake News IQ Quiz
      </h2>
      <div
        style={{
          textAlign: "center",
          color: "#222",
          fontSize: "1.08rem",
          marginBottom: 18,
          opacity: 0.8,
        }}
      >
        Test your knowledge and become a Fake News Detective!
      </div>
      {!showResult ? (
        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {/* Question display */}
            <div className="question-container">
              {/* Progress bar */}
              <div
                style={{
                  width: "100%",
                  height: 4,
                  background: "#f0f0f0",
                  borderRadius: 2,
                  marginBottom: 24,
                }}
              >
                <motion.div
                  initial={{ width: 0 }}
                  animate={{
                    width: `${((current + 1) / questions.length) * 100}%`,
                  }}
                  style={{
                    height: "100%",
                    background: "linear-gradient(90deg, #4CAF50, #81C784)",
                    borderRadius: 2,
                  }}
                />
              </div>

              {/* Question */}
              <h3 style={{ color: "#2c3e50", marginBottom: 24 }}>
                {questions[current].question}
              </h3>

              {/* Options */}
              <div className="options-container">
                {questions[current].options.map((opt, idx) => (
                  <motion.button
                    key={idx}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleOption(idx)}
                    disabled={selected !== null}
                    style={{
                      width: "100%",
                      padding: "16px",
                      margin: "8px 0",
                      border: "2px solid #e0e0e0",
                      borderRadius: 12,
                      background:
                        selected === idx
                          ? idx === questions[current].answer
                            ? "#e8f5e9"
                            : "#ffebee"
                          : "#ffffff",
                      cursor: selected === null ? "pointer" : "default",
                      transition: "all 0.2s",
                      textAlign: "left",
                      fontSize: "1rem",
                      color: "#333",
                    }}
                  >
                    {opt}
                  </motion.button>
                ))}
              </div>

              {/* Explanation */}
              <AnimatePresence>
                {showExplanation && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    style={{
                      padding: 16,
                      background: "#f8f9fa",
                      borderRadius: 12,
                      marginTop: 16,
                      color: "#495057",
                    }}
                  >
                    {questions[current].explanation}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </AnimatePresence>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="results-container"
        >
          <div style={{ textAlign: "center", marginTop: 32 }}>
            <h2 style={{ color: "#2c3e50", marginBottom: 16 }}>
              Your Score: {score} / {questions.length}
            </h2>
            <p style={{ color: "#666", marginBottom: 24 }}>
              {score === questions.length
                ? "🏆 Amazing! You're a Fake News Detection Expert!"
                : score >= questions.length * 0.7
                ? "👍 Great job! You're well-equipped to spot fake news."
                : "📚 Keep learning! Practice makes perfect."}
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                setCurrent(0);
                setScore(0);
                setShowResult(false);
              }}
              style={{
                padding: "12px 32px",
                background: "linear-gradient(135deg, #4CAF50, #81C784)",
                color: "white",
                border: "none",
                borderRadius: 12,
                fontSize: "1.1rem",
                cursor: "pointer",
                boxShadow: "0 4px 12px rgba(76, 175, 80, 0.2)",
              }}
            >
              Try Again
            </motion.button>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default QuizPage;
