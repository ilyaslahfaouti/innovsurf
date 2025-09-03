#!/usr/bin/env python3
"""
Script de création de captures d'écran de tous les fichiers de test
Génère des images PNG de chaque fichier pour documentation
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import subprocess
import time

class FileScreenshotCreator:
    def __init__(self, output_dir="file_screenshots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Liste des fichiers à capturer
        self.files_to_capture = [
            "quick_test.sh",
            "setup_api_testing.sh", 
            "setup_test_user.py",
            "simple_api_tester.py",
            "api_screenshot_tool.py",
            "test_forecast_api.py",
            "smart_api_tester.py",
            "fix_auth.py",
            "README_API_TESTING.md",
            "README_FINAL.md"
        ]
    
    def get_file_content(self, filename):
        """Lire le contenu d'un fichier"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erreur de lecture: {e}"
    
    def get_file_info(self, filename):
        """Obtenir les informations d'un fichier"""
        try:
            stat = os.stat(filename)
            size = stat.st_size
            modified = time.ctime(stat.st_mtime)
            return size, modified
        except:
            return 0, "N/A"
    
    def create_file_screenshot(self, filename):
        """Créer une capture d'écran d'un fichier"""
        try:
            print(f"📸 Création de la capture pour {filename}...")
            
            # Lire le contenu
            content = self.get_file_content(filename)
            size, modified = self.get_file_info(filename)
            
            # Déterminer l'extension pour la coloration
            ext = os.path.splitext(filename)[1].lower()
            
            # Dimensions de l'image
            width = 1400
            line_height = 20
            max_lines = 80
            
            # Calculer la hauteur nécessaire
            lines = content.split('\n')
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                content = '\n'.join(lines) + '\n\n... (contenu tronqué)'
            
            height = 200 + (len(lines) * line_height)
            
            # Créer l'image
            img = Image.new('RGB', (width, height), color='#1e1e1e')  # Fond sombre
            draw = ImageDraw.Draw(img)
            
            # Essayer de charger une police
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
                font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
            except:
                try:
                    font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
                    font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
                    font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
                except:
                    font_large = ImageFont.load_default()
                    font_medium = ImageFont.load_default()
                    font_small = ImageFont.load_default()
            
            # En-tête
            header_bg = '#2d2d30'
            draw.rectangle([0, 0, width, 80], fill=header_bg)
            
            # Titre du fichier
            draw.text((20, 20), f"📁 {filename}", fill='#ffffff', font=font_large)
            
            # Informations du fichier
            info_text = f"Taille: {size:,} octets | Modifié: {modified}"
            draw.text((20, 50), info_text, fill='#cccccc', font=font_small)
            
            # Ligne de séparation
            draw.line([(20, 80), (width-20, 80)], fill='#404040', width=2)
            
            # Contenu du fichier avec coloration syntaxique
            y_position = 100
            
            for i, line in enumerate(lines):
                if y_position > height - 50:
                    break
                
                # Couper les lignes trop longues
                if len(line) > 120:
                    line = line[:117] + "..."
                
                # Couleur selon le type de fichier
                if ext in ['.py', '.sh']:
                    # Fichiers de code
                    if line.strip().startswith('#'):
                        color = '#6a9955'  # Commentaires verts
                    elif line.strip().startswith('def ') or line.strip().startswith('class '):
                        color = '#dcdcaa'  # Définitions jaunes
                    elif line.strip().startswith('import ') or line.strip().startswith('from '):
                        color = '#569cd6'  # Imports bleus
                    elif '=' in line and ':' in line:
                        color = '#9cdcfe'  # Variables bleu clair
                    else:
                        color = '#d4d4d4'  # Texte normal blanc
                elif ext == '.md':
                    # Fichiers Markdown
                    if line.strip().startswith('#'):
                        color = '#569cd6'  # Titres bleus
                    elif line.strip().startswith('- ') or line.strip().startswith('* '):
                        color = '#ce9178'  # Listes orange
                    elif line.strip().startswith('```'):
                        color = '#dcdcaa'  # Blocs de code jaunes
                    else:
                        color = '#d4d4d4'  # Texte normal blanc
                else:
                    color = '#d4d4d4'  # Texte normal
                
                # Afficher la ligne
                draw.text((20, y_position), line, fill=color, font=font_small)
                y_position += line_height
            
            # Pied de page
            footer_bg = '#2d2d30'
            draw.rectangle([0, height-40, width, height], fill=footer_bg)
            draw.text((20, height-30), f"Capture générée le {time.strftime('%Y-%m-%d %H:%M:%S')}", 
                     fill='#cccccc', font=font_small)
            
            # Sauvegarder l'image
            output_filename = f"{self.output_dir}/{filename.replace('.', '_').replace('/', '_')}_screenshot.png"
            img.save(output_filename, dpi=(300, 300))
            
            print(f"✅ Capture sauvegardée: {output_filename}")
            return output_filename
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la capture pour {filename}: {e}")
            return None
    
    def create_overview_screenshot(self):
        """Créer une capture d'ensemble de tous les fichiers"""
        try:
            print("📸 Création de la capture d'ensemble...")
            
            # Dimensions
            width = 1600
            height = 1200
            
            # Créer l'image
            img = Image.new('RGB', (width, height), color='#1e1e1e')
            draw = ImageDraw.Draw(img)
            
            # Essayer de charger une police
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 24)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
                font_small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
            except:
                try:
                    font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                    font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
                    font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
                except:
                    font_large = ImageFont.load_default()
                    font_medium = ImageFont.load_default()
                    font_small = ImageFont.load_default()
            
            # Titre principal
            title = "🖼️ Suite Complète des Outils de Test des APIs InnovSurf"
            draw.text((width//2 - len(title)*8, 30), title, fill='#ffffff', font=font_large)
            
            # Ligne de séparation
            draw.line([(50, 80), (width-50, 80)], fill='#404040', width=3)
            
            # Description
            description = "Collection complète d'outils pour tester, documenter et capturer vos APIs avec des captures d'écran automatiques"
            draw.text((width//2 - len(description)*6, 110), description, fill='#cccccc', font=font_medium)
            
            # Catégories de fichiers
            categories = {
                "🚀 Scripts de Lancement": ["quick_test.sh", "setup_api_testing.sh"],
                "🔧 Outils de Configuration": ["setup_test_user.py"],
                "🧪 Outils de Test": ["simple_api_tester.py", "api_screenshot_tool.py", "test_forecast_api.py", "smart_api_tester.py", "fix_auth.py"],
                "📚 Documentation": ["README_API_TESTING.md", "README_FINAL.md"]
            }
            
            y_position = 180
            for category, files in categories.items():
                # Titre de catégorie
                draw.text((50, y_position), category, fill='#569cd6', font=font_medium)
                y_position += 40
                
                # Fichiers de la catégorie
                for filename in files:
                    if os.path.exists(filename):
                        size, modified = self.get_file_info(filename)
                        file_info = f"  📁 {filename} ({size:,} octets)"
                        draw.text((70, y_position), file_info, fill='#d4d4d4', font=font_small)
                        y_position += 25
                    else:
                        file_info = f"  ❌ {filename} (non trouvé)"
                        draw.text((70, y_position), file_info, fill='#f44747', font=font_small)
                        y_position += 25
                
                y_position += 20
            
            # Statistiques
            y_position += 20
            draw.line([(50, y_position), (width-50, y_position)], fill='#404040', width=2)
            y_position += 30
            
            stats_text = f"📊 Statistiques: {len(self.files_to_capture)} fichiers | {len([f for f in self.files_to_capture if os.path.exists(f)])} existants"
            draw.text((50, y_position), stats_text, fill='#4ec9b0', font=font_medium)
            
            # Instructions d'utilisation
            y_position += 60
            instructions = [
                "🎯 Utilisation rapide:",
                "  ./quick_test.sh                    # Interface graphique",
                "  python3 fix_auth.py                # Test recommandé",
                "  python3 api_screenshot_tool.py     # Avec captures",
                "",
                "🔑 Identifiants de test:",
                "  Email: test@innovsurf.com",
                "  Password: testpass123"
            ]
            
            for instruction in instructions:
                if instruction.strip():
                    if instruction.startswith("🎯") or instruction.startswith("🔑"):
                        color = '#4ec9b0'
                        font = font_medium
                    elif instruction.startswith("  "):
                        color = '#d4d4d4'
                        font = font_small
                    else:
                        color = '#cccccc'
                        font = font_small
                    
                    draw.text((50, y_position), instruction, fill=color, font=font)
                    y_position += 25
            
            # Pied de page
            footer_bg = '#2d2d30'
            draw.rectangle([0, height-60, width, height], fill=footer_bg)
            draw.text((50, height-40), f"Généré le {time.strftime('%Y-%m-%d %H:%M:%S')} | InnovSurf API Testing Suite", 
                     fill='#cccccc', font=font_small)
            
            # Sauvegarder
            output_filename = f"{self.output_dir}/OVERVIEW_suite_complete.png"
            img.save(output_filename, dpi=(300, 300))
            
            print(f"✅ Capture d'ensemble sauvegardée: {output_filename}")
            return output_filename
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la capture d'ensemble: {e}")
            return None
    
    def create_all_screenshots(self):
        """Créer toutes les captures d'écran"""
        print("🖼️ Création des captures d'écran de tous les fichiers...")
        print("=" * 60)
        
        created_screenshots = []
        
        # Créer la capture d'ensemble
        overview = self.create_overview_screenshot()
        if overview:
            created_screenshots.append(overview)
        
        # Créer les captures individuelles
        for filename in self.files_to_capture:
            if os.path.exists(filename):
                screenshot = self.create_file_screenshot(filename)
                if screenshot:
                    created_screenshots.append(screenshot)
            else:
                print(f"⚠️  Fichier non trouvé: {filename}")
        
        # Résumé
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES CAPTURES CRÉÉES")
        print("=" * 60)
        print(f"Total des captures: {len(created_screenshots)}")
        
        for screenshot in created_screenshots:
            print(f"✅ {screenshot}")
        
        print(f"\n📁 Toutes les captures sont dans: {self.output_dir}/")
        print("🔍 Pour les visualiser: open file_screenshots/")
        
        return created_screenshots

def main():
    """Fonction principale"""
    print("🖼️ Créateur de Captures d'Écran des Fichiers InnovSurf")
    print("=" * 70)
    
    # Créer le créateur de captures
    creator = FileScreenshotCreator()
    
    # Créer toutes les captures
    screenshots = creator.create_all_screenshots()
    
    print(f"\n🎉 Création terminée ! {len(screenshots)} captures générées")

if __name__ == "__main__":
    main()
