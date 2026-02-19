from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import re

class ForensicReportGenerator:
    """Generate PDF forensic reports for scam analysis"""
    
    def __init__(self, output_dir='reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Scam keywords to highlight
        self.scam_keywords = [
            'pay', 'fee', 'registration', 'processing', 'verification', 'deposit',
            'urgent', 'immediately', 'hurry', 'limited time', 'expires', 'last chance',
            'whatsapp only', 'telegram only', 'no interview', 'direct selection',
            'guaranteed', 'earn lakhs', 'work from home', 'no experience',
            'freshers', 'lpa', 'salary', 'package', 'selected', 'congratulations',
            'wallet', 'transfer', 'send money', 'payment', 'charges'
        ]
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#E74C3C'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskMedium',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#F39C12'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#27AE60'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='ScamHighlight',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2C3E50'),
            backColor=colors.HexColor('#FFE5E5'),
            leading=14
        ))
    
    def _highlight_scam_text(self, text):
        """Highlight scam-related keywords in text"""
        highlighted_text = text
        
        # Sort keywords by length (longest first) to avoid partial matches
        sorted_keywords = sorted(self.scam_keywords, key=len, reverse=True)
        
        for keyword in sorted_keywords:
            # Case-insensitive replacement with highlighting
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            highlighted_text = pattern.sub(
                lambda m: f'<font color="#E74C3C"><b>{m.group()}</b></font>',
                highlighted_text
            )
        
        return highlighted_text
    
    def generate_report(self, analysis_result, job_text):
        """Generate comprehensive forensic report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fraud_analysis_{timestamp}.pdf'
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # Title
        title = Paragraph("JobShield AI - Fraud Analysis Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Report metadata
        metadata = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis ID:', timestamp],
            ['Input Type:', analysis_result.get('input_type', 'text').upper()]
        ]
        t = Table(metadata, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#4A90E2')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E1E8ED'))
        ]))
        story.append(t)
        story.append(Spacer(1, 0.4*inch))
        
        # Risk Score Summary
        story.append(Paragraph("Risk Assessment Summary", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        risk_score = analysis_result['risk_score']
        risk_tier = analysis_result['risk_tier']
        
        risk_style = self._get_risk_style(risk_tier)
        risk_text = f"<b>Risk Score: {risk_score}%</b> - {risk_tier.replace('_', ' ')}"
        story.append(Paragraph(risk_text, self.styles[risk_style]))
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendation Box
        story.append(Paragraph("Recommendation", self.styles['Heading3']))
        recommendation_text = f"<b>{analysis_result['recommendation']}</b>"
        story.append(Paragraph(recommendation_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Component Scores
        story.append(Paragraph("Risk Component Breakdown", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        components = analysis_result.get('component_scores', {})
        comp_data = [['Component', 'Score', 'Status']]
        for comp, score in components.items():
            status = '⚠ HIGH RISK' if score > 70 else '⚡ MODERATE' if score > 40 else '✓ LOW RISK'
            comp_data.append([
                comp.replace('_', ' ').title(),
                f"{score:.1f}%",
                status
            ])
        
        comp_table = Table(comp_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A90E2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E1E8ED')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFB')])
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Evidence and Explanations
        if 'explanations' in analysis_result and analysis_result['explanations']:
            story.append(Paragraph("Evidence & Risk Factors", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for i, exp in enumerate(analysis_result['explanations'], 1):
                severity_color = '#E74C3C' if exp['severity'] == 'high' else '#F39C12' if exp['severity'] == 'medium' else '#27AE60'
                bullet = f"<font color='{severity_color}'><b>{i}. {exp['factor']}</b></font> ({exp['severity'].upper()})"
                story.append(Paragraph(bullet, self.styles['Normal']))
                story.append(Paragraph(f"   {exp['detail']}", self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            story.append(Spacer(1, 0.2*inch))
        
        # Triggered Rules
        if 'triggered_rules' in analysis_result and analysis_result['triggered_rules']:
            story.append(Paragraph("Fraud Pattern Matches", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for i, rule in enumerate(analysis_result['triggered_rules'], 1):
                rule_text = f"<font color='#E74C3C'><b>{i}. {rule['category'].replace('_', ' ').title()}</b></font>"
                story.append(Paragraph(rule_text, self.styles['Normal']))
                story.append(Paragraph(f"   Pattern: \"{rule['pattern']}\" (Severity: {rule['severity']})", self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            story.append(Spacer(1, 0.2*inch))
        
        # Company Verification
        if 'company_verification' in analysis_result and analysis_result['company_verification']:
            cv = analysis_result['company_verification']
            story.append(Paragraph("Company Verification", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            if cv.get('found'):
                status_text = f"<font color='#27AE60'><b>✓ Company Found in Registry</b></font>"
                story.append(Paragraph(status_text, self.styles['Normal']))
                story.append(Paragraph(f"Company: {cv.get('company_name', 'N/A')}", self.styles['Normal']))
                story.append(Paragraph(f"Confidence: {cv.get('confidence', 0)}%", self.styles['Normal']))
                story.append(Paragraph(f"Source: {cv.get('verification_source', 'Registry')}", self.styles['Normal']))
            else:
                status_text = f"<font color='#E74C3C'><b>✗ Company Not Found</b></font>"
                story.append(Paragraph(status_text, self.styles['Normal']))
                story.append(Paragraph(f"Message: {cv.get('message', 'Not verified')}", self.styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # Spam Lines Detection (if available)
        if 'spam_lines' in analysis_result and analysis_result['spam_lines']:
            story.append(Paragraph("Detected Spam/Scam Lines", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            spam_lines = analysis_result['spam_lines'][:10]  # Top 10
            for i, spam_line in enumerate(spam_lines, 1):
                line_text = spam_line['line']
                score = spam_line['score']
                patterns = ', '.join(spam_line['patterns'][:5])  # Show first 5 patterns
                
                # Highlight the line
                highlighted_line = self._highlight_scam_text(line_text)
                
                story.append(Paragraph(f"<b>{i}. Suspicious Line (Score: {score})</b>", self.styles['Normal']))
                story.append(Paragraph(highlighted_line, self.styles['ScamHighlight']))
                story.append(Paragraph(f"<i>Matched patterns: {patterns}</i>", self.styles['Normal']))
                story.append(Spacer(1, 0.15*inch))
            
            story.append(Spacer(1, 0.2*inch))
        
        # Original Job Text with Highlighting
        story.append(PageBreak())
        story.append(Paragraph("Original Job Posting Content (Suspicious Text Highlighted)", self.styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Highlight scam keywords in the text
        highlighted_text = self._highlight_scam_text(job_text[:3000])
        
        # Split into paragraphs for better formatting
        paragraphs = highlighted_text.split('\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para, self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = "<i>This report was generated by JobShield AI. For questions, visit our GitHub repository.</i>"
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def _get_risk_style(self, risk_tier):
        """Get style based on risk tier"""
        if 'CRITICAL' in risk_tier or 'HIGH' in risk_tier:
            return 'RiskHigh'
        elif 'MODERATE' in risk_tier:
            return 'RiskMedium'
        else:
            return 'RiskLow'
