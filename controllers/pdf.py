import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table, TableStyle

from models import Quote


class Pdf:
    def __drawBasedCenteredText(
        self,
        c: Canvas,
        text_above: str,
        text_below: str,
        x: float,
        y: float,
        font1: str,
        size1: float,
        font2: str,
        size2: float,
        spacing: float,
    ) -> None:
        width_text1 = stringWidth(text_above, font1, size1)
        width_text2 = stringWidth(text_below, font2, size2)

        x_below = x + (width_text1 - width_text2) / 2

        c.setFont(font1, size1)
        c.drawString(x, y, text_above)

        c.setFont(font2, size2)
        c.drawString(x_below, y - spacing, text_below)

    def __drawNextText(
        self,
        c: Canvas,
        first_text: str,
        second_text: str,
        x: float,
        y: float,
        font1: str,
        size1: float,
        font2: str,
        size2: float,
        spacing: float,
    ) -> None:
        second_x = x + stringWidth(first_text, font1, size1) + spacing

        c.setFont(font1, size1)
        c.drawString(x, y, first_text)

        c.setFont(font2, size2)
        c.drawString(second_x, y, second_text)

    def generate_quote(self, quote: Quote) -> str:
        issuer_name = "Marcelo Renato Balestra Lemus"
        issuer_short_name = "Marcelo Balestra"
        issuer_phone = "461 147 7068"
        issuer_rfc = "BALM5309242P3"
        issuer_address = "CARRETERA CORTAZAR-JARAL KM. 9 C.P. 38480"
        cer_sanidad = "DGSA-DSAP-CSAUC-009|2024"
        u_economica = "11002350"
        u_acuicola = "11010196"

        page_size = letter
        width, height = page_size

        desktop = Path.home() / "Desktop"
        output_dir = desktop / "Cotizaciones"
        if not output_dir.exists():
            output_dir.mkdir()

        quote_number = f"{quote.folio}{str(quote.date.year)[-2:]}{quote.date.month}{quote.date.day}"
        output_path = str(
            output_dir
            / f"COTIZACIÓN {quote_number} {quote.customer.name.split()[0]}.pdf"
        )

        c = Canvas(output_path, pagesize=page_size)

        # Watermark
        img = ImageReader("./assets/tilapia.jpg")
        img_width, img_height = img.getSize()

        scale = 4 / 5
        new_width = img_width * scale
        new_height = img_height * scale
        c.saveState()
        c.setFillAlpha(0.15)

        c.drawImage(
            img,
            (width - new_width) / 2,
            ((height - new_height) / 2),
            width=new_width,
            height=new_height,
        )
        c.restoreState()

        # Logo
        c.drawImage("./assets/logo.jpg", 95, height - 230, width=175, height=175)

        # Folio
        c.setFont("Helvetica", 9.5)
        c.drawString(70, height - 60, f"Folio: {str(quote.folio).zfill(10)}")

        # Header
        half_width = width / 2
        self.__drawBasedCenteredText(
            c,
            issuer_name,
            f"R.F.C.    {issuer_rfc}",
            half_width + 65,
            height - 75,
            "Helvetica-Oblique",
            13,
            "Helvetica",
            11,
            23,
        )
        self.__drawBasedCenteredText(
            c,
            "CERTIFICADO DE SANIDAD ACUICOLA PARA UNIDADES DE CUARENTENA",
            cer_sanidad,
            half_width + 65,
            height - 117,
            "Helvetica",
            5.2,
            "Helvetica",
            9.5,
            15,
        )

        c.setFont("Helvetica", 10.8)
        c.drawString(
            half_width + 65, height - 154, f"U. ECONOMICA   R.N.P.A.  {u_economica}"
        )
        c.drawString(
            half_width + 65, height - 168, f"U. ACUÍCOLA       R.N.P.A.  {u_acuicola}"
        )
        c.setFont("Helvetica", 7.9)
        c.drawString(half_width + 65, height - 185, issuer_address)
        c.setFont("Helvetica", 10)
        c.drawString(half_width + 65, height - 203, "FECHA:")
        c.drawRightString(
            width - 55, height - 203, quote.date.strftime("%d de %B del %Y")
        )

        # Title
        c.setFont("Helvetica-Bold", 42)
        c.setFillColorRGB(59 / 255, 111 / 255, 178 / 255)
        c.drawCentredString(half_width, height - 270, "COTIZACIÓN")
        c.setFillColorRGB(0 / 255, 0 / 255, 0 / 255)

        # Client info
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, height - 303, "Atención a:")
        c.setFont("Helvetica", 10)
        c.drawString(115, height - 303, quote.customer.name)
        c.drawString(115, height - 315, quote.customer.address)

        # Leyend
        style = ParagraphStyle("Custom", firstLineIndent=30, fontSize=12, leading=16)
        leyend = "Por este medio pongo a su dispocisión la cotizacón de los productos solicitados, agradecemos su preferencia y amablemente nos ponemos a sus ordenes:"
        p = Paragraph(leyend, style)
        _, ph = p.wrapOn(c, width - 103, height)
        p.drawOn(c, 50, height - 326 - ph)

        # Content table
        data = [["CLAVE", "CONCEPTO", "TALLA", "CANTIDAD", "P. UNITARIO", "TOTAL"]]
        for r in quote.concepts:
            data.append(
                [
                    "5011432H",
                    r.concept,
                    r.size,
                    f"{r.quantity:,}",
                    f"$ {r.price}",
                    f"$ {r.quantity * r.price:,}",
                ]
            )

        for r in range(6 - len(data)):
            data.append([])

        table = Table(data, colWidths=[60, 195, 45, 65, 70, 70])

        styles = [
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 0), (-1, -1), (52 / 255, 81 / 255, 148 / 255)),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
        for i in range(1, len(data), 2):
            styles.append(
                ("BACKGROUND", (0, i), (-1, i), (217 / 255, 224 / 255, 241 / 255))
            )

        table.setStyle(TableStyle(styles))
        _, th = table.wrapOn(c, width, height)
        table.drawOn(c, 52.5, height - 393 - th)

        # Notes
        self.__drawNextText(
            c,
            "Vigencia:",
            quote.vigency,
            50,
            height - 540,
            "Helvetica-Bold",
            8,
            "Helvetica",
            8,
            5,
        )
        self.__drawNextText(
            c,
            "Forma de pago:",
            "50% anticipo y 50% al aviso de entrega",
            50,
            height - 552,
            "Helvetica-Bold",
            8,
            "Helvetica",
            8,
            5,
        )
        txt = "Entrega:"
        font = "Helvetica-Bold"
        size = 8

        x = 50
        y = height - 564
        second_x = x + stringWidth(txt, font, size) + 5

        c.setFont(font, size)
        c.drawString(x, y, txt)

        style = ParagraphStyle(
            "Custom",
            fontName="Helvetica",
            fontSize=size,
            leading=16,
            alignment=TA_JUSTIFY,
        )
        leyend = "Todos los organismos se empacan debidamente en ayuno 24 hrs. con parámetros óptimos para su traslado, la entrega se hará via terrestre en nuestras instalaciones o en las instalaciones del cliente junto con su analisis bactereologico por un laboratorio autorizado por SENASICA"

        p = Paragraph(leyend, style)
        _, ph = p.wrapOn(c, half_width + 17.5, height)
        p.drawOn(c, second_x, y - ph + 7)

        # Totales
        c.setFont("Helvetica-Oblique", 10)
        c.drawRightString(width - 125, height - 555, "SUB-TOTAL")
        c.drawRightString(width - 125, height - 570, "I.V.A.")
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(width - 125, height - 585, "TOTAL")

        c.setFont("Helvetica", 10)
        c.drawRightString(width - 55, height - 555, f"$ {quote.subtotal:,}")
        c.drawCentredString(width - 75, height - 570, f"{quote.iva*100}%")
        c.drawRightString(width - 55, height - 585, f"$ {quote.total:,}")

        # Signs
        half_half = half_width / 2
        issuer_x = half_half + 25
        client_x = half_width + half_half - 25

        scale = 2 / 6

        c.drawImage(
            "./assets/sign.png",
            issuer_x - 70,
            height - 735,
            width=366 * scale,
            height=212 * scale,
        )

        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(issuer_x, height - 665, "ATENTAMENTE")
        c.drawCentredString(client_x, height - 665, "RECIBIDO")

        c.drawCentredString(issuer_x, height - 725, "_________________________")
        c.drawCentredString(client_x, height - 725, "_________________________")

        c.drawCentredString(issuer_x, height - 740, issuer_short_name)
        c.drawCentredString(client_x, height - 740, quote.customer.name)

        c.setFont("Helvetica", 10)
        c.drawCentredString(issuer_x, height - 753, f"Tel. {issuer_phone}")

        c.save()
        return str(output_dir)
