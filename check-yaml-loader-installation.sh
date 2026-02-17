#!/usr/bin/env bash

########################################
# INSTALLATION CHECKER - YAML Dynamic Loader
# Vérifiez que tout est correctement installé
########################################

echo "🔍 YAML Dynamic Loader - Vérification d'installation"
echo "================================================="
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Compteurs
CHECKS_PASSED=0
CHECKS_FAILED=0

# Fonction de vérification
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} Fichier trouvé: $1"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} Fichier MANQUANT: $1"
        ((CHECKS_FAILED++))
    fi
}

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Contenu trouvé dans: $1"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} Contenu MANQUANT dans: $1"
        ((CHECKS_FAILED++))
    fi
}

# ========================================
# Vérifications des fichiers JavaScript/CSS
# ========================================
echo "📦 Fichiers JavaScript et CSS"
echo "----"
check_file "doc/javascripts/yaml-loader.js"
check_file "doc/stylesheets/yaml-loader.css"
echo ""

# ========================================
# Vérifications de la configuration MkDocs
# ========================================
echo "⚙️  Configuration mkdocs.yml"
echo "----"
check_content "mkdocs.yml" "js-yaml"
check_content "mkdocs.yml" "yaml-loader.js"
check_content "mkdocs.yml" "yaml-loader.css"
echo ""

# ========================================
# Vérifications de la documentation
# ========================================
echo "📚 Fichiers de documentation"
echo "----"
check_file "doc/3_User_Guide/yaml_loader_guide.md"
check_file "doc/3_User_Guide/yaml_loader_integration_example.md"
check_file "doc/YAML_LOADER_TECHNICAL.md"
check_file "YAML_LOADER_README.md"
check_file "resources/yaml-loader-example.yaml"
echo ""

# ========================================
# Résumé
# ========================================
echo "📊 Résumé"
echo "========"
echo -e "Vérifications réussies: ${GREEN}${CHECKS_PASSED}${NC}"
echo -e "Vérifications échouées: ${RED}${CHECKS_FAILED}${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Installation réussie !${NC}"
    echo ""
    echo "🚀 Prochaines étapes :"
    echo "  1. Lancez la documentation : mkdocs serve"
    echo "  2. Consultez le guide d'utilisation :"
    echo "     doc/3_User_Guide/yaml_loader_guide.md"
    echo "  3. Regardez les exemples :"
    echo "     doc/3_User_Guide/yaml_loader_integration_example.md"
    exit 0
else
    echo -e "${RED}✗ Installation incomplète !${NC}"
    echo ""
    echo "❌ Fichiers manquants ou erreurs détectées."
    echo "Consultez YAML_LOADER_README.md pour plus d'informations."
    exit 1
fi
