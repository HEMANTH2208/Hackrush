from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class ForensicReportGenerator:
    """Generate PDF forensic reports for scam analysis"""
    
    def __init__(self, output_dir='reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.red,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskMedium',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.orange,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.green,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, analysis_result, job_text):
        """Generate comprehensive forensic report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fraud_analysis_{timestamp}.pdf'
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("JobShield AI - Fraud Analysis Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Report metadata
        metadata = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis ID:', timestamp]
        ]
        t = Table(metadata, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 0.3*inch))
        
        # Risk Score Summary
        story.append(Paragraph("Risk Assessment Summary", self.styles['Heading2']))
        risk_score = analysis_result['risk_score']
        risk_tier = analysis_result['risk_tier']
        
        risk_style = self._get_risk_style(risk_tier)
        risk_text = f"Risk Score: {risk_score}% - {risk_tier.replace('_', ' ')}"
        story.append(Paragraph(risk_text, self.styles[risk_style]))
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendation
        story.append(Paragraph("Recommendation", self.styles['Heading3']))
        story.append(Paragraph(analysis_result['recommendation'], self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Component Scores
        story.append(Paragraph("Risk Component Breakdown", self.styles['Heading2']))
        components = analysis_result.get('component_scores', {})
        comp_data = [['Component', 'Score']]
        for comp, score in components.items():
            comp_data.append([comp.replace('_', ' ').title(), f"{score:.1f}%"])
        
        comp_table = Table(comp_data, colWidths=[3*inch, 2*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Evidence and Explanations
        if 'explanations' in analysis_result and analysis_result['explanations']:
            story.append(Paragraph("Evidence & Risk Factors", self.styles['Heading2']))
            for exp in analysis_result['explanations']:
                bullet = f"• <b>{exp['factor']}</b> ({exp['severity']}): {exp['detail']}"
                story.append(Paragraph(bullet, self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            story.append(Spacer(1, 0.2*inch))
        
        # Triggered Rules
        if 'triggered_rules' in analysis_result and analysis_result['triggered_rules']:
            story.append(Paragraph("Fraud Pattern Matches", self.styles['Heading2']))
            for rule in analysis_result['triggered_rules']:
                rule_text = f"• {rule['category'].replace('_', ' ').title()}: \"{rule['pattern']}\" (Severity: {rule['severity']})"
                story.append(Paragraph(rule_text, self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            story.append(Spacer(1, 0.2*inch))
        
        # Original Job Text
        story.append(PageBreak())
        story.append(Paragraph("Original Job Posting Content", self.styles['Heading2']))
        job_para = Paragraph(job_text[:2000], self.styles['Normal'])
        story.append(job_para)
        
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
