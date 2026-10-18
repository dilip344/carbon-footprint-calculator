from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle

def build_report(record,breakdown,recommendations,prediction,forecast,fusion=None):
 buf=BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=16*mm,bottomMargin=16*mm,title="GreenPulse AI Report"); styles=getSampleStyleSheet(); story=[]
 story += [Paragraph("GreenPulse AI",styles["Title"]),Paragraph("AI-Powered Carbon Footprint Report",styles["Heading2"]),Paragraph(f"User: {record.user_name}",styles["BodyText"]),Spacer(1,10)]
 rows=[["Metric","Result"],["Monthly footprint",f"{record.monthly_emissions:.2f} kg CO2e"],["Annual footprint",f"{record.annual_emissions:.2f} kg CO2e"],["Sustainability score",f"{record.sustainability_score:.1f}/100"],["AI lifestyle group",record.cluster],["AI annual prediction",f"{prediction:.2f} kg CO2e"]]
 t=Table(rows,colWidths=[75*mm,85*mm]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#173f31")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#dce8df")),("PADDING",(0,0),(-1,-1),6)])); story += [Paragraph("Summary",styles["Heading2"]),t]
 if fusion:
  fw=[["Fusion transparency","Value"],["Deterministic estimate",f"{fusion["deterministic_estimate"]:.2f} kg CO2e/year"],["Random Forest estimate",f"{fusion["ml_estimate"]:.2f} kg CO2e/year"],["Fused estimate",f"{fusion["fused_estimate"]:.2f} kg CO2e/year"],["AI confidence weight",f"{fusion["confidence_weight"]*100:.1f}%"],["Distribution distance (S1)",f"{fusion["s1_distance"]:.3f}"],["Cluster density (S2)",f"{fusion["s2_density"]:.3f}"],["Historical residual (S3)",f"{fusion["s3_residual"]:.3f}"],["Divergence detected","Yes" if fusion["divergence_flag"] else "No"]]
  ftb=Table(fw,colWidths=[75*mm,85*mm]); ftb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#173f31")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#dce8df")),("PADDING",(0,0),(-1,-1),5)])); story += [Spacer(1,10),Paragraph("Adaptive Fusion Transparency",styles["Heading2"]),ftb]
 br=[["Source","kg CO2e/month"]]+[[k,f"{v:.2f}"] for k,v in breakdown.items() if k!="Total"]+[["TOTAL",f"{breakdown['Total']:.2f}"]]
 bt=Table(br,colWidths=[75*mm,85*mm]); bt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#34745c")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#dce8df")),("PADDING",(0,0),(-1,-1),5)])); story += [Spacer(1,10),Paragraph("Emission Breakdown",styles["Heading2"]),bt,Spacer(1,10),Paragraph("Personalized Recommendations",styles["Heading2"])]
 for x in recommendations: story.append(Paragraph("• "+x,styles["BodyText"])); story.append(Spacer(1,4))
 fr=[["Forecast month","Estimated kg CO2e"]]+[[str(x["month"]),f"{x['estimated_emissions']:.2f}"] for x in forecast]; ft=Table(fr,colWidths=[75*mm,85*mm]); ft.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#34745c")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#dce8df")),("PADDING",(0,0),(-1,-1),5)])); story += [Spacer(1,10),Paragraph("AI Forecast",styles["Heading2"]),ft,Spacer(1,12),Paragraph("Educational MVP: replace demo emission factors with documented country-specific factors for final research use.",styles["BodyText"])]
 doc.build(story); buf.seek(0); return buf
