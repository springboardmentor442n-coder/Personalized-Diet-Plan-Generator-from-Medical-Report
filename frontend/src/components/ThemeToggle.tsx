import React from 'react';
import { motion } from 'motion/react';
import { Sun, Moon, Plus } from 'lucide-react';

interface ThemeToggleProps {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ theme, toggleTheme }) => {
  const isDark = theme === 'dark';

  return (
    <button
      onClick={toggleTheme}
      className="relative flex items-center w-20 h-10 p-1 bg-slate-200 dark:bg-slate-800 rounded-full transition-colors duration-500 focus:outline-none shadow-inner group"
      aria-label="Toggle theme"
    >
      {/* Track Background Icons */}
      <div className="absolute inset-0 flex justify-between items-center px-2.5 pointer-events-none">
        <Sun size={14} className={`${isDark ? 'text-slate-500' : 'text-amber-500'} transition-colors duration-500`} />
        <Moon size={14} className={`${isDark ? 'text-indigo-400' : 'text-slate-400'} transition-colors duration-500`} />
      </div>

      {/* The "Doctor" Slider Handle */}
      <motion.div
        animate={{ x: isDark ? 40 : 0 }}
        transition={{ type: "spring", stiffness: 400, damping: 30 }}
        className="relative z-10 w-8 h-8 bg-white dark:bg-slate-100 rounded-full shadow-lg flex items-center justify-center overflow-hidden"
      >
        {/* Medical Cross on the handle */}
        <div className="relative w-full h-full flex items-center justify-center">
           <Plus 
            size={18} 
            className={`${isDark ? 'text-medical-600' : 'text-medical-500'} transition-colors duration-500`} 
            strokeWidth={3}
          />
          
          {/* Subtle heartbeat line effect inside handle */}
          <motion.div 
            animate={{ 
              opacity: [0.2, 0.5, 0.2],
              scaleX: [1, 1.2, 1]
            }}
            transition={{ repeat: Infinity, duration: 2 }}
            className="absolute inset-0 flex items-center justify-center pointer-events-none"
          >
            <div className="w-6 h-px bg-medical-500/20" />
          </motion.div>
        </div>
      </motion.div>
      
      {/* Decorative "Pill" text/style */}
      <div className="absolute -top-6 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
        <span className="text-[10px] font-bold uppercase tracking-widest text-medical-600 dark:text-medical-400 bg-medical-50 dark:bg-medical-900/30 px-2 py-0.5 rounded-md border border-medical-100 dark:border-medical-800">
          {isDark ? 'Night Shift' : 'Day Shift'}
        </span>
      </div>
    </button>
  );
};
