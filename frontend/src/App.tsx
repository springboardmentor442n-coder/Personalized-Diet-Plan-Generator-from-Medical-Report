import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Activity, RefreshCw, ChevronLeft, Download, Share2, Sun, Moon } from 'lucide-react';
import { FileUpload } from './components/FileUpload';
import { PatientCard } from './components/PatientCard';
import { HealthScore } from './components/HealthScore';
import { StatsGrid } from './components/StatsGrid';
import { AbnormalTable } from './components/AbnormalTable';
import { LabReport } from './types';
import { ThemeToggle } from './components/ThemeToggle';

export default function App() {
  const [report, setReport] = useState<LabReport | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') as 'light' | 'dark' || 'light';
    }
    return 'light';
  });

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleFileSelect = async (file: File) => {
  setIsLoading(true);
  setError(null);

  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/analyze/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();
    setReport(data);
  } catch (err) {
    console.error(err);
    setError("Failed to analyze the report. Backend connection failed.");
  } finally {
    setIsLoading(false);
  }
};

  const reset = () => {
    setReport(null);
    setError(null);
  };

  return (
    <div className="min-h-screen transition-colors duration-300 bg-dot-pattern">
      {/* Header */}
      <header className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 medical-gradient rounded-xl flex items-center justify-center text-white shadow-lg shadow-medical-500/20">
              <Activity size={24} />
            </div>
            <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">
              AI <span className="text-medical-600">Nutricare</span>
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            {report && (
              <div className="hidden md:flex items-center gap-2 mr-4">
                <button className="p-2.5 text-slate-400 hover:text-medical-600 dark:hover:text-medical-400 transition-colors rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800">
                  <Share2 size={20} />
                </button>
                <button className="p-2.5 text-slate-400 hover:text-medical-600 dark:hover:text-medical-400 transition-colors rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800">
                  <Download size={20} />
                </button>
                <div className="h-6 w-px bg-slate-200 dark:bg-slate-800 mx-2" />
                <button 
                  onClick={reset}
                  className="flex items-center gap-2 px-5 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-sm font-bold transition-all"
                >
                  <RefreshCw size={16} />
                  New Analysis
                </button>
              </div>
            )}

            <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 pt-12 pb-24">
        <AnimatePresence mode="wait">
          {!report ? (
            <motion.div
              key="upload-view"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="max-w-4xl mx-auto"
            >
              <div className="text-center mb-16">
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="inline-block px-4 py-1.5 mb-6 bg-medical-50 dark:bg-medical-900/30 text-medical-600 dark:text-medical-400 rounded-full text-xs font-bold tracking-widest uppercase border border-medical-100 dark:border-medical-800"
                >
                  Next-Gen Health Intelligence
                </motion.div>
                <h2 className="text-5xl md:text-6xl font-extrabold text-slate-900 dark:text-white mb-6 leading-tight">
                  Understand Your Health <br />
                  <span className="text-transparent bg-clip-text medical-gradient">With Precision AI</span>
                </h2>
                <p className="text-xl text-slate-500 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
                  Upload your medical lab reports and get instant, easy-to-understand insights, 
                  health scores, and detailed analysis of your biomarkers.
                </p>
              </div>

              <FileUpload onFileSelect={handleFileSelect} isLoading={isLoading} />

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-8 p-5 bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-900/30 rounded-2xl text-red-600 dark:text-red-400 text-center text-sm font-semibold shadow-sm"
                >
                  {error}
                </motion.div>
              )}

              <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8">
                <FeatureCard 
                  title="Smart Analysis" 
                  desc="AI-powered extraction of complex medical data into simple, actionable terms."
                />
                <FeatureCard 
                  title="Health Scoring" 
                  desc="Get an overall score based on your test results and clinical ranges."
                />
                <FeatureCard 
                  title="Trend Tracking" 
                  desc="Identify critical biomarkers that need immediate medical attention."
                />
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="dashboard-view"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-8"
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-4">
                <div className="flex items-center gap-4">
                  <button 
                    onClick={reset}
                    className="p-3 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-2xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-all border border-slate-200 dark:border-slate-800 shadow-sm"
                  >
                    <ChevronLeft size={24} />
                  </button>
                  <div>
                    <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white">Report Dashboard</h2>
                    <p className="text-slate-500 dark:text-slate-400">Analysis completed successfully</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Patient Info & Stats */}
                <div className="lg:col-span-2 space-y-8">
                  <PatientCard info={report.patientInfo} />
                  <StatsGrid 
                    total={report.summary.totalTests} 
                    normal={report.summary.normalTests} 
                    abnormal={report.summary.abnormalTests} 
                  />
                  <AbnormalTable findings={report.findings} />
                </div>

                {/* Right Column: Health Score & Summary */}
                <div className="space-y-8">
                  <HealthScore score={report.healthScore} />
                  
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

const FeatureCard = ({ title, desc }: { title: string; desc: string }) => (
  <div className="p-8 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/60 dark:border-slate-800/60 shadow-startup hover:shadow-startup-hover transition-all duration-300">
    <div className="w-12 h-12 bg-medical-50 dark:bg-medical-900/30 text-medical-600 dark:text-medical-400 rounded-xl flex items-center justify-center mb-6">
      <Activity size={24} />
    </div>
    <h4 className="text-xl font-bold text-slate-800 dark:text-white mb-3">{title}</h4>
    <p className="text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</p>
  </div>
);
