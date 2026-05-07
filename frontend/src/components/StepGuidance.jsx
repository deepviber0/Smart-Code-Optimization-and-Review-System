import React from 'react';
import { HelpCircle, AlertCircle, CheckCircle2 } from 'lucide-react';

const StepGuidance = ({ step }) => {
  return (
    <div className="bg-surface border border-border rounded-xl p-5 mb-4 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-1.5 h-full bg-primary"></div>
      
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold border border-primary/30">
          {step.number}
        </div>
        
        <div className="flex-grow space-y-4">
          <div>
            <h4 className="text-heading font-medium flex items-center gap-2 mb-1">
              <AlertCircle className="w-4 h-4 text-warning" /> 
              What to fix
            </h4>
            <p className="text-body text-sm bg-background p-3 rounded-md border border-border">
              {step.what}
            </p>
          </div>
          
          <div>
            <h4 className="text-heading font-medium flex items-center gap-2 mb-1">
              <HelpCircle className="w-4 h-4 text-purple-400" /> 
              Why it matters
            </h4>
            <p className="text-body text-sm bg-background p-3 rounded-md border border-border">
              {step.why}
            </p>
          </div>
          
          <div>
            <h4 className="text-heading font-medium flex items-center gap-2 mb-1">
              <CheckCircle2 className="w-4 h-4 text-success" /> 
              How to fix it
            </h4>
            <p className="text-body text-sm bg-background p-3 rounded-md border border-border">
              {step.how}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StepGuidance;
