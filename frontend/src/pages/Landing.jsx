import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Activity, ShieldAlert, FileSearch, HelpCircle, CheckCircle, Brain } from 'lucide-react';

const Landing = () => {
  return (
    <div className="flex-grow">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-24 pb-32">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
              Stop Copying AI Code.<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-400">
                Start Understanding It.
              </span>
            </h1>
            <p className="mt-4 text-xl md:text-2xl text-body max-w-3xl mx-auto mb-10">
              Paste your code and get learning-oriented feedback powered by Machine Learning — not just the fixed version.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/editor"
                className="px-8 py-4 rounded-lg bg-primary text-white font-bold text-lg hover:bg-indigo-600 transition-all shadow-[0_0_20px_rgba(99,102,241,0.3)] hover:shadow-[0_0_30px_rgba(99,102,241,0.5)]"
              >
                Try It Now
              </Link>
              <a
                href="#how-it-works"
                className="px-8 py-4 rounded-lg bg-surface border border-border text-heading font-bold text-lg hover:bg-white/5 transition-all"
              >
                See How It Works
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-surface border-y border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Intelligent Code Review</h2>
            <p className="text-body text-lg max-w-2xl mx-auto">
              Our ML-powered engine analyzes your code's structure and semantics to provide deep insights.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard 
              icon={<ShieldAlert className="w-8 h-8 text-error" />}
              title="Code Analysis"
              description="Detects bugs, bad practices, and logical errors instantly using advanced heuristics."
            />
            <FeatureCard 
              icon={<Activity className="w-8 h-8 text-warning" />}
              title="Performance Check"
              description="Identifies slow or inefficient code patterns that could bottleneck your application."
            />
            <FeatureCard 
              icon={<FileSearch className="w-8 h-8 text-primary" />}
              title="Readability Score"
              description="Rates how clean and readable your code is, helping you write maintainable software."
            />
            <FeatureCard 
              icon={<HelpCircle className="w-8 h-8 text-purple-400" />}
              title="Step-by-Step Guidance"
              description="Explains issues and improvements one step at a time, hiding the final code by default."
            />
            <FeatureCard 
              icon={<Brain className="w-8 h-8 text-pink-400" />}
              title="ML-Powered Structure Check"
              description="Uses AST embeddings and machine learning to score the structural quality of your code."
            />
            <FeatureCard 
              icon={<CheckCircle className="w-8 h-8 text-success" />}
              title="Code Quality Score"
              description="Overall score out of 100 with category breakdown to track your improvement."
            />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-body text-lg">A simple 4-step process to better coding.</p>
          </div>

          <div className="flex flex-col md:flex-row justify-between items-start md:items-center relative">
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-border -z-10 transform -translate-y-1/2"></div>
            
            <Step number="1" title="Paste Your Code" />
            <Step number="2" title="AI Analyzes It" />
            <Step number="3" title="Review Feedback & Learn" />
            <Step number="4" title="See Optimized Version" />
          </div>
        </div>
      </section>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }) => (
  <motion.div 
    whileHover={{ y: -5 }}
    className="bg-background border border-border rounded-xl p-6 hover:border-primary/50 transition-colors group"
  >
    <div className="mb-4 p-3 bg-surface rounded-lg inline-block group-hover:scale-110 transition-transform">
      {icon}
    </div>
    <h3 className="text-xl font-bold text-heading mb-2">{title}</h3>
    <p className="text-body leading-relaxed">{description}</p>
  </motion.div>
);

const Step = ({ number, title }) => (
  <div className="flex flex-col items-center text-center w-full md:w-1/4 mb-8 md:mb-0">
    <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-white font-bold text-xl mb-4 shadow-[0_0_15px_rgba(99,102,241,0.4)]">
      {number}
    </div>
    <h4 className="text-lg font-bold text-heading">{title}</h4>
  </div>
);

export default Landing;
