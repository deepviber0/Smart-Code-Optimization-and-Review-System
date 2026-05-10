import { jsPDF } from 'jspdf';
import autoTableModule from 'jspdf-autotable';

const autoTable = autoTableModule.default || autoTableModule.autoTable || autoTableModule;

const generateReport = ({ code, language, results, analysisMode }) => {
  try {
    const doc = new jsPDF('p', 'mm', 'a4');
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 14;
    const contentWidth = pageWidth - margin * 2;
    let y = 0;

    // ─────────────────────────────────────────────
    //  Color Palette
    // ─────────────────────────────────────────────
    const C = {
      primary:    [99, 102, 241],
      primaryDk:  [79, 70, 229],
      dark:       [17, 24, 39],
      darkSurface:[31, 41, 55],
      text:       [55, 65, 81],
      textLight:  [107, 114, 128],
      lightBg:    [243, 244, 246],
      lighterBg:  [249, 250, 251],
      success:    [22, 163, 74],
      warning:    [217, 119, 6],
      error:      [220, 38, 38],
      white:      [255, 255, 255],
      border:     [229, 231, 235],
    };

    const scoreColor = (val) => {
      if (val >= 80) return C.success;
      if (val >= 50) return C.warning;
      return C.error;
    };

    const scoreLabel = (val) => {
      if (val >= 90) return 'Excellent';
      if (val >= 80) return 'Great';
      if (val >= 70) return 'Good';
      if (val >= 50) return 'Needs Work';
      return 'Poor';
    };

    // ─────────────────────────────────────────────
    //  Helper: page break check
    // ─────────────────────────────────────────────
    const ensureSpace = (needed) => {
      if (y + needed > pageHeight - 20) {
        doc.addPage();
        y = 20;
      }
    };

    // ─────────────────────────────────────────────
    //  Helper: section header
    // ─────────────────────────────────────────────
    const sectionHeader = (title, icon) => {
      ensureSpace(18);
      doc.setFillColor(...C.primary);
      doc.rect(margin, y, contentWidth, 10, 'F');
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(11);
      doc.setTextColor(...C.white);
      doc.text((icon ? icon + '  ' : '') + title, margin + 4, y + 7);
      doc.setTextColor(...C.text);
      y += 14;
    };

    // ─────────────────────────────────────────────
    //  Helper: sub-section header
    // ─────────────────────────────────────────────
    const subHeader = (title) => {
      ensureSpace(12);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(10);
      doc.setTextColor(...C.primaryDk);
      doc.text(title, margin, y);
      y += 6;
    };

    // ─────────────────────────────────────────────
    //  Helper: draw a score bar
    // ─────────────────────────────────────────────
    const drawScoreBar = (label, value, xStart, barWidth) => {
      ensureSpace(12);
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(9);
      doc.setTextColor(...C.text);
      doc.text(label, xStart, y);
      doc.text(`${value}/100`, xStart + barWidth - 2, y, { align: 'right' });
      y += 3;

      // Track
      doc.setFillColor(...C.lightBg);
      doc.rect(xStart, y, barWidth, 3, 'F');

      // Fill
      const color = scoreColor(value);
      const fillWidth = Math.max(0, (value / 100) * barWidth);
      doc.setFillColor(...color);
      doc.rect(xStart, y, fillWidth, 3, 'F');

      y += 7;
    };

    // ─────────────────────────────────────────────
    //  Helper: key-value row
    // ─────────────────────────────────────────────
    const kvRow = (key, value) => {
      ensureSpace(8);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(9);
      doc.setTextColor(...C.text);
      doc.text(`${key}:`, margin + 2, y);
      doc.setFont('helvetica', 'normal');
      const keyWidth = doc.getTextWidth(`${key}:  `);
      doc.text(String(value ?? 'N/A'), margin + 2 + keyWidth, y);
      y += 6;
    };

    // ═══════════════════════════════════════════════
    //  PAGE HEADER / TITLE BLOCK
    // ═══════════════════════════════════════════════
    doc.setFillColor(...C.dark);
    doc.rect(0, 0, pageWidth, 48, 'F');

    // Accent line
    doc.setFillColor(...C.primary);
    doc.rect(0, 48, pageWidth, 2, 'F');

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(24);
    doc.setTextColor(...C.white);
    doc.text('Smart Code Review', pageWidth / 2, 18, { align: 'center' });

    doc.setFontSize(11);
    doc.setTextColor(161, 161, 170);
    doc.text('AI-Powered Code Analysis Report', pageWidth / 2, 27, { align: 'center' });

    doc.setFontSize(8);
    doc.setTextColor(113, 113, 122);
    const now = new Date();
    const dateStr = now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    doc.text(`${dateStr}  |  ${timeStr}  |  Language: ${language.toUpperCase()}  |  Mode: ${analysisMode.charAt(0).toUpperCase() + analysisMode.slice(1)}`, pageWidth / 2, 38, { align: 'center' });

    y = 58;

    // ═══════════════════════════════════════════════
    //  1. EXECUTIVE SUMMARY
    // ═══════════════════════════════════════════════
    sectionHeader('Executive Summary');

    const score = results.score?.overall ?? 0;
    const sColor = scoreColor(score);

    // Score display
    doc.setFillColor(...C.lighterBg);
    doc.rect(margin, y - 2, contentWidth, 32, 'F');
    doc.setDrawColor(...C.border);
    doc.rect(margin, y - 2, contentWidth, 32, 'S');

    // Big score number
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(40);
    doc.setTextColor(...sColor);
    doc.text(`${score}`, margin + 12, y + 22);

    const scoreTextWidth = doc.getTextWidth(`${score}`);
    doc.setFontSize(14);
    doc.setTextColor(...C.textLight);
    doc.text('/ 100', margin + 14 + scoreTextWidth, y + 22);

    // Score label
    doc.setFontSize(12);
    doc.setTextColor(...sColor);
    doc.text(scoreLabel(score), margin + 14 + scoreTextWidth + 30, y + 10);

    // Summary text
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.setTextColor(...C.text);
    const issueCount = results.issues?.length ?? 0;
    const stepCount = results.steps?.length ?? 0;
    const summaryText = `Analysis detected ${issueCount} issue${issueCount !== 1 ? 's' : ''} with ${stepCount} improvement suggestion${stepCount !== 1 ? 's' : ''}.`;
    doc.text(summaryText, margin + 14 + scoreTextWidth + 30, y + 20);

    y += 36;

    // Sub-score bars
    subHeader('Category Breakdown');
    const barWidth = contentWidth - 4;
    const b = results.score?.breakdown || {};
    
    // Normalize to 100 for the bar display
    drawScoreBar('Correctness', Math.round((b.syntax_safety || 0) * 4), margin + 2, barWidth);
    drawScoreBar('Performance', Math.round((b.performance || 0) * 5), margin + 2, barWidth);
    drawScoreBar('Readability', Math.round((b.readability || 0) * 5), margin + 2, barWidth);
    drawScoreBar('Best Practices', Math.round((b.best_practices || 0) * 5), margin + 2, barWidth);
    drawScoreBar('Structural Design', Math.round((b.structure || 0) * 6.67), margin + 2, barWidth);

    y += 4;

    // ═══════════════════════════════════════════════
    //  2. SUBMITTED CODE
    // ═══════════════════════════════════════════════
    sectionHeader('Submitted Code');

    const allCodeLines = (code || '').split('\n');
    const codeLinesToShow = allCodeLines.slice(0, 35);
    const totalLines = allCodeLines.length;

    kvRow('Total Lines', totalLines);
    kvRow('Language', language.charAt(0).toUpperCase() + language.slice(1));
    y += 2;

    doc.setFillColor(...C.lighterBg);
    doc.setDrawColor(...C.border);
    const codeBlockH = Math.min(codeLinesToShow.length * 4.2 + 6, 130);
    doc.rect(margin, y, contentWidth, codeBlockH, 'FD');

    doc.setFont('courier', 'normal');
    doc.setFontSize(7.5);
    let codeY = y + 5;

    codeLinesToShow.forEach((line, idx) => {
      if (codeY > pageHeight - 22) {
        doc.addPage();
        codeY = 20;
      }
      // Line number
      doc.setTextColor(156, 163, 175);
      doc.text(String(idx + 1).padStart(3, ' '), margin + 2, codeY);
      // Separator
      doc.setTextColor(209, 213, 219);
      doc.text('|', margin + 12, codeY);
      // Code
      doc.setTextColor(31, 41, 55);
      const safeLine = (line || '').substring(0, 95) + (line.length > 95 ? '...' : '');
      doc.text(safeLine, margin + 15, codeY);
      codeY += 4.2;
    });

    y = codeY + 4;
    if (totalLines > 35) {
      doc.setFont('helvetica', 'italic');
      doc.setFontSize(8);
      doc.setTextColor(...C.textLight);
      doc.text(`... ${totalLines - 35} more lines not shown`, margin + 2, y);
      y += 6;
    }
    y += 4;

    // ═══════════════════════════════════════════════
    //  3. ISSUES DETECTED
    // ═══════════════════════════════════════════════
    sectionHeader(`Issues Detected  (${issueCount})`);

    if (results.issues && results.issues.length > 0) {
      const issueRows = results.issues.map((issue, idx) => {
        const sev = (issue.severity || 'info').toUpperCase();
        const title = issue.title || 'Untitled Issue';
        const desc = (issue.description || 'No description provided.');
        const line = issue.line ? `Line ${issue.line}` : '-';
        return [idx + 1, sev, line, title, desc];
      });

      autoTable(doc, {
        startY: y,
        margin: { left: margin, right: margin },
        head: [['#', 'Severity', 'Line', 'Issue Title', 'Description']],
        body: issueRows,
        theme: 'striped',
        headStyles: {
          fillColor: C.dark,
          textColor: C.white,
          fontStyle: 'bold',
          fontSize: 8,
          cellPadding: 3,
        },
        bodyStyles: {
          fontSize: 7.5,
          textColor: C.text,
          cellPadding: 2.5,
          lineColor: C.border,
        },
        alternateRowStyles: {
          fillColor: C.lighterBg,
        },
        columnStyles: {
          0: { cellWidth: 8, halign: 'center' },
          1: { cellWidth: 18, halign: 'center', fontStyle: 'bold' },
          2: { cellWidth: 14, halign: 'center' },
          3: { cellWidth: 38 },
          4: { cellWidth: 'auto' },
        },
        didParseCell: (data) => {
          if (data.section === 'body' && data.column.index === 1) {
            const sev = data.cell.raw;
            if (sev === 'CRITICAL') data.cell.styles.textColor = C.error;
            else if (sev === 'WARNING') data.cell.styles.textColor = C.warning;
            else data.cell.styles.textColor = C.primary;
          }
        },
      });

      y = doc.lastAutoTable.finalY + 10;
    } else {
      doc.setFillColor(236, 253, 245);
      doc.rect(margin, y, contentWidth, 10, 'F');
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(10);
      doc.setTextColor(...C.success);
      doc.text('✓  No issues detected — excellent code quality!', margin + 4, y + 7);
      y += 16;
    }

    // ═══════════════════════════════════════════════
    //  4. IMPROVEMENT PLAN
    // ═══════════════════════════════════════════════
    if (results.steps && results.steps.length > 0) {
      sectionHeader(`Improvement Plan  (${results.steps.length} steps)`);

      results.steps.forEach((step) => {
        ensureSpace(30);

        // Step number badge
        doc.setFillColor(...C.primary);
        doc.circle(margin + 5, y + 3, 4, 'F');
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(9);
        doc.setTextColor(...C.white);
        doc.text(String(step.number || '?'), margin + 5, y + 4.5, { align: 'center' });

        // What to fix
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(9);
        doc.setTextColor(...C.dark);
        const whatText = doc.splitTextToSize(step.what || '', contentWidth - 20);
        doc.text(whatText, margin + 12, y + 4);
        y += Math.max(8, whatText.length * 4);

        // Why it matters
        if (step.why) {
          doc.setFont('helvetica', 'italic');
          doc.setFontSize(8);
          doc.setTextColor(...C.textLight);
          const whyText = doc.splitTextToSize('Why: ' + step.why, contentWidth - 16);
          doc.text(whyText, margin + 12, y);
          y += whyText.length * 3.5 + 1;
        }

        // How to fix
        if (step.how) {
          doc.setFont('helvetica', 'normal');
          doc.setFontSize(8);
          doc.setTextColor(...C.success);
          const howText = doc.splitTextToSize('Fix: ' + step.how, contentWidth - 16);
          doc.text(howText, margin + 12, y);
          y += howText.length * 3.5 + 1;
        }

        // Divider line
        doc.setDrawColor(...C.border);
        doc.setLineWidth(0.2);
        doc.line(margin + 12, y + 1, margin + contentWidth - 4, y + 1);
        y += 5;
      });
    }

    // ═══════════════════════════════════════════════
    //  5. ML ANALYSIS
    // ═══════════════════════════════════════════════
    if (results.mlStats) {
      sectionHeader('Machine Learning Analysis');

      doc.setFillColor(...C.lighterBg);
      doc.setDrawColor(...C.border);
      doc.rect(margin, y, contentWidth, 28, 'FD');

      const colW = contentWidth / 3;

      // Column 1: Structural Quality
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7);
      doc.setTextColor(...C.textLight);
      doc.text('STRUCTURAL QUALITY', margin + colW * 0 + 6, y + 6);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(18);
      doc.setTextColor(...scoreColor(results.mlStats.structural_quality_score || 0));
      doc.text(String(results.mlStats.structural_quality_score ?? 'N/A'), margin + colW * 0 + 6, y + 18);

      // Column 2: Anomaly Status
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7);
      doc.setTextColor(...C.textLight);
      doc.text('ANOMALY STATUS', margin + colW * 1 + 6, y + 6);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(14);
      const isAnom = results.mlStats.is_anomalous;
      doc.setTextColor(...(isAnom ? C.error : C.success));
      doc.text(isAnom ? 'Detected' : 'Normal', margin + colW * 1 + 6, y + 18);

      // Column 3: AI-Generated Probability
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7);
      doc.setTextColor(...C.textLight);
      doc.text('AI-GENERATED PROB.', margin + colW * 2 + 6, y + 6);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(18);
      doc.setTextColor(...C.dark);
      const aiProb = results.mlStats.ai_generated_probability;
      doc.text(aiProb != null ? `${(aiProb * 100).toFixed(0)}%` : 'N/A', margin + colW * 2 + 6, y + 18);

      y += 34;

      // Top AST Nodes
      if (results.mlStats.top_nodes && results.mlStats.top_nodes.length > 0) {
        kvRow('Top AST Node Types', results.mlStats.top_nodes.slice(0, 8).join(', '));
      }
      if (results.mlStats.total_nodes) {
        kvRow('Total AST Nodes Parsed', results.mlStats.total_nodes);
      }
      y += 4;
    }

    // ═══════════════════════════════════════════════
    //  6. OPTIMIZED CODE
    // ═══════════════════════════════════════════════
    if (results.optimizedCode) {
      sectionHeader('Optimized Code');

      const optLines = results.optimizedCode.split('\n').slice(0, 45);

      doc.setFillColor(240, 253, 244);
      doc.setDrawColor(187, 247, 208);
      const optBlockH = Math.min(optLines.length * 4.2 + 6, 150);
      doc.rect(margin, y, contentWidth, optBlockH, 'FD');

      doc.setFont('courier', 'normal');
      doc.setFontSize(7.5);
      let optY = y + 5;

      optLines.forEach((line, idx) => {
        if (optY > pageHeight - 22) {
          doc.addPage();
          optY = 20;
        }
        // Line number
        doc.setTextColor(134, 239, 172);
        doc.text(String(idx + 1).padStart(3, ' '), margin + 2, optY);
        doc.text('|', margin + 12, optY);
        // Code in green-tinted text
        doc.setTextColor(21, 128, 61);
        const safeLine = (line || '').substring(0, 95) + (line.length > 95 ? '...' : '');
        doc.text(safeLine, margin + 15, optY);
        optY += 4.2;
      });

      y = optY + 4;

      if (results.optimizedCode.split('\n').length > 45) {
        doc.setFont('helvetica', 'italic');
        doc.setFontSize(8);
        doc.setTextColor(...C.textLight);
        doc.text(`... ${results.optimizedCode.split('\n').length - 45} more lines not shown`, margin + 2, y);
        y += 6;
      }
    }

    // ═══════════════════════════════════════════════
    //  FOOTER ON ALL PAGES
    // ═══════════════════════════════════════════════
    const totalPages = doc.getNumberOfPages();
    for (let i = 1; i <= totalPages; i++) {
      doc.setPage(i);

      // Dark footer bar
      doc.setFillColor(...C.dark);
      doc.rect(0, pageHeight - 10, pageWidth, 10, 'F');

      // Accent line above footer
      doc.setFillColor(...C.primary);
      doc.rect(0, pageHeight - 10, pageWidth, 0.5, 'F');

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7);
      doc.setTextColor(156, 163, 175);
      doc.text(
        'Smart Code Optimization and Review System  —  AI-Powered Analysis',
        pageWidth / 2,
        pageHeight - 4,
        { align: 'center' }
      );
      doc.text(
        `Page ${i} / ${totalPages}`,
        pageWidth - margin,
        pageHeight - 4,
        { align: 'right' }
      );
      doc.text(
        dateStr,
        margin,
        pageHeight - 4
      );
    }

    // ═══════════════════════════════════════════════
    //  SAVE FILE
    // ═══════════════════════════════════════════════
    const filename = `SmartReview-Report-${language}-${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}.pdf`;
    doc.save(filename);

  } catch (err) {
    console.error('PDF Generation Error:', err);
    alert('Failed to generate PDF report. Check console for details.');
  }
};

export default generateReport;
