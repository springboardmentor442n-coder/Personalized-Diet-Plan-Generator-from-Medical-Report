import React from 'react';
import { motion } from 'motion/react';
import { User, Calendar, Hash, Activity } from 'lucide-react';
import { PatientInfo } from '../types';

interface PatientCardProps {
  info: PatientInfo;
}

export const PatientCard: React.FC<PatientCardProps> = ({ info }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="startup-card"
    >
      <div className="flex items-center gap-4 mb-8">
        <div className="w-12 h-12 bg-medical-100 dark:bg-medical-900/30 text-medical-600 dark:text-medical-400 rounded-2xl flex items-center justify-center shadow-inner">
          <User size={24} />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-slate-800 dark:text-white">Patient Information</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">Demographic and report details</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        <InfoItem icon={<User size={18} />} label="Name" value={info.name} />
        <InfoItem icon={<Activity size={18} />} label="Age / Gender" value={`${info.age} / ${info.gender}`} />
        <InfoItem icon={<Hash size={18} />} label="Lab Number" value={info.labNumber} />
        <InfoItem icon={<Calendar size={18} />} label="Collection Date" value={info.collectionDate} />
        <InfoItem icon={<Calendar size={18} />} label="Report Date" value={info.reportDate} />
      </div>
    </motion.div>
  );
};

const InfoItem = ({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) => (
  <div className="flex flex-col gap-2">
    <div className="flex items-center gap-2 text-slate-400 dark:text-slate-500">
      {icon}
      <span className="text-xs font-bold uppercase tracking-widest">{label}</span>
    </div>
    <span className="text-slate-800 dark:text-slate-200 font-semibold text-lg">{value}</span>
  </div>
);
