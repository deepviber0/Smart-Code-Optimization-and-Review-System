const { jsPDF } = require('jspdf');
const autoTable = require('jspdf-autotable');

try {
  const doc = new jsPDF('p', 'mm', 'a4');
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 14;
  const contentWidth = pageWidth - margin * 2;
  let y = 0;

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

  const ensureSpace = (needed) => {
    if (y + needed > pageHeight - 20) {
      doc.addPage();
      y = 20;
    }
  };

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

  doc.setFillColor(...C.dark);
  doc.rect(0, 0, pageWidth, 48, 'F');
  
  sectionHeader('Test Section');
  
  autoTable(doc, {
    startY: y,
    head: [['#', 'Severity', 'Line', 'Issue Title', 'Description']],
    body: [
      [1, 'WARNING', 'Line 1', 'Test Issue', 'Description']
    ]
  });

  doc.save('test.pdf');
  console.log('PDF generated successfully!');
} catch (err) {
  console.error('PDF Generation Error:', err);
}
