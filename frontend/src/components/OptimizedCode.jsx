import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Copy, Check, GitCompare, Code } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript';
import py from 'react-syntax-highlighter/dist/esm/languages/hljs/python';
import javaLang from 'react-syntax-highlighter/dist/esm/languages/hljs/java';
import cppLang from 'react-syntax-highlighter/dist/esm/languages/hljs/cpp';
import cLang from 'react-syntax-highlighter/dist/esm/languages/hljs/c';
import { vs2015 } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { githubGist } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { useTheme } from '../context/ThemeContext';
import CodeDiff from './CodeDiff';

// Register all supported languages
SyntaxHighlighter.registerLanguage('javascript', js);
SyntaxHighlighter.registerLanguage('python', py);
SyntaxHighlighter.registerLanguage('java', javaLang);
SyntaxHighlighter.registerLanguage('cpp', cppLang);
SyntaxHighlighter.registerLanguage('c', cLang);

const OptimizedCode = ({ optimizedCode, originalCode, language, mode = 'beginner' }) => {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState('code'); // 'code' | 'diff'
  const { theme } = useTheme();

  const handleCopy = () => {
    navigator.clipboard.writeText(optimizedCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const highlighterStyle = theme === 'dark' ? vs2015 : githubGist;

  return (
    <div className="bg-surface border border-border rounded-xl overflow-hidden mt-8">
      <button 
        className="w-full px-6 py-4 flex flex-col items-center justify-center hover:bg-surface-hover transition-colors focus:outline-none group"
        onClick={() => setExpanded(!expanded)}
        id="optimized-code-toggle"
      >
        <div className="flex items-center gap-2 mb-1">
          <h3 className="text-lg font-bold text-heading">View Optimized Code</h3>
          {expanded 
            ? <ChevronUp className="text-body w-5 h-5 group-hover:text-primary transition-colors" /> 
            : <ChevronDown className="text-body w-5 h-5 group-hover:text-primary transition-colors" />
          }
        </div>
        <p className="text-xs text-body italic">Understand the issues above first — then expand</p>
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            {/* Toolbar */}
            <div className="px-4 py-3 border-t border-border bg-background flex items-center justify-between flex-wrap gap-2">
              {/* View Mode Toggle */}
              <div className="flex items-center bg-surface rounded-lg border border-border overflow-hidden">
                <button
                  onClick={() => setViewMode('code')}
                  className={`flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium transition-colors ${
                    viewMode === 'code' 
                      ? 'bg-primary text-white' 
                      : 'text-body hover:text-heading'
                  }`}
                  id="view-mode-code"
                >
                  <Code className="w-3.5 h-3.5" />
                  Code
                </button>
                <button
                  onClick={() => setViewMode('diff')}
                  className={`flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium transition-colors ${
                    viewMode === 'diff' 
                      ? 'bg-primary text-white' 
                      : 'text-body hover:text-heading'
                  }`}
                  id="view-mode-diff"
                >
                  <GitCompare className="w-3.5 h-3.5" />
                  Before vs After
                </button>
              </div>

              {/* Copy Button */}
              {viewMode === 'code' && (
                <button 
                  onClick={handleCopy}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-surface hover:bg-surface-hover border border-border rounded-lg text-body hover:text-heading transition-colors text-sm"
                  title="Copy Code"
                  id="copy-optimized-code"
                >
                  {copied 
                    ? <><Check className="w-3.5 h-3.5 text-success" /> Copied!</>
                    : <><Copy className="w-3.5 h-3.5" /> Copy</>
                  }
                </button>
              )}
            </div>

            {/* Content */}
            <div className="border-t border-border">
              {viewMode === 'code' ? (
                <div className="p-4 bg-codebg">
                  <div className="rounded-lg overflow-hidden border border-border/50">
                    <SyntaxHighlighter 
                      language={language} 
                      style={highlighterStyle}
                      customStyle={{ margin: 0, padding: '1.5rem', background: 'transparent' }}
                      showLineNumbers
                    >
                      {optimizedCode}
                    </SyntaxHighlighter>
                  </div>
                </div>
              ) : (
                <div className="p-4 bg-codebg">
                  <CodeDiff
                    originalCode={originalCode}
                    optimizedCode={optimizedCode}
                    language={language}
                  />
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default OptimizedCode;
