import React from 'react';
import { motion } from 'motion/react';

interface HealthScoreProps {
  score: number;
}

export const HealthScore: React.FC<HealthScoreProps> = ({ score }) => {
  const radius = 75;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = (s: number) => {
    if (s >= 80) return '#10b981'; // Green
    if (s >= 60) return '#f59e0b'; // Yellow
    if (s >= 40) return '#f97316'; // Orange
    return '#ef4444'; // Red
  };

  const getStatus = (s: number) => {
    if (s >= 80) return 'Excellent';
    if (s >= 60) return 'Good';
    if (s >= 40) return 'Fair';
    return 'Critical';
  };

  const color = getColor(score);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="startup-card flex flex-col items-center justify-center text-center"
    >
      <h3 className="text-xl font-bold text-slate-800 dark:text-white mb-8">Overall Health Score</h3>
      
      <div className="relative inline-flex items-center justify-center">
        <svg className="w-56 h-56 transform -rotate-90">
          {/* Background Circle */}
          <circle
            cx="112"
            cy="112"
            r={radius}
            stroke="currentColor"
            strokeWidth="14"
            fill="transparent"
            className="text-slate-100 dark:text-slate-800"
          />
          {/* Progress Circle */}
          <motion.circle
            cx="112"
            cy="112"
            r={radius}
            stroke={color}
            strokeWidth="14"
            fill="transparent"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            strokeLinecap="round"
          />
        </svg>
        
        <div className="absolute flex flex-col items-center">
          <motion.span 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-6xl font-extrabold text-slate-900 dark:text-white tracking-tighter"
          >
            {score}
          </motion.span>
          <span className="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em]">Points</span>
        </div>
      </div>

      <div className="mt-10">
        <span 
          className="px-6 py-2 rounded-2xl text-sm font-bold shadow-sm border"
          style={{ 
            backgroundColor: `${color}10`, 
            color: color,
            borderColor: `${color}20`
          }}
        >
          {getStatus(score)} Condition
        </span>
      </div>
    </motion.div>
  );
};
