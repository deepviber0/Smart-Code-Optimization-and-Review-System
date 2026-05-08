import React, { useState } from 'react';
import { AlertCircle, AlertTriangle, Info, ChevronDown, ChevronUp, Lightbulb, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const IssueCard = ({ issue, mode = 'beginner', index = 0 }) => {
  const [expanded, setExpanded] = useState(mode === 'beginner' && index === 0);

  const getSeverityStyles = (severity) => {
    switch (severity) {
      case 'critical':
        return { 
          border: 'border-l-error', 
          icon: <AlertCircle className="text-error w-5 h-5" />, 
          bg: 'bg-error/10',
          badge: 'bg-error/15 text-error border-error/20',
          label: 'Critical'
        };
      case 'warning':
        return { 
          border: 'border-l-warning', 
          icon: <AlertTriangle className="text-warning w-5 h-5" />, 
          bg: 'bg-warning/10',
          badge: 'bg-warning/15 text-warning border-warning/20',
          label: 'Warning'
        };
      case 'info':
      default:
        return { 
          border: 'border-l-primary', 
          icon: <Info className="text-primary w-5 h-5" />, 
          bg: 'bg-primary/10',
          badge: 'bg-primary/15 text-primary border-primary/20',
          label: 'Info'
        };
    }
  };

  const styles = getSeverityStyles(issue.severity);

  // Simplify description for beginner mode
  const getDescription = () => {
    if (mode === 'beginner' && issue.description) {
      // Truncate overly technical descriptions
      const desc = issue.description;
      if (desc.length > 150) {
        return desc.substring(0, 150) + '...';
      }
      return desc;
    }
    return issue.description;
  };

  return (
    <motion.div 
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`bg-surface border border-border border-l-4 ${styles.border} rounded-r-xl mb-3 overflow-hidden hover:bg-surface-hover transition-colors`}
    >
      <button 
        className="w-full px-4 py-3 flex items-center justify-between focus:outline-none"
        onClick={() => setExpanded(!expanded)}
        id={`issue-card-${index}`}
      >
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${styles.bg}`}>
            {styles.icon}
          </div>
          <div className="text-left">
            <h4 className="text-heading font-medium text-sm sm:text-base">{issue.title}</h4>
            <div className="flex items-center gap-2 mt-0.5">
              {mode === 'advanced' && (
                <span className={`text-[10px] px-2 py-0.5 rounded-full border font-semibold uppercase tracking-wide ${styles.badge}`}>
                  {styles.label}
                </span>
              )}
              {issue.line && (
                <span className="text-xs text-body">Line {issue.line}</span>
              )}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {expanded 
            ? <ChevronUp className="text-body w-5 h-5" /> 
            : <ChevronDown className="text-body w-5 h-5" />
          }
        </div>
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 pt-1">
              <div className="pl-14 space-y-3">
                {/* Description */}
                <p className="text-body text-sm leading-relaxed">{getDescription()}</p>
                
                {/* Beginner Tip */}
                {mode === 'beginner' && (
                  <div className="flex items-start gap-2 bg-warning/5 border border-warning/15 rounded-lg p-3">
                    <Lightbulb className="w-4 h-4 text-warning mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-body">
                      <span className="text-warning font-medium">Tip: </span>
                      {issue.severity === 'critical' 
                        ? 'This is a significant issue that should be fixed first for your code to work correctly.'
                        : issue.severity === 'warning'
                        ? 'Fixing this will make your code cleaner and more efficient.'
                        : 'This is a helpful suggestion to improve your coding style.'
                      }
                    </p>
                  </div>
                )}

                {/* Advanced: Technical Details */}
                {mode === 'advanced' && (
                  <div className="flex items-start gap-2 bg-primary/5 border border-primary/15 rounded-lg p-3">
                    <Zap className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                    <div className="text-sm">
                      <span className="text-primary font-medium">Impact: </span>
                      <span className="text-body">
                        {issue.severity === 'critical'
                          ? 'This issue can cause runtime errors, unexpected behavior, or security vulnerabilities. Immediate attention required.'
                          : issue.severity === 'warning'
                          ? 'May impact performance, maintainability, or could lead to bugs in edge cases.'
                          : 'Addresses code quality, readability, or adherence to best practices.'
                        }
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default IssueCard;
