import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript';
import py from 'react-syntax-highlighter/dist/esm/languages/hljs/python';
import { vs2015 } from 'react-syntax-highlighter/dist/esm/styles/hljs';

SyntaxHighlighter.registerLanguage('javascript', js);
SyntaxHighlighter.registerLanguage('python', py);

const OptimizedCode = ({ optimizedCode, language }) => {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(optimizedCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-surface border border-border rounded-xl overflow-hidden mt-8">
      <button 
        className="w-full px-6 py-4 flex flex-col items-center justify-center hover:bg-[#222] transition-colors focus:outline-none group"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-2 mb-1">
          <h3 className="text-lg font-bold text-heading">View Optimized Code</h3>
          {expanded ? <ChevronUp className="text-body w-5 h-5 group-hover:text-primary transition-colors" /> : <ChevronDown className="text-body w-5 h-5 group-hover:text-primary transition-colors" />}
        </div>
        <p className="text-xs text-body italic">Understand the issues above first — then expand</p>
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
          >
            <div className="p-4 border-t border-border bg-codebg relative">
              <button 
                onClick={handleCopy}
                className="absolute top-6 right-6 p-2 bg-surface hover:bg-[#333] border border-border rounded-md text-body hover:text-heading transition-colors z-10"
                title="Copy Code"
              >
                {copied ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
              </button>
              
              <div className="rounded-lg overflow-hidden border border-border/50">
                <SyntaxHighlighter 
                  language={language} 
                  style={vs2015}
                  customStyle={{ margin: 0, padding: '1.5rem', background: 'transparent' }}
                  showLineNumbers
                >
                  {optimizedCode}
                </SyntaxHighlighter>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default OptimizedCode;
