import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define custom Canvas for headers and footers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Cover page (Page 1) doesn't get headers/footers
        if self._pageNumber == 1:
            self.saveState()
            # Draw OL Blue block on the left
            self.setFillColor(colors.HexColor("#0B2C5C"))
            self.rect(0, 0, 30, 792, fill=True, stroke=False)
            # Draw OL Red thin block next to it
            self.setFillColor(colors.HexColor("#D31115"))
            self.rect(30, 0, 10, 792, fill=True, stroke=False)
            self.restoreState()
            return
            
        self.saveState()
        
        # Header text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0B2C5C"))
        self.drawString(54, 745, "PROJET RECRUITMENT MATCH")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawRightString(558, 745, "CAHIER DES CHARGES")
        
        # Header Line
        self.setStrokeColor(colors.HexColor("#D1D5DB"))
        self.setLineWidth(0.5)
        self.line(54, 737, 558, 737)
        
        # Footer Line
        self.line(54, 60, 558, 60)
        
        # Footer Text
        page_text = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(558, 45, page_text)
        self.drawString(54, 45, "Confidentiel - Projet Académique L3 Web 2026")
        self.restoreState()

def create_specification_pdf(filename="Cahier_des_charges_Recruitment_Match.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Configure colors
    primary_color = colors.HexColor("#0B2C5C") # OL Blue
    secondary_color = colors.HexColor("#D31115") # OL Red
    text_color = colors.HexColor("#333333") # Charcoal
    
    # Modify normal style
    styles['Normal'].textColor = text_color
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=primary_color,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=18,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=40
    )
    
    metadata_style = ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=16,
        textColor=colors.HexColor("#1F2937")
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    # --- PAGE 1: COVER PAGE ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("CAHIER DES CHARGES", ParagraphStyle('Upper', fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=secondary_color, spaceAfter=10)))
    story.append(Paragraph("PROJET RECRUITMENT MATCH", title_style))
    story.append(Paragraph("Application SaaS d'aide à la décision pour le recrutement de football professionnel basée sur la similarité statistique", subtitle_style))
    
    story.append(Spacer(1, 150))
    
    meta_text = """
    <b>Auteur :</b> Rayane Ourad<br/>
    <b>Cadre :</b> Projet Universitaire - Licence 3 Informatique (Web 2026)<br/>
    <b>Date de livraison :</b> 30 Juin 2026<br/>
    <b>Cible R&D :</b> Cellule de Recrutement / Olympique Lyonnais (OL)
    """
    story.append(Paragraph(meta_text, metadata_style))
    story.append(PageBreak())
    
    # --- PAGE 2: CONTEXTE & OBJECTIFS ---
    story.append(Paragraph("1. Contexte et Objectifs du Projet", h1_style))
    story.append(Paragraph("1.1. Contexte", h2_style))
    story.append(Paragraph(
        "Le marché actuel du recrutement sportif est confronté à des inefficacités majeures. Les clubs de football "
        "dépensent des sommes colossales pour des joueurs dont le profil ne correspond pas toujours aux besoins tactiques "
        "ou financiers réels. Le processus de recrutement repose souvent sur des réseaux informels d'agents, des "
        "échanges de messages désorganisés (ex. WhatsApp) et des analyses vidéo subjectives, manquant de rigueur statistique. "
        "De plus, les bases de données professionnelles classiques (ex. Wyscout) sont extrêmement coûteuses et complexes à utiliser.",
        body_style
    ))
    
    story.append(Paragraph("1.2. Problématique", h2_style))
    story.append(Paragraph(
        "<i>« Comment rationaliser le recrutement sportif en utilisant la Data Intelligence pour identifier instantanément "
        "des talents correspondant à des critères tactiques, physiques et financiers précis, tout en proposant des alternatives "
        "économiques viables aux stars du marché ? »</i>",
        body_style
    ))
    
    story.append(Paragraph("1.3. Objectifs Principaux", h2_style))
    story.append(Paragraph("• <b>Optimisation Budgétaire :</b> Aider le club (ici l'Olympique Lyonnais) à trouver des profils équivalents à moindre coût (High Value / Low Cost).", bullet_style))
    story.append(Paragraph("• <b>Rationalisation Scientifique :</b> Remplacer l'intuition par un algorithme de similarité statistique pour comparer les joueurs.", bullet_style))
    story.append(Paragraph("• <b>Gain de Temps :</b> Permettre aux recruteurs de filtrer instantanément des milliers de profils selon des critères complexes.", bullet_style))
    story.append(Paragraph("• <b>Prise de Décision Sécurisée :</b> Valider la disponibilité, la situation contractuelle et les coûts des joueurs pour éviter les erreurs de casting.", bullet_style))
    
    story.append(Spacer(1, 15))
    
    # --- PAGE 2 (Suite): SWOT ---
    story.append(Paragraph("2. Analyse SWOT", h1_style))
    
    # SWOT Table Data
    swot_data = [
        [
            Paragraph("<b>FORCES (Strengths)</b><br/>• UX Simplifiée (Chercher, Comparer, Trouver).<br/>• Algorithme de Matching statistique objectif.<br/>• Aide à la décision financière (High Value / Low Cost).", body_style),
            Paragraph("<b>FAIBLESSES (Weaknesses)</b><br/>• Dépendance à des données Open Source moins denses.<br/>• Absence du facteur humain (mental, blessures).<br/>• Nouvel outil sans historique de réussite client.", body_style)
        ],
        [
            Paragraph("<b>OPPORTUNITÉS (Opportunities)</b><br/>• Contexte de baisse des droits TV : obligation de recruter malin.<br/>• Démocratisation de la Data de performance.<br/>• Extensibilité à d'autres sports (Rugby, Basket).", body_style),
            Paragraph("<b>MENACES (Threats)</b><br/>• Concurrence établie (Hudl, Wyscout).<br/>• Risque de verrouillage des APIs de données gratuites.<br/>• Résistance au changement des recruteurs traditionnels.", body_style)
        ]
    ]
    
    swot_table = Table(swot_data, colWidths=[240, 240])
    swot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")), 
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FEF2F2")), 
        ('BACKGROUND', (0,1), (0,1), colors.HexColor("#ECFDF5")), 
        ('BACKGROUND', (1,1), (1,1), colors.HexColor("#FFFBEB")), 
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('BOX', (0,0), (-1,-1), 1, primary_color),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(swot_table)
    story.append(PageBreak())
    
    # --- PAGE 3: SPECIFICATIONS FONCTIONNELLES & ROLES ---
    story.append(Paragraph("3. Spécifications Fonctionnelles", h1_style))
    story.append(Paragraph("3.1. Gestion des Utilisateurs et des Rôles (RBAC)", h2_style))
    story.append(Paragraph(
        "L'application implémente un contrôle d'accès basé sur les rôles (RBAC) pour sécuriser les données tactiques et financières :",
        body_style
    ))
    story.append(Paragraph("• <b>Administrateur (admin) :</b> Dispose de tous les droits. C'est le seul profil habilité à inscrire de nouveaux recruteurs via la route d'inscription `/register`.", bullet_style))
    story.append(Paragraph("• <b>Directeur Sportif (director) :</b> Accède au dashboard de recherche, aux fiches détaillées et à la totalité de l'outil de suivi de budget (données financières complètes).", bullet_style))
    story.append(Paragraph("• <b>Recruteur / Scout (scout) :</b> Accède à la recherche et à l'analyse de similarité de performance des joueurs (les données financières très sensibles peuvent être masquées).", bullet_style))
    
    story.append(Paragraph("3.2. Parcours Utilisateur & Fonctionnalités Clés", h2_style))
    story.append(Paragraph("1. <b>Authentification :</b> Écran de connexion sécurisé par Token JWT. Session expirant après 60 minutes.", bullet_style))
    story.append(Paragraph("2. <b>Module de Scouting (Recherche multicritère) :</b> L'utilisateur configure des curseurs (jauges de 0 à 100) pour définir son profil idéal :<br/>"
                           "   - <i>Critères Physiques :</i> Vitesse, Accélération, Endurance.<br/>"
                           "   - <i>Critères Techniques :</i> Finition, Dribble, Passes courtes, Tirs de loin.<br/>"
                           "   - <i>Filtres bloquants :</i> Poste (ex. Attaquant, Défenseur), Âge maximum, Fin de contrat (ex: 2026), Valeur et Salaire maximum.", bullet_style))
    story.append(Paragraph("3. <b>Moteur de Matching :</b> Calcule un score de compatibilité (%) en comparant les critères définis par le recruteur aux statistiques réelles des joueurs stockées en base de données. Les résultats sont triés par ordre décroissant de compatibilité.", bullet_style))
    story.append(Paragraph("4. <b>Fiche Joueur Détaillée :</b> Présente un profil complet du joueur sélectionné avec un graphique radar comparant ses aptitudes à la moyenne de son poste, et affiche sa situation financière et contractuelle.", bullet_style))
    story.append(Paragraph("5. <b>Suivi Budgétaire :</b> Permet de simuler l'impact financier d'un transfert sur l'enveloppe budgétaire globale du club.", bullet_style))
    
    story.append(Spacer(1, 10))
    
    # --- PAGE 4: SPECIFICATIONS TECHNIQUES ---
    story.append(Paragraph("4. Spécifications Techniques", h1_style))
    
    tech_header_style = ParagraphStyle('TechHeader', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.white)
    
    tech_data = [
        [Paragraph("<b>Composant</b>", tech_header_style), Paragraph("<b>Technologie</b>", tech_header_style), Paragraph("<b>Rôle & Justification</b>", tech_header_style)],
        [Paragraph("<b>Front-end</b>", body_style), Paragraph("React.js (JavaScript)", body_style), Paragraph("Fluidité, interface réactive et composants dynamiques (curseurs, listes).", body_style)],
        [Paragraph("<b>Visualisation</b>", body_style), Paragraph("Recharts / Chart.js", body_style), Paragraph("Affichage des graphiques radars interactifs sur les fiches des joueurs.", body_style)],
        [Paragraph("<b>Back-end (API)</b>", body_style), Paragraph("FastAPI (Python 3.12+)", body_style), Paragraph("Haute performance, typage statique et documentation interactive automatique.", body_style)],
        [Paragraph("<b>Logique Data</b>", body_style), Paragraph("Pandas, NumPy, Scikit-Learn", body_style), Paragraph("Manipulation des données de performance et calcul de distance (similarité KNN).", body_style)],
        [Paragraph("<b>Base de données</b>", body_style), Paragraph("SQLite / PostgreSQL", body_style), Paragraph("SQLite en local pour le développement rapide, PostgreSQL en production.", body_style)],
        [Paragraph("<b>Sécurité</b>", body_style), Paragraph("PyJWT, Bcrypt", body_style), Paragraph("Hachage sécurisé des mots de passe et gestion des sessions via jetons signés JWT.", body_style)]
    ]
    
    tech_table = Table(tech_data, colWidths=[100, 140, 240])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FAFB")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
        
    story.append(tech_table)
    story.append(PageBreak())
    
    # --- PAGE 5: BUDGET & COUTS ---
    story.append(Paragraph("5. Gestion et Suivi du Budget", h1_style))
    story.append(Paragraph("5.1. Fonctionnalité de Budgétisation dans l'Application (Club)", h2_style))
    story.append(Paragraph(
        "L'un des trois piliers du MVP est le module de suivi de budget de l'Olympique Lyonnais. Il permet au Directeur Sportif de :",
        body_style
    ))
    story.append(Paragraph("• <b>Simuler une transaction :</b> Calculer le coût complet d'une recrue en intégrant : "
                           "<i>l'Indemnité de transfert + le Salaire annuel + la Commission d'agent (estimée à 10%)</i>.", bullet_style))
    story.append(Paragraph("• <b>Visualiser l'impact budgétaire :</b> Une jauge interactive affiche en temps réel la part du budget consommée (ex. Enveloppe de 30 M€) et le solde restant après chaque simulation d'achat.", bullet_style))
    story.append(Paragraph("• <b>Rapport Qualité/Prix :</b> Calculer un ratio d'efficience statistique par rapport au coût financier (ex. <i>nombre d'interceptions réussies par million d'euros dépensé</i>) afin de maximiser le retour sur investissement.", bullet_style))

    story.append(Paragraph("5.2. Budget Estimatif de Réalisation et d'Exploitation (Projet)", h2_style))
    story.append(Paragraph(
        "Pour assurer le déploiement et la maintenance future de la plateforme, le budget prévisionnel est estimé ainsi :",
        body_style
    ))
    
    budget_rows = [
        [Paragraph("<b>Poste de Dépense</b>", tech_header_style), Paragraph("<b>Coût Estimé</b>", tech_header_style), Paragraph("<b>Description / Détails</b>", tech_header_style)],
        [Paragraph("<b>Hébergement & Cloud</b>", body_style), Paragraph("15 € / mois", body_style), Paragraph("Hébergement FastAPI sur Railway, base PostgreSQL managée et Vercel pour le Front-end.", body_style)],
        [Paragraph("<b>API de Données Foot</b>", body_style), Paragraph("0 € (Dev) -> 120 €/mois", body_style), Paragraph("Données Open Source en développement, puis abonnement API professionnel intermédiaire en production.", body_style)],
        [Paragraph("<b>Développement (MVP)</b>", body_style), Paragraph("10 000 € (Interne)", body_style), Paragraph("Phase de conception, développement backend, intégration algorithmique et frontend (15-20 jours/homme).", body_style)],
        [Paragraph("<b>Maintenance & Support</b>", body_style), Paragraph("500 € / an", body_style), Paragraph("Mises à jour de sécurité des dépendances (FastAPI/React) et renouvellement des domaines.", body_style)]
    ]
    
    budget_table = Table(budget_rows, colWidths=[130, 110, 240])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FAFB")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(budget_table)
    story.append(PageBreak())
    
    # --- PAGE 6: ROADMAP & MOSCOW ---
    story.append(Paragraph("6. Roadmap & Priorisation (MoSCoW)", h1_style))
    story.append(Paragraph("• <b>Must have (Indispensable) :</b> Connexion JWT avec rôles, base SQLite joueurs, moteur de recherche et calcul de similarité, affichage des résultats triés.", bullet_style))
    story.append(Paragraph("• <b>Should have (Important) :</b> Création de listes de favoris (shortlists), exportation de rapports PDF sur un joueur, graphiques radars interactifs.", bullet_style))
    story.append(Paragraph("• <b>Could have (Optionnel) :</b> Recommandations par Intelligence Artificielle (modèles prédictifs), messagerie de contact directe avec les agents de joueurs.", bullet_style))
    story.append(Paragraph("• <b>Won't have (Hors scope) :</b> Négociation en ligne de contrats, intégration de flux vidéo en direct.", bullet_style))
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF mis à jour avec succès !")

if __name__ == "__main__":
    create_specification_pdf()
