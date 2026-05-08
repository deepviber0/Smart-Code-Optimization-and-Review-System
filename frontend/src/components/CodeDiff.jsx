import React, { useMemo } from 'react';
import { diffLines } from 'diff';

const CodeDiff = ({ originalCode, optimizedCode, language }) => {
  const diffResult = useMemo(() => {
    if (!originalCode || !optimizedCode) return [];
    return diffLines(originalCode, optimizedCode);
  }, [originalCode, optimizedCode]);

  // Build line-by-line arrays for side-by-side
  const { leftLines, rightLines } = useMemo(() => {
    const left = [];
    const right = [];
    let leftNum = 1;
    let rightNum = 1;

    diffResult.forEach((part) => {
      const lines = part.value.split('\n');
      // Remove trailing empty string from split
      if (lines[lines.length - 1] === '') lines.pop();

      if (part.removed) {
        lines.forEach((line) => {
          left.push({ num: leftNum++, text: line, type: 'removed' });
          right.push({ num: null, text: '', type: 'empty' });
        });
      } else if (part.added) {
        lines.forEach((line) => {
          left.push({ num: null, text: '', type: 'empty' });
          right.push({ num: rightNum++, text: line, type: 'added' });
        });
      } else {
        lines.forEach((line) => {
          left.push({ num: leftNum++, text: line, type: 'unchanged' });
          right.push({ num: rightNum++, text: line, type: 'unchanged' });
        });
      }
    });

    return { leftLines: left, rightLines: right };
  }, [diffResult]);

  const getLineClass = (type) => {
    switch (type) {
      case 'removed': return 'bg-error/10 border-l-[3px] border-error';
      case 'added': return 'bg-success/10 border-l-[3px] border-success';
      case 'empty': return 'bg-surface/50';
      default: return 'border-l-[3px] border-transparent';
    }
  };

  const getTextClass = (type) => {
    switch (type) {
      case 'removed': return 'text-error/90';
      case 'added': return 'text-success/90';
      case 'empty': return '';
      default: return 'text-body';
    }
  };

  const stats = useMemo(() => {
    let added = 0, removed = 0;
    diffResult.forEach(part => {
      const count = part.value.split('\n').filter(l => l !== '').length;
      if (part.added) added += count;
      if (part.removed) removed += count;
    });
    return { added, removed };
  }, [diffResult]);

  return (
    <div className="space-y-3">
      {/* Stats Bar */}
      <div className="flex items-center gap-4 px-4 py-2 bg-surface rounded-lg border border-border text-sm">
        <span className="text-heading font-medium">Changes:</span>
        <span className="flex items-center gap-1.5 text-success">
          <span className="w-2.5 h-2.5 rounded-sm bg-success/20 border border-success/40"></span>
          +{stats.added} added
        </span>
        <span className="flex items-center gap-1.5 text-error">
          <span className="w-2.5 h-2.5 rounded-sm bg-error/20 border border-error/40"></span>
          -{stats.removed} removed
        </span>
      </div>

      {/* Side-by-Side Diff */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-0 border border-border rounded-xl overflow-hidden">
        {/* Left: Original */}
        <div className="border-b lg:border-b-0 lg:border-r border-border">
          <div className="px-4 py-2.5 bg-error/5 border-b border-border flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-error/30"></span>
            <span className="text-sm font-semibold text-heading">Original</span>
          </div>
          <div className="overflow-x-auto bg-codebg">
            <pre className="text-sm font-mono leading-relaxed">
              {leftLines.map((line, idx) => (
                <div key={`left-${idx}`} className={`flex min-h-[24px] ${getLineClass(line.type)}`}>
                  <span className="w-12 flex-shrink-0 text-right pr-3 text-muted text-xs leading-[24px] select-none border-r border-border/30">
                    {line.num || ''}
                  </span>
                  <span className={`pl-3 pr-4 whitespace-pre ${getTextClass(line.type)}`}>
                    {line.type === 'removed' && <span className="text-error/50 mr-1">−</span>}
                    {line.text}
                  </span>
                </div>
              ))}
            </pre>
          </div>
        </div>

        {/* Right: Optimized */}
        <div>
          <div className="px-4 py-2.5 bg-success/5 border-b border-border flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-success/30"></span>
            <span className="text-sm font-semibold text-heading">Optimized</span>
          </div>
          <div className="overflow-x-auto bg-codebg">
            <pre className="text-sm font-mono leading-relaxed">
              {rightLines.map((line, idx) => (
                <div key={`right-${idx}`} className={`flex min-h-[24px] ${getLineClass(line.type)}`}>
                  <span className="w-12 flex-shrink-0 text-right pr-3 text-muted text-xs leading-[24px] select-none border-r border-border/30">
                    {line.num || ''}
                  </span>
                  <span className={`pl-3 pr-4 whitespace-pre ${getTextClass(line.type)}`}>
                    {line.type === 'added' && <span className="text-success/50 mr-1">+</span>}
                    {line.text}
                  </span>
                </div>
              ))}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeDiff;
