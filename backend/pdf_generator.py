from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm

def generar_boleta(nombre, materias, promedios, archivo="boleta.pdf"):
    # 📄 CONFIGURACIÓN MILIMÉTRICA
    doc = SimpleDocTemplate(
        archivo,
        pagesize=letter,
        leftMargin=12*mm,
        rightMargin=12*mm,
        topMargin=10*mm,
        bottomMargin=10*mm
    )

    styles = getSampleStyleSheet()

    # 🎨 ESTILOS EXACTOS
    titulo = ParagraphStyle(
        name="titulo",
        parent=styles["Normal"],
        alignment=1,
        fontSize=14,
        leading=16
    )

    normal = ParagraphStyle(
        name="normal",
        parent=styles["Normal"],
        fontSize=8,
        leading=10
    )

    elementos = []

    # =========================
    # 🧾 HEADER EXACTO
    # =========================
    header = Table([
        [
            Paragraph(f"<b>{nombre}</b><br/>Grado: __________", normal),
            Paragraph("<b>DEL MONTE SCHOOL</b>", titulo),
            Paragraph(
                "<b>Profa. Español:</b><br/>_________________<br/><br/>"
                "<b>Teacher English:</b><br/>_________________",
                normal
            )
        ]
    ], colWidths=[70*mm, 60*mm, 60*mm], rowHeights=[30*mm])

    header.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.8, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (1,0), (1,0), "CENTER"),
    ]))

    elementos.append(header)
    elementos.append(Spacer(1, 6))

    # =========================
    # 📊 TABLA MATERIAS EXACTA
    # =========================
    data = [["ASIGNATURA", "P-I", "P-II", "P-III", "P-IV", "FINAL", "RECUP."]]

    for m in materias:
        data.append([
            m["materia"],
            m["P1"],
            m["P2"],
            m["P3"],
            m["P4"],
            m["final"],
            ""
        ])

    data.append([
        "PROMEDIO",
        promedios["P1"],
        promedios["P2"],
        promedios["P3"],
        promedios["P4"],
        promedios["final"],
        ""
    ])

    tabla = Table(
        data,
        colWidths=[65*mm, 15*mm, 15*mm, 15*mm, 15*mm, 18*mm, 17*mm],
        repeatRows=1
    )

    tabla.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E6E6E6")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ("FONTSIZE", (0,0), (-1,-1), 8),

        # PROMEDIO resaltado
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#F2F2F2")),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
    ]))

    # =========================
    # 📋 PANEL DERECHO AJUSTADO
    # =========================
    obs = [
        ["OBSERVACIONES Y ASISTENCIA"],
        ["☐ Cumple normas de convivencia"],
        ["☐ Interés por su rendimiento"],
        ["☐ Presentación personal"],
        ["☐ Finaliza trabajos"],
        ["☐ Participa activamente"],
        [""],
        ["ASISTENCIA: _______"]
    ]

    tabla_obs = Table(
        obs,
        colWidths=[55*mm],
        rowHeights=[8*mm]*len(obs)
    )

    tabla_obs.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E6E6E6")),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))

    # 🔗 BLOQUE CENTRAL PERFECTAMENTE ALINEADO
    bloque = Table([
        [tabla, tabla_obs]
    ], colWidths=[130*mm, 55*mm])

    elementos.append(bloque)
    elementos.append(Spacer(1, 8))

    # =========================
    # 💬 COMENTARIOS
    # =========================
    elementos.append(Paragraph("<b>COMENTARIOS DE LOS MAESTROS</b>", normal))
    elementos.append(Spacer(1, 4))

    comentarios = Table(
        [[""]],
        colWidths=[185*mm],
        rowHeights=[35*mm]
    )

    comentarios.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.5, colors.black)
    ]))

    elementos.append(comentarios)
    elementos.append(Spacer(1, 10))

    # =========================
    # ✍️ FIRMAS EXACTAS
    # =========================
    firmas = Table([
        ["PADRE DE FAMILIA", "PROF(A). ESPAÑOL", "TEACHER", "DIRECTOR"]
    ], colWidths=[46*mm]*4, rowHeights=[12*mm])

    firmas.setStyle(TableStyle([
        ("LINEABOVE", (0,0), (-1,0), 0.5, colors.black),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("VALIGN", (0,0), (-1,0), "BOTTOM"),
        ("FONTSIZE", (0,0), (-1,0), 8)
    ]))

    elementos.append(firmas)

    # =========================
    # 📄 GENERAR
    # =========================
    doc.build(elementos)