import jsPDF from 'jspdf';
import 'jspdf-autotable';

const generateReport = ({ code, language, results, analysisMode }) => {
  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.getWidth();
  let y = 20;

  // ───────── Color Palette ─────────
  const colors = {
    primary: [99, 102, 241],
    dark: [15, 15, 15],
    text: [55, 65, 81],
    lightBg: [243, 244, 246],
    success: [34, 197, 94],
    warning: [245, 158, 11],
    error: [239, 68, 68],
    white: [255, 255, 255],
  };

  // ───────── Helper Functions ─────────
  const addSectionTitle = (title) => {
    if (y > 260) {
      doc.addPage();
      y = 20;
    }
    doc.setFillColor(...colors.primary);
    doc.roundedRect(14, y - 2, pageWidth - 28, 10, 2, 2, 'F');
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(12);
    doc.setTextColor(...colors.white);
    doc.text(title, 18, y + 5);
    doc.setTextColor(...colors.text);
    y += 16;
  };

  const addKeyValue = (key, value) => {
    if (y > 275) {
      doc.addPage();
      y = 20;
    }
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(10);
    doc.text(`${key}:`, 18, y);
    doc.setFont('helvetica', 'normal');
    doc.text(String(value), 18 + doc.getTextWidth(`${key}: `), y);
    y += 7;
  };

  // ───────── Header ─────────
  doc.setFillColor(...colors.dark);
  doc.rect(0, 0, pageWidth, 45, 'F');

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(22);
  doc.setTextColor(...colors.white);
  doc.text('Smart Code Review', pageWidth / 2, 18, { align: 'center' });

  doc.setFontSize(11);
  doc.setTextColor(161, 161, 170);
  doc.text('AI-Powered Code Analysis Report', pageWidth / 2, 27, { align: 'center' });

  doc.setFontSize(9);
  doc.setTextColor(113, 113, 122);
  const timestamp = new Date().toLocaleString();
  doc.text(`Generated: ${timestamp}  •  Language: ${language.toUpperCase()}  •  Mode: ${analysisMode}`, pageWidth / 2, 36, { align: 'center' });

  y = 55;

  // ───────── Overall Score ─────────
  addSectionTitle('Quality Score');

  const score = results.score.overall;
  const scoreColor = score >= 80 ? colors.success : score >= 50 ? colors.warning : colors.error;

  doc.setFillColor(...colors.lightBg);
  doc.roundedRect(14, y - 2, pageWidth - 28, 28, 3, 3, 'F');

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(36);
  doc.setTextColor(...scoreColor);
  doc.text(`${score}`, 30, y + 18);

  doc.setFontSize(12);
  doc.setTextColor(...colors.text);
  doc.text('/ 100', 30 + doc.getTextWidth(`${score}`) + 3, y + 18);

  // Sub-scores on the right
  doc.setFontSize(9);
  const subScoreX = 110;
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(...colors.text);
  doc.text(`Correctness: ${results.score.correctness}`, subScoreX, y + 6);
  doc.text(`Performance: ${results.score.performance}`, subScoreX, y + 13);
  doc.text(`Readability: ${results.score.readability}`, subScoreX + 50, y + 6);
  doc.text(`Best Practices: ${results.score.bestPractices}`, subScoreX + 50, y + 13);

  y += 36;

  // ───────── Code Summary ─────────
  addSectionTitle('Submitted Code');

  const codeLines = code.split('\n').slice(0, 30);
  doc.setFont('courier', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(75, 85, 99);

  doc.setFillColor(248, 249, 252);
  const codeBlockHeight = Math.min(codeLines.length * 4.5 + 8, 120);
  doc.roundedRect(14, y - 2, pageWidth - 28, codeBlockHeight, 2, 2, 'F');
  doc.setDrawColor(229, 231, 235);
  doc.roundedRect(14, y - 2, pageWidth - 28, codeBlockHeight, 2, 2, 'S');

  codeLines.forEach((line, idx) => {
    if (y > 275) {
      doc.addPage();
      y = 20;
    }
    const lineNum = String(idx + 1).padStart(3, ' ');
    doc.setTextColor(156, 163, 175);
    doc.text(lineNum, 18, y + 3);
    doc.setTextColor(55, 65, 81);
    const truncatedLine = line.length > 90 ? line.substring(0, 90) + '...' : line;
    doc.text(truncatedLine, 30, y + 3);
    y += 4.5;
  });

  if (code.split('\n').length > 30) {
    doc.setTextColor(156, 163, 175);
    doc.setFont('helvetica', 'italic');
    doc.setFontSize(8);
    doc.text(`... and ${code.split('\n').length - 30} more lines`, 18, y + 3);
    y += 6;
  }

  y += 10;

  // ───────── Issues Detected ─────────
  addSectionTitle(`Issues Detected (${results.issues.length})`);

  if (results.issues.length > 0) {
    const issueData = results.issues.map((issue, idx) => [
      idx + 1,
      issue.severity?.toUpperCase() || 'INFO',
      issue.title || 'Untitled',
      (issue.description || '').substring(0, 80) + (issue.description?.length > 80 ? '...' : ''),
    ]);

    doc.autoTable({
      startY: y,
      margin: { left: 14, right: 14 },
      head: [['#', 'Severity', 'Issue', 'Description']],
      body: issueData,
      theme: 'grid',
      headStyles: {
        fillColor: colors.primary,
        textColor: colors.white,
        fontStyle: 'bold',
        fontSize: 9,
      },
      bodyStyles: {
        fontSize: 8,
        textColor: colors.text,
        cellPadding: 3,
      },
      columnStyles: {
        0: { cellWidth: 10 },
        1: { cellWidth: 22, fontStyle: 'bold' },
        2: { cellWidth: 40 },
        3: { cellWidth: 'auto' },
      },
      didParseCell: (data) => {
        if (data.section === 'body' && data.column.index === 1) {
          const severity = data.cell.raw;
          if (severity === 'CRITICAL') data.cell.styles.textColor = colors.error;
          else if (severity === 'WARNING') data.cell.styles.textColor = colors.warning;
          else data.cell.styles.textColor = colors.primary;
        }
      },
    });

    y = doc.lastAutoTable.finalY + 12;
  } else {
    doc.setFont('helvetica', 'italic');
    doc.setFontSize(10);
    doc.text('No issues detected. Great code!', 18, y);
    y += 12;
  }

  // ───────── Optimization Suggestions ─────────
  if (y > 240) {
    doc.addPage();
    y = 20;
  }

  addSectionTitle('Improvement Plan');

  if (results.steps && results.steps.length > 0) {
    results.steps.forEach((step) => {
      if (y > 255) {
        doc.addPage();
        y = 20;
      }

      doc.setFillColor(...colors.lightBg);
      doc.roundedRect(14, y - 2, pageWidth - 28, 24, 2, 2, 'F');

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(10);
      doc.setTextColor(...colors.primary);
      doc.text(`Step ${step.number}`, 18, y + 5);

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(8);
      doc.setTextColor(...colors.text);

      const whatLines = doc.splitTextToSize(`What: ${step.what}`, pageWidth - 42);
      doc.text(whatLines, 18, y + 11);

      const howLines = doc.splitTextToSize(`How: ${step.how}`, pageWidth - 42);
      doc.text(howLines, 18, y + 17);

      y += 28;
    });
  }

  // ───────── ML Analysis Summary ─────────
  if (results.mlStats) {
    if (y > 240) {
      doc.addPage();
      y = 20;
    }

    addSectionTitle('ML Analysis Summary');

    addKeyValue('Structural Quality Score', results.mlStats.structural_quality_score || 'N/A');
    addKeyValue('Anomaly Detected', results.mlStats.is_anomalous ? 'Yes' : 'No');
    addKeyValue('AI-Generated Probability', 
      results.mlStats.ai_generated_probability 
        ? `${(results.mlStats.ai_generated_probability * 100).toFixed(1)}%` 
        : 'N/A'
    );
    if (results.mlStats.top_nodes) {
      addKeyValue('Top AST Nodes', results.mlStats.top_nodes.join(', '));
    }
    y += 4;
  }

  // ───────── Optimized Code ─────────
  if (results.optimizedCode) {
    if (y > 200) {
      doc.addPage();
      y = 20;
    }

    addSectionTitle('Optimized Code');

    const optLines = results.optimizedCode.split('\n').slice(0, 40);
    doc.setFont('courier', 'normal');
    doc.setFontSize(8);

    doc.setFillColor(248, 249, 252);
    const optBlockHeight = Math.min(optLines.length * 4.5 + 8, 140);
    doc.roundedRect(14, y - 2, pageWidth - 28, optBlockHeight, 2, 2, 'F');
    doc.setDrawColor(229, 231, 235);
    doc.roundedRect(14, y - 2, pageWidth - 28, optBlockHeight, 2, 2, 'S');

    optLines.forEach((line, idx) => {
      if (y > 275) {
        doc.addPage();
        y = 20;
      }
      const lineNum = String(idx + 1).padStart(3, ' ');
      doc.setTextColor(156, 163, 175);
      doc.text(lineNum, 18, y + 3);
      doc.setTextColor(34, 197, 94);
      const truncatedLine = line.length > 90 ? line.substring(0, 90) + '...' : line;
      doc.text(truncatedLine, 30, y + 3);
      y += 4.5;
    });

    y += 10;
  }

  // ───────── Footer ─────────
  const totalPages = doc.getNumberOfPages();
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    doc.setFillColor(...colors.dark);
    doc.rect(0, doc.internal.pageSize.getHeight() - 12, pageWidth, 12, 'F');
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(7);
    doc.setTextColor(113, 113, 122);
    doc.text(
      'Generated by Smart Code Optimization and Review System',
      pageWidth / 2,
      doc.internal.pageSize.getHeight() - 5,
      { align: 'center' }
    );
    doc.text(
      `Page ${i} of ${totalPages}`,
      pageWidth - 18,
      doc.internal.pageSize.getHeight() - 5,
      { align: 'right' }
    );
  }

  // ───────── Save ─────────
  const filename = `code-review-report-${language}-${Date.now()}.pdf`;
  doc.save(filename);
};

export default generateReport;
