import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Code2, Menu, X, Sun, Moon } from 'lucide-react';
import { useState } from 'react';
import { useTheme } from '../context/ThemeContext';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  const navLinks = [
    { name: 'Features', path: '/#features' },
    { name: 'How It Works', path: '/#how-it-works' },
    { name: 'About', path: '/about' }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          
          <div className="flex-shrink-0 flex items-center gap-2">
            <Link to="/" className="flex items-center gap-2 text-heading font-bold text-xl hover:text-primary transition-colors">
              <Code2 className="h-6 w-6 text-primary" />
              <span>Smart Review</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              link.path.startsWith('/#') ? (
                <a 
                  key={link.name} 
                  href={link.path}
                  className="text-sm font-medium text-body hover:text-heading transition-colors"
                >
                  {link.name}
                </a>
              ) : (
                <Link 
                  key={link.name} 
                  to={link.path} 
                  className={`text-sm font-medium transition-colors ${isActive(link.path) ? 'text-primary' : 'text-body hover:text-heading'}`}
                >
                  {link.name}
                </Link>
              )
            ))}

            {/* Theme Toggle Button */}
            <button
              onClick={toggleTheme}
              className="relative p-2 rounded-lg bg-surface border border-border hover:border-primary/50 transition-all group"
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
              id="theme-toggle"
            >
              <div className="relative w-5 h-5">
                <Sun 
                  className={`absolute inset-0 w-5 h-5 text-warning transition-all duration-300 ${
                    theme === 'light' 
                      ? 'opacity-100 rotate-0 scale-100' 
                      : 'opacity-0 -rotate-90 scale-0'
                  }`} 
                />
                <Moon 
                  className={`absolute inset-0 w-5 h-5 text-primary transition-all duration-300 ${
                    theme === 'dark' 
                      ? 'opacity-100 rotate-0 scale-100' 
                      : 'opacity-0 rotate-90 scale-0'
                  }`} 
                />
              </div>
            </button>

            <Link 
              to="/editor" 
              className="px-4 py-2 rounded-md bg-primary text-white font-medium hover:bg-primary-hover transition-colors"
            >
              Start Reviewing Code
            </Link>
          </div>

          <div className="md:hidden flex items-center gap-3">
            {/* Mobile Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-surface border border-border"
              id="theme-toggle-mobile"
            >
              {theme === 'dark' ? (
                <Moon className="w-5 h-5 text-primary" />
              ) : (
                <Sun className="w-5 h-5 text-warning" />
              )}
            </button>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-body hover:text-heading"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden bg-surface border-b border-border">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navLinks.map((link) => (
              <div key={link.name}>
                {link.path.startsWith('/#') ? (
                  <a
                    href={link.path}
                    className="block px-3 py-2 rounded-md text-base font-medium text-body hover:text-heading hover:bg-surface-hover"
                    onClick={() => setIsOpen(false)}
                  >
                    {link.name}
                  </a>
                ) : (
                  <Link
                    to={link.path}
                    className="block px-3 py-2 rounded-md text-base font-medium text-body hover:text-heading hover:bg-surface-hover"
                    onClick={() => setIsOpen(false)}
                  >
                    {link.name}
                  </Link>
                )}
              </div>
            ))}
            <Link
              to="/editor"
              onClick={() => setIsOpen(false)}
              className="block w-full text-center mt-4 px-4 py-2 rounded-md bg-primary text-white font-medium"
            >
              Start Reviewing Code
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
