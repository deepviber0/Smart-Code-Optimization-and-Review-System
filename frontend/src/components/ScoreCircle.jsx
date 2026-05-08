import React, { useEffect, useState } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const ScoreCircle = ({ score, subScores, mode = 'beginner' }) => {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    // Animate score from 0 to target
    const timeout = setTimeout(() => {
      setAnimatedScore(score);
    }, 100);
    return () => clearTimeout(timeout);
  }, [score]);

  const getColor = (val) => {
    if (val >= 80) return '#22C55E'; // Success
    if (val >= 50) return '#F59E0B'; // Warning
    return '#EF4444'; // Error
  };

  const getLabel = (val) => {
    if (val >= 90) return 'Excellent';
    if (val >= 80) return 'Great';
    if (val >= 70) return 'Good';
    if (val >= 50) return 'Needs Work';
    return 'Poor';
  };

  const getEncouragement = (val) => {
    if (val >= 90) return "Outstanding work! Your code follows best practices exceptionally well. 🌟";
    if (val >= 80) return "Great job! Just a few minor improvements could make this even better. 💪";
    if (val >= 70) return "Good foundation! Review the suggestions below to level up. 📈";
    if (val >= 50) return "There's room for improvement. The feedback below will help you learn. 📚";
    return "Let's work through the issues together. Every fix teaches something new! 🚀";
  };

  const getTrendIcon = (val) => {
    if (val >= 70) return <TrendingUp className="w-4 h-4 text-success" />;
    if (val >= 50) return <Minus className="w-4 h-4 text-warning" />;
    return <TrendingDown className="w-4 h-4 text-error" />;
  };

  return (
    <div className="bg-surface border border-border rounded-xl p-6 flex flex-col items-center">
      <h3 className="text-lg font-bold text-heading mb-6 self-start">Code Quality Score</h3>
      
      {/* Score Circle */}
      <div className="w-40 h-40 mb-4">
        <CircularProgressbar
          value={animatedScore}
          text={`${animatedScore}`}
          styles={buildStyles({
            pathTransitionDuration: 1.5,
            pathColor: getColor(animatedScore),
            textColor: 'var(--color-heading)',
            trailColor: 'var(--color-border)',
            textSize: '24px',
          })}
        />
      </div>

      {/* Score Label */}
      <div className="flex items-center gap-2 mb-2">
        <span 
          className="text-lg font-bold"
          style={{ color: getColor(animatedScore) }}
        >
          {getLabel(animatedScore)}
        </span>
        {getTrendIcon(animatedScore)}
      </div>

      {/* Encouragement (Both modes) */}
      <p className="text-body text-sm text-center mb-6 px-4 leading-relaxed">
        {getEncouragement(animatedScore)}
      </p>

      {/* Sub-scores - Advanced mode only */}
      {mode === 'advanced' && (
        <div className="w-full space-y-4 pt-4 border-t border-border">
          <SubScore label="Correctness" value={subScores.correctness} color={getColor(subScores.correctness)} />
          <SubScore label="Performance" value={subScores.performance} color={getColor(subScores.performance)} />
          <SubScore label="Readability" value={subScores.readability} color={getColor(subScores.readability)} />
          <SubScore label="Best Practices" value={subScores.bestPractices} color={getColor(subScores.bestPractices)} />
        </div>
      )}

      {/* Beginner mode hint */}
      {mode === 'beginner' && (
        <div className="text-xs text-muted text-center mt-2">
          Switch to Advanced mode to see detailed sub-scores
        </div>
      )}
    </div>
  );
};

const SubScore = ({ label, value, color }) => (
  <div>
    <div className="flex justify-between text-sm mb-1">
      <span className="text-body">{label}</span>
      <span className="text-heading font-medium">{value}/100</span>
    </div>
    <div className="w-full bg-border rounded-full h-2">
      <div 
        className="h-2 rounded-full transition-all duration-1000 ease-out"
        style={{ width: `${value}%`, backgroundColor: color }}
      ></div>
    </div>
  </div>
);

export default ScoreCircle;
