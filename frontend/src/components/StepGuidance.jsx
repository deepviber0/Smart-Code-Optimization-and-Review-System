import React, { useState } from 'react';
import { HelpCircle, AlertCircle, CheckCircle2, ChevronDown, ChevronUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const StepGuidance = ({ step, mode = 'beginner', index = 0 }) => {
  const [expanded, setExpanded] = useState(index === 0);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-surface border border-border rounded-xl mb-4 relative overflow-hidden"
    >
      {/* Accent Bar */}
      <div className="absolute top-0 left-0 w-1.5 h-full bg-primary"></div>

      {/* Clickable Header */}
      <button 
        className="w-full px-5 py-4 flex items-center justify-between focus:outline-none hover:bg-surface-hover transition-colors"
        onClick={() => setExpanded(!expanded)}
        id={`step-guidance-${index}`}
      >
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold border border-primary/30">
            {step.number}
          </div>
          <div className="text-left">
            <h4 className="text-heading font-medium text-sm sm:text-base">{step.what}</h4>
            {mode === 'beginner' && (
              <p className="text-xs text-body mt-0.5">Click to see how to fix this</p>
            )}
          </div>
        </div>
        {expanded 
          ? <ChevronUp className="text-body w-5 h-5 flex-shrink-0" /> 
          : <ChevronDown className="text-body w-5 h-5 flex-shrink-0" />
        }
      </button>

      {/* Expandable Content */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-5 pt-1">
              <div className="flex-grow space-y-4 pl-12">
                {/* What to fix */}
                <div>
                  <h4 className="text-heading font-medium flex items-center gap-2 mb-1 text-sm">
                    <AlertCircle className="w-4 h-4 text-warning" /> 
                    What to fix
                  </h4>
                  <p className="text-body text-sm bg-background p-3 rounded-md border border-border">
                    {step.what}
                  </p>
                </div>
                
                {/* Why it matters - Advanced only */}
                {mode === 'advanced' && (
                  <div>
                    <h4 className="text-heading font-medium flex items-center gap-2 mb-1 text-sm">
                      <HelpCircle className="w-4 h-4 text-purple-400" /> 
                      Why it matters
                    </h4>
                    <p className="text-body text-sm bg-background p-3 rounded-md border border-border">
                      {step.why}
                    </p>
                  </div>
                )}
                
                {/* How to fix */}
                <div>
                  <h4 className="text-heading font-medium flex items-center gap-2 mb-1 text-sm">
                    <CheckCircle2 className="w-4 h-4 text-success" /> 
                    How to fix it
                  </h4>
                  <p className="text-body text-sm bg-background p-3 rounded-md border border-border">
                    {step.how}
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default StepGuidance;
