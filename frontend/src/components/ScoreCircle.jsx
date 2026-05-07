import React, { useEffect, useState } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const ScoreCircle = ({ score, subScores }) => {
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

  return (
    <div className="bg-surface border border-border rounded-xl p-6 flex flex-col items-center">
      <h3 className="text-lg font-bold text-heading mb-6 self-start">Code Quality Score</h3>
      
      <div className="w-40 h-40 mb-8">
        <CircularProgressbar
          value={animatedScore}
          text={`${animatedScore}`}
          styles={buildStyles({
            pathTransitionDuration: 1.5,
            pathColor: getColor(animatedScore),
            textColor: '#FFFFFF',
            trailColor: 'rgba(255,255,255,0.05)',
            textSize: '24px',
          })}
        />
      </div>

      <div className="w-full space-y-4">
        <SubScore label="Correctness" value={subScores.correctness} color={getColor(subScores.correctness)} />
        <SubScore label="Performance" value={subScores.performance} color={getColor(subScores.performance)} />
        <SubScore label="Readability" value={subScores.readability} color={getColor(subScores.readability)} />
        <SubScore label="Best Practices" value={subScores.bestPractices} color={getColor(subScores.bestPractices)} />
      </div>
    </div>
  );
};

const SubScore = ({ label, value, color }) => (
  <div>
    <div className="flex justify-between text-sm mb-1">
      <span className="text-body">{label}</span>
      <span className="text-heading font-medium">{value}/100</span>
    </div>
    <div className="w-full bg-[#2A2A2A] rounded-full h-2">
      <div 
        className="h-2 rounded-full transition-all duration-1000 ease-out"
        style={{ width: `${value}%`, backgroundColor: color }}
      ></div>
    </div>
  </div>
);

export default ScoreCircle;
