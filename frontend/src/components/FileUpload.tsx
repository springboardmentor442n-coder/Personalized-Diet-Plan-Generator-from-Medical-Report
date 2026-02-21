import React from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, isLoading }) => {
  const [file, setFile] = React.useState<File | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    multiple: false,
    disabled: isLoading,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles && acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
        onFileSelect(acceptedFiles[0]);
      }
    },
  } as any);

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    setFile(null);
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={cn(
          "relative group cursor-pointer transition-all duration-500",
          "border-2 border-dashed rounded-[2.5rem] p-16 text-center",
          isDragActive 
            ? "border-medical-500 bg-medical-50/50 dark:bg-medical-900/10" 
            : "border-slate-200 dark:border-slate-800 hover:border-medical-400 dark:hover:border-medical-500 bg-white dark:bg-slate-900/50 hover:bg-slate-50 dark:hover:bg-slate-900",
          isLoading && "opacity-50 cursor-not-allowed",
          "shadow-startup hover:shadow-startup-hover"
        )}
      >
        <input {...getInputProps()} />
        
        <AnimatePresence mode="wait">
          {!file ? (
            <motion.div
              key="upload-prompt"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col items-center"
            >
              <div className="w-20 h-20 bg-medical-100 dark:bg-medical-900/30 text-medical-600 dark:text-medical-400 rounded-3xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-500 shadow-lg shadow-medical-500/10">
                <Upload size={36} />
              </div>
              <h3 className="text-2xl font-bold text-slate-800 dark:text-white mb-3">Upload Lab Report</h3>
              <p className="text-slate-500 dark:text-slate-400 max-w-xs mx-auto leading-relaxed">
                Drag and drop your PDF medical report here, or click to browse files
              </p>
              <div className="mt-8 px-5 py-2.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm font-bold text-slate-600 dark:text-slate-300 shadow-sm">
                Supported format: PDF
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="file-selected"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col items-center"
            >
              <div className="w-20 h-20 bg-medical-600 text-white rounded-3xl flex items-center justify-center mb-6 shadow-2xl shadow-medical-500/30">
                <FileText size={36} />
              </div>
              <h3 className="text-xl font-bold text-slate-800 dark:text-white mb-2 truncate max-w-xs">{file.name}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mb-6 font-medium">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              
              {!isLoading && (
                <button
                  onClick={removeFile}
                  className="px-6 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-red-50 dark:hover:bg-red-900/20 text-slate-500 hover:text-red-500 transition-all rounded-xl font-bold text-sm"
                >
                  Remove File
                </button>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {isLoading && (
          <div className="absolute inset-0 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-[2.5rem] flex flex-col items-center justify-center z-20">
            <div className="w-16 h-16 border-4 border-medical-200 dark:border-medical-900 border-t-medical-600 rounded-full animate-spin mb-6"></div>
            <p className="text-medical-700 dark:text-medical-400 font-bold text-lg animate-pulse tracking-tight">Analyzing Your Report...</p>
          </div>
        )}
      </div>
    </div>
  );
};
