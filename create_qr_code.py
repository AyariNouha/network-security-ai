import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_professional_qr(url, output_filename="qr_code_projet.png"):
    """
    Créer un QR Code professionnel avec logo circulaire
    """
    
    # Configuration QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Haute correction pour logo
        box_size=15,
        border=4,
    )
    
    # Ajouter données
    qr.add_data(url)
    qr.make(fit=True)
    
    # Créer image QR
    qr_img = qr.make_image(fill_color="#1e3c72", back_color="white").convert('RGB')
    
    # Dimensions
    qr_width, qr_height = qr_img.size
    
    # Créer logo circulaire au centre
    logo_size = qr_width // 5
    
    # Créer un cercle pour le logo
    logo_circle = Image.new('RGB', (logo_size, logo_size), '#1e3c72')
    draw = ImageDraw.Draw(logo_circle)
    
    # Dessiner cercle avec icône shield
    draw.ellipse([0, 0, logo_size, logo_size], fill='#1e3c72', outline='white', width=5)
    
    # Ajouter texte "AI" au centre (simple)
    try:
        font = ImageFont.truetype("arial.ttf", logo_size // 3)
    except:
        font = ImageFont.load_default()
    
    # Texte centré
    text = "🛡️"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((logo_size - text_width) // 2, (logo_size - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    # Créer masque circulaire
    mask = Image.new('L', (logo_size, logo_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, logo_size, logo_size], fill=255)
    
    # Appliquer le logo au centre du QR code
    logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    qr_img.paste(logo_circle, logo_position, mask)
    
    # Sauvegarder
    qr_img.save(output_filename, quality=95)
    print(f"✅ QR Code créé: {output_filename}")
    print(f"📐 Dimensions: {qr_width}x{qr_height} pixels")
    
    return output_filename

def create_qr_slide_image(url, title="AI NETWORK SECURITY", output="qr_slide.png"):
    """
    Créer une image complète pour slide avec QR code
    """
    
    # Créer QR code d'abord
    qr_file = create_professional_qr(url, "temp_qr.png")
    
    # Dimensions du slide (1200x675 pour 16:9)
    slide_width = 1200
    slide_height = 675
    
    # Créer fond
    slide = Image.new('RGB', (slide_width, slide_height), '#f8f9fa')
    draw = ImageDraw.Draw(slide)
    
    # Titre en haut
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        text_font = ImageFont.truetype("arial.ttf", 36)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Dessiner titre
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((slide_width - title_width) // 2, 50), title, fill='#1e3c72', font=title_font)
    
    # Charger QR code
    qr_img = Image.open(qr_file)
    qr_img = qr_img.resize((400, 400), Image.Resampling.LANCZOS)
    
    # Positionner QR code à gauche
    qr_position = (150, (slide_height - 400) // 2)
    slide.paste(qr_img, qr_position)
    
    # Texte "SCAN ME" à droite
    scan_x = 650
    scan_y = 200
    
    draw.text((scan_x, scan_y), "SCAN", fill='#1e3c72', font=title_font)
    draw.text((scan_x, scan_y + 70), "ME", fill='#2a5298', font=title_font)
    
    # Features list
    features = [
        "✓ Code Source Complet",
        "✓ 3 Modèles ML",
        "✓ Docker Ready",
        "✓ Documentation",
    ]
    
    features_y = scan_y + 180
    for i, feature in enumerate(features):
        draw.text((scan_x, features_y + i * 40), feature, fill='#555', font=small_font)
    
    # Footer
    draw.text((50, slide_height - 50), "GitHub Repository", fill='#999', font=small_font)
    
    # Sauvegarder
    slide.save(output, quality=95)
    print(f"✅ Slide complet créé: {output}")
    
    # Nettoyer
    os.remove(qr_file)
    
    return output

if __name__ == "__main__":
    # REMPLACER PAR VOTRE URL
    github_url = "https://github.com/AyariNouha/network-security-ai"
    
    # Option 1: QR Code simple
    create_professional_qr(github_url, "qr_code_github.png")
    
    # Option 2: Slide complet
    create_qr_slide_image(github_url, "AI NETWORK SECURITY", "qr_slide_complet.png")
    
    print("\n✅ TERMINÉ!")
    print("📁 Fichiers créés:")
    print("   - qr_code_github.png (QR simple)")
    print("   - qr_slide_complet.png (Slide complet)")