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
          <div className="flex flex-col gap-3">
            <SubScore 
              label="Syntax & Safety" 
              value={subScores.breakdown?.syntax_safety || 0} 
              total={25} 
              color="#3B82F6" 
            />
            <SubScore 
              label="Readability" 
              value={subScores.breakdown?.readability || 0} 
              total={20} 
              color="#A855F7" 
            />
            <SubScore 
              label="Performance" 
              value={subScores.breakdown?.performance || 0} 
              total={20} 
              color="#F59E0B" 
            />
            <SubScore 
              label="Best Practices" 
              value={subScores.breakdown?.best_practices || 0} 
              total={20} 
              color="#EC4899" 
            />
            <SubScore 
              label="Structural Design" 
              value={subScores.breakdown?.structure || 0} 
              total={15} 
              color="#14B8A6" 
            />
          </div>

          {subScores.deductions?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-border/50">
              <h4 className="text-[10px] uppercase tracking-widest text-body font-bold mb-2">Main Points Deducted</h4>
              <ul className="space-y-1.5">
                {subScores.deductions.slice(0, 5).map((d, i) => (
                  <li key={i} className="text-xs text-error/80 flex items-start gap-1.5">
                    <span className="mt-1 w-1 h-1 rounded-full bg-error shrink-0"></span>
                    <span>{d}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Beginner mode hint */}
      {mode === 'beginner' && (
        <div className="text-xs text-muted text-center mt-2">
          Switch to Advanced mode to see score breakdown
        </div>
      )}
    </div>
  );
};

const SubScore = ({ label, value, total, color }) => {
  const percentage = (value / total) * 100;
  return (
    <div>
      <div className="flex justify-between text-[11px] mb-1">
        <span className="text-body font-medium">{label}</span>
        <span className="text-heading font-bold">{value}/{total}</span>
      </div>
      <div className="w-full bg-border/50 rounded-full h-1.5">
        <div 
          className="h-1.5 rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${percentage}%`, backgroundColor: color }}
        ></div>
      </div>
    </div>
  );
};

export default ScoreCircle;
