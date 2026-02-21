import React from 'react';
import { motion } from 'motion/react';
import { AlertTriangle, ArrowUp, ArrowDown, Minus } from 'lucide-react';
import { LabTest, Severity } from '../types';

interface AbnormalTableProps {
  findings: LabTest[];
}

export const AbnormalTable: React.FC<AbnormalTableProps> = ({ findings }) => {
  const abnormalOnly = findings.filter(f => f.severity !== "Normal");

  const getSeverityStyles = (severity: Severity) => {
    switch (severity) {
      case "Mild": return "bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 border-amber-100 dark:border-amber-900/30";
      case "Moderate": return "bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-400 border-orange-100 dark:border-orange-900/30";
      case "Critical": return "bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 border-red-100 dark:border-red-900/30";
      default: return "bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 border-emerald-100 dark:border-emerald-900/30";
    }
  };

  const getInterpretationIcon = (interp: string) => {
    if (interp === "High") return <ArrowUp size={14} className="text-red-500" />;
    if (interp === "Low") return <ArrowDown size={14} className="text-blue-500" />;
    return <Minus size={14} className="text-slate-400" />;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="startup-card"
      //className="bg-white dark:bg-slate-900 rounded-3xl shadow-startup border border-slate-200/60 dark:border-slate-800/60 overflow-hidden"
    >
      <div className="p-8 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400 rounded-2xl flex items-center justify-center shadow-inner">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-800 dark:text-white">Abnormal Findings</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">Tests requiring clinical attention</p>
          </div>
        </div>
        <span className="px-4 py-1.5 bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400 text-xs font-bold rounded-xl border border-rose-100 dark:border-rose-900/30">
          {abnormalOnly.length} Issues Found
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/50 dark:bg-slate-800/50">
              <th className="px-8 py-5 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.15em]">Test Name</th>
              <th className="px-8 py-5 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.15em]">Value</th>
              <th className="px-8 py-5 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.15em]">Reference Range</th>
              <th className="px-8 py-5 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.15em]">Status</th>
              <th className="px-8 py-5 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.15em]">Severity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {abnormalOnly.length > 0 ? (
              abnormalOnly.map((test, idx) => (
                <motion.tr
                  key={idx}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.1 * idx }}
                  className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors"
                >
                  <td className="px-8 py-6">
                    <span className="font-bold text-slate-800 dark:text-slate-200">{test.name}</span>
                  </td>
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-2">
                      <span className="font-extrabold text-slate-900 dark:text-white text-lg">{test.value}</span>
                      <span className="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase">{test.unit}</span>
                    </div>
                  </td>
                  <td className="px-8 py-6 text-sm font-medium text-slate-500 dark:text-slate-400">
                    {test.referenceRange}
                  </td>
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-2">
                      <div className={`p-1 rounded-md ${test.interpretation === 'High' ? 'bg-red-50 dark:bg-red-900/20' : 'bg-blue-50 dark:bg-blue-900/20'}`}>
                        {getInterpretationIcon(test.interpretation)}
                      </div>
                      <span className={`text-sm font-bold ${test.interpretation === 'High' ? 'text-red-600 dark:text-red-400' : 'text-blue-600 dark:text-blue-400'}`}>
                        {test.interpretation}
                      </span>
                    </div>
                  </td>
                  <td className="px-8 py-6">
                    <span className={`px-4 py-1.5 rounded-xl text-xs font-bold border ${getSeverityStyles(test.severity)}`}>
                      {test.severity}
                    </span>
                  </td>
                </motion.tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="px-8 py-20 text-center text-slate-400 dark:text-slate-600 italic font-medium">
                  No abnormal findings detected. All tests are within normal range.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
};
