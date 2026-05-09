import React, { useRef, useEffect, useCallback } from 'react';
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, drawSelection } from '@codemirror/view';
import { EditorState, Compartment } from '@codemirror/state';
import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands';
import { syntaxHighlighting, defaultHighlightStyle, bracketMatching, indentOnInput, foldGutter } from '@codemirror/language';
import { javascript } from '@codemirror/lang-javascript';
import { python } from '@codemirror/lang-python';
import { java } from '@codemirror/lang-java';
import { cpp } from '@codemirror/lang-cpp';
import { oneDark } from '@codemirror/theme-one-dark';
import { useTheme } from '../context/ThemeContext';

const languageExtensions = {
  javascript: () => javascript(),
  python: () => python(),
  java: () => java(),
  c: () => cpp(),
  cpp: () => cpp(),
};

// Light theme for CodeMirror
const lightTheme = EditorView.theme({
  '&': {
    backgroundColor: '#FFFFFF',
    color: '#1F2937',
  },
  '.cm-content': {
    caretColor: '#6366F1',
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
  },
  '.cm-cursor': {
    borderLeftColor: '#6366F1',
  },
  '&.cm-focused .cm-selectionBackground, .cm-selectionBackground': {
    backgroundColor: 'rgba(99, 102, 241, 0.15) !important',
  },
  '.cm-activeLine': {
    backgroundColor: 'rgba(99, 102, 241, 0.05)',
  },
  '.cm-gutters': {
    backgroundColor: '#F9FAFB',
    color: '#9CA3AF',
    border: 'none',
    borderRight: '1px solid rgba(0,0,0,0.06)',
  },
  '.cm-activeLineGutter': {
    backgroundColor: 'rgba(99, 102, 241, 0.08)',
    color: '#6366F1',
  },
}, { dark: false });

const CodeEditor = ({ value, onChange, language }) => {
  const editorRef = useRef(null);
  const viewRef = useRef(null);
  const langCompartment = useRef(new Compartment());
  const themeCompartment = useRef(new Compartment());
  const isInternalUpdate = useRef(false);
  const { theme } = useTheme();

  const getLanguageExtension = useCallback((lang) => {
    const factory = languageExtensions[lang];
    return factory ? factory() : javascript();
  }, []);

  const getThemeExtension = useCallback((currentTheme) => {
    return currentTheme === 'dark' ? oneDark : lightTheme;
  }, []);

  // Create editor on mount
  useEffect(() => {
    if (!editorRef.current) return;

    const updateListener = EditorView.updateListener.of((update) => {
      if (update.docChanged && !isInternalUpdate.current) {
        const newValue = update.state.doc.toString();
        onChange(newValue);
      }
    });

    const state = EditorState.create({
      doc: value || '',
      extensions: [
        lineNumbers(),
        highlightActiveLine(),
        highlightActiveLineGutter(),
        history(),
        drawSelection(),
        bracketMatching(),
        indentOnInput(),
        foldGutter(),
        syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
        keymap.of([...defaultKeymap, ...historyKeymap, indentWithTab]),
        langCompartment.current.of(getLanguageExtension(language)),
        themeCompartment.current.of(getThemeExtension(theme)),
        updateListener,
        EditorView.lineWrapping,
        EditorState.tabSize.of(2),
      ],
    });

    const view = new EditorView({
      state,
      parent: editorRef.current,
    });

    viewRef.current = view;

    return () => {
      view.destroy();
      viewRef.current = null;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Reconfigure language when it changes
  useEffect(() => {
    if (!viewRef.current) return;
    viewRef.current.dispatch({
      effects: langCompartment.current.reconfigure(getLanguageExtension(language)),
    });
  }, [language, getLanguageExtension]);

  // Reconfigure theme when it changes
  useEffect(() => {
    if (!viewRef.current) return;
    viewRef.current.dispatch({
      effects: themeCompartment.current.reconfigure(getThemeExtension(theme)),
    });
  }, [theme, getThemeExtension]);

  // Sync external value changes (e.g., sample code loading, clear)
  useEffect(() => {
    if (!viewRef.current) return;
    const currentDoc = viewRef.current.state.doc.toString();
    if (value !== currentDoc) {
      isInternalUpdate.current = true;
      viewRef.current.dispatch({
        changes: {
          from: 0,
          to: currentDoc.length,
          insert: value || '',
        },
      });
      isInternalUpdate.current = false;
    }
  }, [value]);

  return (
    <div
      ref={editorRef}
      className="absolute inset-0 w-full h-full overflow-hidden"
      id="code-editor-container"
    />
  );
};

export default CodeEditor;
