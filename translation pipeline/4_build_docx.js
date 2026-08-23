const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, PageBreak } = require('docx');
const fs = require('fs');
const SURVEY_DATA = require('./survey_data_for_docx.js');

const LANG_ORDER = ['en', 'pt', 'es', 'ms', 'vi', 'bn'];
const LANG_LABELS = {
  en: 'English', pt: 'Portuguese (Brazil)', es: 'Spanish (Mexico, Peru)',
  ms: 'Bahasa Malaysia', vi: 'Vietnamese', bn: 'Bengali (Bangladesh)'
};
const TYPE_LABELS = {
  select: 'Dropdown', radio: 'Multiple choice', checkbox: 'Checkboxes',
  text: 'Short answer', textarea: 'Paragraph', scale: 'Linear scale, 1-5'
};

const NAVY = "1F3864";
const LIGHT = "E7EDF5";

function heading(text, level) {
  return new Paragraph({ text, heading: level, spacing: { before: 200, after: 100 } });
}

function para(runs, opts = {}) {
  return new Paragraph({ children: runs, spacing: { after: 80 }, ...opts });
}

function questionBlock(qNum, q, langCode) {
  const children = [];
  const typeLabel = TYPE_LABELS[q.type] || q.type;
  const reqLabel = q.req ? 'Required' : 'Not required';

  children.push(para([
    new TextRun({ text: `${qNum}. `, bold: true }),
    new TextRun({ text: q.q, bold: true }),
  ]));
  children.push(para([
    new TextRun({ text: `${typeLabel} — ${reqLabel}`, italics: true, size: 18, color: "555555" }),
  ]));

  if (q.opts && q.opts.length) {
    children.push(para([new TextRun({ text: q.opts.join(' / '), size: 20 })]));
  }
  if (q.type === 'scale' && langCode === 'en' && q.lo && q.hi) {
    children.push(para([new TextRun({ text: `1 = ${q.lo}, 5 = ${q.hi}`, size: 20 })]));
  }
  children.push(new Paragraph({ text: '', spacing: { after: 120 } }));
  return children;
}

function buildLanguageSection(langCode, isFirst) {
  const d = SURVEY_DATA[langCode];
  const children = [];

  if (!isFirst) {
    children.push(new Paragraph({ children: [new PageBreak()] }));
  }

  children.push(new Paragraph({
    text: `Google Forms Build Guide — ${LANG_LABELS[langCode]}`,
    heading: HeadingLevel.HEADING_1,
    spacing: { after: 100 }
  }));

  children.push(para([
    new TextRun({ text: 'Shareable link (paste here once the form is built and published): ', bold: true }),
    new TextRun({ text: '_______________________________________________', color: "999999" }),
  ]));
  children.push(new Paragraph({ text: '', spacing: { after: 150 } }));

  children.push(para([new TextRun({ text: 'Form title: ', bold: true }), new TextRun({ text: d.form_title })]));
  children.push(para([new TextRun({ text: 'Form description: ', bold: true }), new TextRun({ text: d.form_desc })]));
  children.push(new Paragraph({ text: '', spacing: { after: 150 } }));

  d.sections.forEach((section, si) => {
    children.push(heading(section.title, HeadingLevel.HEADING_2));
    children.push(para([new TextRun({ text: section.sub, italics: true, size: 20, color: "555555" })]));
    children.push(new Paragraph({ text: '', spacing: { after: 100 } }));
    section.questions.forEach((q, qi) => {
      questionBlock(qi + 1, q, langCode).forEach(p => children.push(p));
    });
  });

  if (langCode === 'en') {
    children.push(heading('Build checklist', HeadingLevel.HEADING_2));
    const checklist = [
      'Set form to collect email addresses: OFF (anonymity requirement, Section 3.16 of proposal)',
      'Settings -> Responses -> "Limit to 1 response": OFF (would require login, breaks anonymity)',
      'Confirm response destination is linked to a Sheet (Responses tab -> green Sheets icon -> Create/select spreadsheet)',
      'Test-submit once yourself before sharing the link',
      'Copy the shareable link (top right "Send" button -> link icon) and paste it at the top of this section',
    ];
    checklist.forEach(item => {
      children.push(new Paragraph({ text: item, bullet: { level: 0 }, spacing: { after: 60 } }));
    });
  }

  return children;
}

let allChildren = [];
LANG_ORDER.forEach((lc, i) => {
  allChildren = allChildren.concat(buildLanguageSection(lc, i === 0));
});

const doc = new Document({
  sections: [{
    properties: {},
    children: allChildren,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('Google_Forms_Build_Guide_All_Languages.docx', buffer);
  console.log('Document written');
});
