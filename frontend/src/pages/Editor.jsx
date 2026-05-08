import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import ScoreCircle from '../components/ScoreCircle';
import IssueCard from '../components/IssueCard';
import StepGuidance from '../components/StepGuidance';
import OptimizedCode from '../components/OptimizedCode';
import CodeEditor from '../components/CodeEditor';
import { Loader2, Download, Brain, Sparkles, BarChart3 } from 'lucide-react';
import generateReport from '../utils/generateReport';

const Editor = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('javascript');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [analysisMode, setAnalysisMode] = useState('beginner');

  const sampleCode = `function calculate(x,y){
var result
result = x+y
for(i=0;i<100;i++){
console.log(result)
}
return result
}`;

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError("Please paste some code first.");
      return;
    }
    
    setError(null);
    setIsAnalyzing(true);
    setResults(null);
    
    try {
      // Small simulated delay for "ML processing" feel
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const response = await axios.post('http://localhost:5000/api/analyze', {
        code,
        language
      });
      
      setResults(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze code. Please ensure backend servers are running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClear = () => {
    setCode('');
    setResults(null);
    setError(null);
  };

  const handleDownloadPDF = () => {
    if (!results) return;
    generateReport({
      code,
      language,
      results,
      analysisMode,
    });
  };

  return (
    <div className="flex-grow max-w-[1600px] w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col lg:flex-row gap-8">
      
      {/* Left Panel - Code Input */}
      <div className="w-full lg:w-1/2 flex flex-col h-full min-h-[600px]">
        {/* Editor Header */}
        <div className="bg-surface border border-border rounded-t-xl p-4 flex justify-between items-center">
          <h2 className="text-heading font-bold">Code Editor</h2>
          <select 
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-background border border-border text-body rounded-md px-3 py-1.5 focus:outline-none focus:border-primary text-sm"
            id="language-selector"
          >
            <option value="javascript">JavaScript</option>
            <option value="python">Python</option>
            <option value="java">Java</option>
            <option value="c">C</option>
            <option value="cpp">C++</option>
          </select>
        </div>
        
        {/* CodeMirror Editor */}
        <div className="flex-grow relative border-x border-border bg-codebg overflow-hidden min-h-[350px]">
          <CodeEditor
            value={code}
            onChange={setCode}
            language={language}
          />
        </div>
        
        {/* Editor Footer */}
        <div className="bg-surface border border-border rounded-b-xl p-4 flex flex-col gap-3">
          {error && <div className="text-error text-sm bg-error/10 border border-error/20 rounded-lg px-3 py-2">{error}</div>}
          
          {/* Analysis Mode Toggle */}
          <div className="flex items-center justify-center">
            <div className="mode-toggle-track" onClick={() => setAnalysisMode(prev => prev === 'beginner' ? 'advanced' : 'beginner')}>
              <div className={`mode-toggle-slider ${analysisMode === 'advanced' ? 'advanced' : ''}`}></div>
              <span className={`mode-toggle-label ${analysisMode === 'beginner' ? 'text-white' : 'text-body'}`}>
                <span className="flex items-center justify-center gap-1">
                  <Sparkles className="w-3.5 h-3.5" />
                  Beginner
                </span>
              </span>
              <span className={`mode-toggle-label ${analysisMode === 'advanced' ? 'text-white' : 'text-body'}`}>
                <span className="flex items-center justify-center gap-1">
                  <Brain className="w-3.5 h-3.5" />
                  Advanced
                </span>
              </span>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="flex-1 bg-primary text-white font-medium py-3 rounded-lg hover:bg-primary-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
              id="analyze-button"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing your code...
                </>
              ) : (
                'Analyze My Code'
              )}
            </button>
            <button
              onClick={handleClear}
              disabled={isAnalyzing}
              className="px-6 py-3 border border-border rounded-lg text-body hover:text-heading hover:bg-surface-hover transition-colors disabled:opacity-50"
              id="clear-button"
            >
              Clear
            </button>
          </div>
          <div className="text-center">
             <button onClick={() => setCode(sampleCode)} className="text-xs text-primary hover:underline" id="load-sample">Load Sample Issue Code</button>
          </div>
        </div>
      </div>

      {/* Right Panel - Results */}
      <div className="w-full lg:w-1/2 flex flex-col h-full overflow-y-auto pr-2 custom-scrollbar pb-8">
        {!isAnalyzing && !results && (
          <div className="flex-grow flex flex-col items-center justify-center text-body opacity-50 h-full min-h-[400px] border border-dashed border-border rounded-xl">
            <div className="w-16 h-16 mb-4 rounded-full bg-surface flex items-center justify-center">
              <span className="text-2xl">👀</span>
            </div>
            <p>Paste some code and click analyze to see results.</p>
          </div>
        )}

        {isAnalyzing && (
          <div className="flex-grow flex flex-col items-center justify-center h-full min-h-[400px]">
            <div className="relative w-24 h-24">
              <div className="absolute inset-0 border-t-2 border-primary rounded-full animate-spin"></div>
              <div className="absolute inset-2 border-r-2 border-purple-400 rounded-full animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
              <div className="absolute inset-4 border-b-2 border-pink-400 rounded-full animate-spin" style={{ animationDuration: '2s' }}></div>
            </div>
            <p className="mt-6 text-heading font-medium animate-pulse">Running ML Code Analysis...</p>
            <p className="mt-2 text-body text-sm">Parsing AST • Extracting Features • ML Prediction</p>
          </div>
        )}

        <AnimatePresence>
          {results && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="space-y-8"
            >
              {/* Download PDF Button */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
                <button
                  onClick={handleDownloadPDF}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-primary/10 border border-primary/20 rounded-xl text-primary font-medium hover:bg-primary/20 transition-all group"
                  id="download-pdf-button"
                >
                  <Download className="w-5 h-5 group-hover:animate-bounce" />
                  Download PDF Report
                </button>
              </motion.div>

              {/* SECTION A — CODE QUALITY SCORE */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
                <ScoreCircle score={results.score.overall} subScores={results.score} mode={analysisMode} />
              </motion.div>

              {/* SECTION — ML STATS (Advanced Only) */}
              {analysisMode === 'advanced' && results.mlStats && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}>
                  <div className="bg-surface border border-border rounded-xl p-6">
                    <h3 className="text-lg font-bold text-heading mb-4 flex items-center gap-2">
                      <BarChart3 className="w-5 h-5 text-purple-400" />
                      ML Analysis Insights
                    </h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-background rounded-lg p-4 border border-border">
                        <div className="text-xs text-body uppercase tracking-wide mb-1">Structural Quality</div>
                        <div className="text-2xl font-bold text-heading">{results.mlStats.structural_quality_score || 'N/A'}</div>
                      </div>
                      <div className="bg-background rounded-lg p-4 border border-border">
                        <div className="text-xs text-body uppercase tracking-wide mb-1">Anomaly Status</div>
                        <div className={`text-2xl font-bold ${results.mlStats.is_anomalous ? 'text-error' : 'text-success'}`}>
                          {results.mlStats.is_anomalous ? 'Detected' : 'Normal'}
                        </div>
                      </div>
                      <div className="bg-background rounded-lg p-4 border border-border">
                        <div className="text-xs text-body uppercase tracking-wide mb-1">AI-Generated Prob.</div>
                        <div className="text-2xl font-bold text-heading">
                          {results.mlStats.ai_generated_probability 
                            ? `${(results.mlStats.ai_generated_probability * 100).toFixed(0)}%` 
                            : 'N/A'}
                        </div>
                      </div>
                      <div className="bg-background rounded-lg p-4 border border-border">
                        <div className="text-xs text-body uppercase tracking-wide mb-1">AST Nodes</div>
                        <div className="text-sm font-medium text-heading truncate">
                          {results.mlStats.top_nodes?.slice(0, 3).join(', ') || 'N/A'}
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* SECTION B — ISSUES FOUND */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-heading">Issues Detected</h3>
                  <span className="bg-surface px-3 py-1 rounded-full text-sm text-body border border-border">
                    {results.issues.length} found
                  </span>
                </div>
                <div>
                  {results.issues.map((issue, idx) => (
                    <IssueCard key={idx} issue={issue} mode={analysisMode} index={idx} />
                  ))}
                </div>
              </motion.div>

              {/* SECTION C — STEP BY STEP GUIDANCE */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }}>
                <h3 className="text-xl font-bold text-heading mb-4">Improvement Plan</h3>
                <div>
                  {results.steps.map((step, idx) => (
                    <StepGuidance key={idx} step={step} mode={analysisMode} index={idx} />
                  ))}
                </div>
              </motion.div>

              {/* SECTION D — OPTIMIZED CODE */}
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }}>
                <OptimizedCode 
                  optimizedCode={results.optimizedCode} 
                  originalCode={code}
                  language={results.language} 
                  mode={analysisMode}
                />
              </motion.div>

            </motion.div>
          )}
        </AnimatePresence>
      </div>

    </div>
  );
};

export default Editor;
