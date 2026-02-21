import React from 'react';
import { motion } from 'motion/react';
import { CheckCircle2, AlertCircle, Activity } from 'lucide-react';

interface StatsGridProps {
  total: number;
  normal: number;
  abnormal: number;
}

export const StatsGrid: React.FC<StatsGridProps> = ({ total, normal, abnormal }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <StatCard
        icon={<Activity className="text-medical-600" />}
        label="Total Tests"
        value={total}
        color="bg-medical-50"
        delay={0}
      />
      <StatCard
        icon={<CheckCircle2 className="text-emerald-600" />}
        label="Normal Results"
        value={normal}
        color="bg-emerald-50"
        delay={0.1}
      />
      <StatCard
        icon={<AlertCircle className="text-rose-600" />}
        label="Abnormal Results"
        value={abnormal}
        color="bg-rose-50"
        delay={0.2}
      />
    </div>
  );
};

const StatCard = ({ icon, label, value, color, delay }: any) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay }}
    className="startup-card flex items-center gap-5 hover:scale-[1.02] transition-transform duration-300"
  >
    <div className={`w-14 h-14 ${color} dark:bg-opacity-10 rounded-2xl flex items-center justify-center shadow-inner`}>
      {icon}
    </div>
    <div>
      <p className="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-1">{label}</p>
      <p className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">{value}</p>
    </div>
  </motion.div>
);
