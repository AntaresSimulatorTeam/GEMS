# YAML Dynamic Loader - Documentation Technique

## 📋 Table des matières

1. [Architecture](#architecture)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Utilisation](#utilisation)
5. [API](#api)
6. [Validation](#validation)
7. [Gestion des erreurs](#gestion-des-erreurs)
8. [Dépannage](#dépannage)

---

## Architecture

### Components

```
┌─────────────────────────────────────────────────────┐
│           Documentation MkDocs                       │
├─────────────────────────────────────────────────────┤
│  Markdown avec <div data-yaml-url="..."></div>      │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│        YAML Dynamic Loader (JavaScript)             │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │  yaml-loader.js                              │   │
│  │  - Initialisation automatique                │   │
│  │  - Chargement du YAML (fetch)                │   │
│  │  - Parsing (js-yaml)                         │   │
│  │  - Validation                                │   │
│  │  - Rendu HTML                                │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  yaml-loader.css                             │   │
│  │  - Styles boutons                            │   │
│  │  - Styles contenu                            │   │
│  │  - Support thème sombre                      │   │
│  └─────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│    Dépendances JavaScript externes (CDN)            │
├─────────────────────────────────────────────────────┤
│  - js-yaml@4.1.0 (jsDelivr)                         │
└─────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│    GitHub (raw.githubusercontent.com)               │
├─────────────────────────────────────────────────────┤
│  - Fichiers YAML publics                            │
│  - Accès via CORS (autorisé)                        │
└─────────────────────────────────────────────────────┘
```

### Flux de chargement

```
1. Page Markdown chargée
   ↓
2. DOMContentLoaded déclenche initializeYAMLLoaders()
   ↓
3. Récupération des éléments avec [data-yaml-url]
   ↓
4. fetch() → GitHub (raw.githubusercontent.com)
   ↓
5. jsyaml.load() → Parse YAML
   ↓
6. validateYAMLStructure() → Validation
   ↓
7. renderYAMLContent() → Génération HTML
   ↓
8. Affichage dans le conteneur
```

---

## Installation

### Étape 1 : Fichiers à ajouter

Les fichiers suivants doivent être présents dans votre projet :

```
doc/
  ├── javascripts/
  │   ├── mathjax.js              (existant)
  │   └── yaml-loader.js          (nouveau)
  ├── stylesheets/
  │   └── yaml-loader.css         (nouveau)
  └── 3_User_Guide/
      └── yaml_loader_guide.md    (nouveau)

resources/
  └── yaml-loader-example.yaml    (exemple)
```

### Étape 2 : Configuration mkdocs.yml

Vérifiez que les lignes suivantes sont présentes dans `mkdocs.yml` :

```yaml
extra_javascript:
  - javascripts/mathjax.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
  # YAML Dynamic Loader - Dependencies
  - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
  # YAML Dynamic Loader - Custom script
  - javascripts/yaml-loader.js

extra_css:
  - stylesheets/yaml-loader.css
```

### Étape 3 : Tester l'installation

Lancez la documentation localement :

```bash
cd /home/gmaistre/Documents/GEMS/GEMS
mkdocs serve
```

Puis ouvrez http://localhost:8000 dans votre navigateur.

---

## Configuration

### Variables JavaScript

Les variables de configuration se trouvent au début de `yaml-loader.js` :

```javascript
const CONFIG = {
    CONTAINER_CLASS: 'yaml-loader-container',    // Classe du conteneur
    BUTTON_CLASS: 'yaml-loader-button',           // Classe des boutons
    CONTENT_CLASS: 'yaml-loader-content',         // Classe du contenu
    ERROR_CLASS: 'yaml-loader-error',             // Classe des erreurs
    LOADING_CLASS: 'yaml-loader-loading',         // Classe de chargement
};
```

### Styles CSS personnalisables

Les variables CSS peuvent être surchargées dans `yaml-loader.css` :

```css
/* Couleur primaire (bleu) */
.yaml-loader-button {
    border-color: #0066cc;
    color: #0066cc;
}

.yaml-loader-button.active {
    background-color: #0066cc;
}

/* Vous pouvez personnaliser ces couleurs */
```

---

## Utilisation

### Méthode 1 : Attribut HTML (recommandée)

La plus simple et la plus courante :

```html
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/owner/repo/branch/path/file.yaml"></div>
```

### Méthode 2 : JavaScript manuel

Pour un contrôle avancé :

```html
<div id="my-container" class="yaml-loader-container"></div>

<script>
const container = document.getElementById('my-container');
const url = 'https://raw.githubusercontent.com/owner/repo/branch/path/file.yaml';
window.loadYAMLFile(container, url);
</script>
```

### Exemple complet dans un fichier Markdown

```markdown
# Exemple : Afficher une configuration

Voici la configuration disponible :

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml"></div>

Cliquez sur les boutons pour afficher les différentes sections.
```

---

## API

### Fonction publique : `window.loadYAMLFile(container, yamlUrl)`

Charge et affiche un fichier YAML dans un conteneur.

**Paramètres :**
- `container` (HTMLElement) : Élément DOM où afficher le contenu
- `yamlUrl` (string) : URL brute du fichier YAML sur GitHub

**Exemple :**

```javascript
const container = document.getElementById('yaml-container');
const url = 'https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml';

window.loadYAMLFile(container, url)
    .then(() => console.log('YAML chargé avec succès'))
    .catch(error => console.error('Erreur :', error));
```

### Fonctions internes (avancé)

| Fonction | Description |
|----------|-------------|
| `fetchYAML(url)` | Charge le contenu du fichier depuis l'URL |
| `parseYAML(yamlString)` | Parse la chaîne YAML en objet JavaScript |
| `validateYAMLStructure(data)` | Valide la structure des données |
| `renderYAMLContent(data, container)` | Génère et affiche le HTML |
| `displayError(container, message)` | Affiche un message d'erreur |
| `escapeHtml(text)` | Échappe les caractères HTML |
| `initializeYAMLLoaders()` | Initialise tous les conteneurs sur la page |

---

## Validation

### Schéma YAML requis

```yaml
sections:                          # Obligatoire : tableau
  - title: "string"                # Obligatoire : titre de la section
    content: |                     # Obligatoire : contenu brut
      Texte brut
      Peut contenir plusieurs lignes
```

### Validations effectuées

```javascript
✓ L'objet root est un objet JavaScript
✓ La propriété 'sections' existe
✓ 'sections' est un tableau
✓ Le tableau 'sections' n'est pas vide
✓ Chaque section est un objet
✓ Chaque section a une propriété 'title' de type string
✓ Chaque section a une propriété 'content' de type string
```

### Exemples valides

```yaml
# ✅ Valide - Exemple simple
sections:
  - title: "Section 1"
    content: |
      Contenu
  - title: "Section 2"
    content: |
      Contenu 2
```

```yaml
# ✅ Valide - Contenu multi-lignes
sections:
  - title: "Configuration"
    content: |
      param1: value1
      param2: value2
      param3: value3
```

### Exemples invalides

```yaml
# ❌ Invalide - Pas de sections
title: "Document"
content: "..."

# ❌ Invalide - sections n'est pas un tableau
sections:
  title: "Section"
  content: "..."

# ❌ Invalide - Sections vide
sections: []

# ❌ Invalide - Section sans title
sections:
  - content: "..."

# ❌ Invalide - Type de content incorrect
sections:
  - title: "Section"
    content: ["array", "instead", "of", "string"]
```

---

## Gestion des erreurs

### Types d'erreurs retournées

#### 1. Erreur HTTP

```
❌ Erreur: Impossible de charger le fichier YAML: Erreur HTTP 404: Not Found
```

**Cause** : URL incorrecte ou fichier supprimé
**Solution** : Vérifiez l'URL dans le navigateur

#### 2. Erreur de parsing YAML

```
❌ Erreur: Erreur lors du parsing YAML: undefined is not iterable
```

**Cause** : Syntaxe YAML invalide
**Solution** : Testez votre YAML avec [yamllint.com](https://www.yamllint.com/)

#### 3. Erreur de validation

```
❌ Erreur: La section 0 doit avoir une propriété "title" de type string.
```

**Cause** : Structure ne respecte pas le schéma
**Solution** : Vérifiez la structure YAML ci-dessus

#### 4. Erreur de bibliothèque

```
❌ Erreur: La bibliothèque js-yaml n'est pas chargée.
```

**Cause** : js-yaml non chargée dans mkdocs.yml
**Solution** : Vérifiez la configuration mkdocs.yml

### Gestion programmatique des erreurs

```javascript
const container = document.getElementById('my-container');
const url = 'https://raw.githubusercontent.com/.../file.yaml';

window.loadYAMLFile(container, url);

// Écouter les clics sur les boutons
container.addEventListener('click', (event) => {
    if (event.target.classList.contains('yaml-loader-button')) {
        console.log('Section cliquée :', event.target.textContent);
    }
});

// Écouter les erreurs (via le DOM)
const errorDiv = container.querySelector('.yaml-loader-error');
if (errorDiv) {
    console.error('Erreur détectée :', errorDiv.textContent);
}
```

---

## Dépannage

### Problème 1 : Conteneur blanc, rien n'apparaît

**Diagnostic :**
1. Ouvrez la console navigateur (F12)
2. Vérifiez qu'il n'y a pas d'erreurs JavaScript
3. Vérifiez que js-yaml est chargée : `console.log(typeof jsyaml)`

**Solutions :**
- Rechargez la page (Ctrl+F5)
- Vérifiez la configuratio de mkdocs.yml
- Vérifiez que la connexion internet fonctionne

### Problème 2 : Erreur "js-yaml n'est pas chargée"

**Solution :**
```yaml
# mkdocs.yml
extra_javascript:
  # ✅ Cet ordre est important !
  - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
  - javascripts/yaml-loader.js
```

### Problème 3 : Chargement infini

**Causes possibles :**
- Fichier YAML trop volumineux (>100 KB)
- Serveur GitHub surchargé
- Connexion internet lente

**Solution :**
- Attendez quelques secondes
- Testez l'URL directement : `https://raw.githubusercontent.com/.../file.yaml`

### Problème 4 : Erreur CORS

**Cause** : Domaine non autorisé par CORS

**Solution :**
- Utilisez uniquement des URLs `raw.githubusercontent.com`
- Ne téléchargez pas depuis d'autres domaines

### Problème 5 : Les boutons ne réagissent pas aux clics

**Causes possibles :**
- CSS non chargé
- Conflit JavaScript

**Solutions :**
1. Vérifiez que `yaml-loader.css` est chargé :
   ```bash
   # Dans la console navigateur
   console.log(document.styleSheets)
   ```

2. Testez en mode anonyme (cache vidé)

3. Vérifiez qu'il n'y a pas d'autres scripts qui interféreraient

### Problème 6 : Caractères spéciaux affichés incorrectement

**Solution :** Les caractères HTML sont échappés automatiquement. Si vous voyez des codes comme `&lt;`, c'est normal.

### Console debug

Enables les logs de debug en ajoutant ce code dans votre navigateur :

```javascript
// Dans la Console (F12)
window.DEBUG_YAML_LOADER = true;

// Puis dans yaml-loader.js, ajoutez :
if (window.DEBUG_YAML_LOADER) {
    console.log('Chargement :', yamlUrl);
    console.log('Validation :', validation);
    console.log('Données :', data);
}
```

---

## Exemples avancés

### Charger plusieurs fichiers YAML

```markdown
### Configuration de base
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../config1.yaml"></div>

### Configuration avancée
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../config2.yaml"></div>
```

### Charger dynamiquement depuis une liste

```html
<select id="config-selector">
    <option value="https://raw.githubusercontent.com/.../config1.yaml">Config 1</option>
    <option value="https://raw.githubusercontent.com/.../config2.yaml">Config 2</option>
</select>

<div id="yaml-container" class="yaml-loader-container"></div>

<script>
document.getElementById('config-selector').addEventListener('change', function(e) {
    const container = document.getElementById('yaml-container');
    window.loadYAMLFile(container, e.target.value);
});
</script>
```

---

## Performance et optimisation

### Taille maximale
- Fichiers < 100 KB recommandé
- jsDelivr CDN gère bien jusqu'à ~1 MB

### Mise en cache
- Le navigateur cache automatiquement les fichiers
- Pas de cache serveur MkDocs
- Cache CORS + CDN jsDelivr

### Optimisation des URLs
```javascript
// ✅ Optimal - Branche main
https://raw.githubusercontent.com/owner/repo/main/file.yaml

// ❌ À éviter - Branche compliquée
https://raw.githubusercontent.com/owner/repo/feature/very/long/branch/name/file.yaml
```

---

## Support et contribution

### Signaler un bug

1. Ouvrez une issue sur [GitHub](https://github.com/AntaresSimulatorTeam/GEMS/issues)
2. Incluez :
   - URL du fichier YAML
   - Log console (F12)
   - Étapes pour reproduire

### Améliorer la solution

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](../../6_Support_Contributing/3_contributing.md).

---

**Dernière mise à jour** : 17 février 2026
**Version** : 1.0.0
