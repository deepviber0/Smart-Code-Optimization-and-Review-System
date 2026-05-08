import React from 'react';
import { Network, Server, Cpu, Code2 } from 'lucide-react';

const About = () => {
  return (
    <div className="flex-grow max-w-4xl mx-auto px-4 sm:px-6 py-16">
      <h1 className="text-4xl font-bold text-heading mb-8 text-center">About The Project</h1>
      
      <div className="bg-surface border border-border rounded-xl p-8 mb-12">
        <h2 className="text-2xl font-bold text-heading mb-4">Our Philosophy</h2>
        <p className="text-body text-lg leading-relaxed mb-6">
          Most AI coding assistants give you the answer instantly. While convenient, this creates dependency and bypasses the learning process. 
          <strong className="text-heading"> Smart Code Optimization and Review System</strong> was built with a different philosophy: <em>learning-oriented feedback.</em>
        </p>
        <p className="text-body text-lg leading-relaxed">
          We explain what's wrong, why it matters, and how to fix it before ever showing the solution. This forces understanding, building real engineering skills.
        </p>
      </div>

      <h2 className="text-2xl font-bold text-heading mb-6">Architecture</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-surface border border-border rounded-xl p-6 flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-primary/20 text-primary rounded-full flex items-center justify-center mb-4">
            <Code2 />
          </div>
          <h3 className="font-bold text-heading mb-2">Frontend</h3>
          <p className="text-sm text-body">React.js + Tailwind CSS. Handles UI, animations, and syntax highlighting.</p>
        </div>
        <div className="bg-surface border border-border rounded-xl p-6 flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-success/20 text-success rounded-full flex items-center justify-center mb-4">
            <Server />
          </div>
          <h3 className="font-bold text-heading mb-2">Backend Gateway</h3>
          <p className="text-sm text-body">Node.js + Express. Mediates API traffic securely between frontend and ML engine.</p>
        </div>
        <div className="bg-surface border border-border rounded-xl p-6 flex flex-col items-center text-center">
          <div className="w-12 h-12 bg-purple-500/20 text-purple-400 rounded-full flex items-center justify-center mb-4">
            <Cpu />
          </div>
          <h3 className="font-bold text-heading mb-2">ML/AI Engine</h3>
          <p className="text-sm text-body">Python + Flask + scikit-learn + tree-sitter. Performs structural AST extraction and ML predictions.</p>
        </div>
      </div>

      <div className="bg-surface border border-border rounded-xl p-8 mb-12">
        <h2 className="text-2xl font-bold text-heading mb-6 flex items-center gap-2">
          <Network className="text-primary" /> ML Integration Pipeline
        </h2>
        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded bg-background text-heading flex items-center justify-center font-bold flex-shrink-0 border border-border">1</div>
            <div>
              <h4 className="font-bold text-heading">Tree-sitter AST Extraction</h4>
              <p className="text-body text-sm">Code is parsed into an Abstract Syntax Tree to extract a structural "fingerprint".</p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded bg-background text-heading flex items-center justify-center font-bold flex-shrink-0 border border-border">2</div>
            <div>
              <h4 className="font-bold text-heading">TF-IDF Vectorization</h4>
              <p className="text-body text-sm">Node sequences are converted into high-dimensional feature vectors.</p>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded bg-background text-heading flex items-center justify-center font-bold flex-shrink-0 border border-border">3</div>
            <div>
              <h4 className="font-bold text-heading">Anomaly Detection</h4>
              <p className="text-body text-sm">An Isolation Forest algorithm evaluates how much the structure deviates from standard best practices.</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="text-center pb-8 text-body text-sm">
        <p>Built for the College Mini Project Presentation.</p>
      </div>
    </div>
  );
};

export default About;
