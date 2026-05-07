import React, { useState } from 'react';
import { AlertCircle, AlertTriangle, Info, ChevronDown, ChevronUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const IssueCard = ({ issue }) => {
  const [expanded, setExpanded] = useState(false);

  const getSeverityStyles = (severity) => {
    switch (severity) {
      case 'critical':
        return { border: 'border-l-error', icon: <AlertCircle className="text-error w-5 h-5" />, bg: 'bg-error/10' };
      case 'warning':
        return { border: 'border-l-warning', icon: <AlertTriangle className="text-warning w-5 h-5" />, bg: 'bg-warning/10' };
      case 'info':
      default:
        return { border: 'border-l-primary', icon: <Info className="text-primary w-5 h-5" />, bg: 'bg-primary/10' };
    }
  };

  const styles = getSeverityStyles(issue.severity);

  return (
    <div className={`bg-surface border border-border border-l-4 ${styles.border} rounded-r-xl mb-3 overflow-hidden hover:bg-[#222] transition-colors`}>
      <button 
        className="w-full px-4 py-3 flex items-center justify-between focus:outline-none"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${styles.bg}`}>
            {styles.icon}
          </div>
          <div className="text-left">
            <h4 className="text-heading font-medium text-sm sm:text-base">{issue.title}</h4>
            {issue.line && (
              <span className="text-xs text-body">Line {issue.line}</span>
            )}
          </div>
        </div>
        {expanded ? <ChevronUp className="text-body w-5 h-5" /> : <ChevronDown className="text-body w-5 h-5" />}
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="px-4 pb-4 pt-1"
          >
            <div className="pl-14">
              <p className="text-body text-sm leading-relaxed">{issue.description}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default IssueCard;
