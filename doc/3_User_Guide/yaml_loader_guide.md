# Guide d'utilisation : YAML Dynamic Loader

Ce guide explique comment intégrer et utiliser le **YAML Dynamic Loader** dans votre documentation MkDocs pour afficher dynamiquement des fichiers YAML depuis GitHub.

## Vue d'ensemble

Le **YAML Dynamic Loader** est une solution JavaScript clé en main qui permet de :

- ✅ Charger dynamiquement des fichiers YAML publics depuis GitHub
- ✅ Parser et valider automatiquement leur structure
- ✅ Générer des boutons interactifs pour naviguer entre les sections
- ✅ Afficher le contenu brut sans conversion supplémentaire
- ✅ Gérer les erreurs avec des messages clairs

## Configuration initiale

### 1. Vérifier la configuration `mkdocs.yml`

La configuration suivante doit être présente dans votre `mkdocs.yml` :

```yaml
extra_javascript:
  # ... autres scripts ...
  - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
  - javascripts/yaml-loader.js

extra_css:
  - stylesheets/yaml-loader.css
```

✅ **Statut** : Cette configuration est déjà en place dans votre projet.

### 2. Structure requise du fichier YAML

Vos fichiers YAML doivent respecter cette structure standardisée :

```yaml
sections:
  - title: "Titre de la première section"
    content: |
      Contenu brut de la section.
      Peut contenir plusieurs lignes.
      Pas de formatage Markdown.
  - title: "Titre de la deuxième section"
    content: |
      Contenu brut de la deuxième section.
```

## Utilisation dans Markdown

### Méthode 1 : Utilisation simple avec attribut HTML

Créez un conteneur vide avec l'attribut `data-yaml-url` pointant vers votre fichier YAML :

```html
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/owner/repo/branch/path/to/file.yaml"></div>
```

### Exemple concret

Si vous souhaitez afficher le fichier `basic_models_library.yml` du dépôt GEMS :

```html
<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml"></div>
```

### Méthode 2 : Utilisation JavaScript manuelle

Si vous avez besoin de charger un fichier YAML sans utiliser l'attribut HTML :

```html
<div id="my-yaml-container" class="yaml-loader-container"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('my-yaml-container');
    const yamlUrl = 'https://raw.githubusercontent.com/owner/repo/branch/path/to/file.yaml';
    window.loadYAMLFile(container, yamlUrl);
});
</script>
```

## Validation de la structure YAML

Le YAML Dynamic Loader valide automatiquement la structure de votre fichier. Les vérifications effectuées sont :

| Vérification | Message d'erreur |
|---|---|
| Propriété `sections` manquante | "Le fichier YAML doit contenir une propriété 'sections' qui est un tableau." |
| `sections` n'est pas un tableau | "La propriété 'sections' doit être un tableau." |
| Tableau `sections` vide | "Le tableau 'sections' ne peut pas être vide." |
| Section sans propriété `title` | "Chaque section doit avoir une propriété 'title' de type string." |
| Section sans propriété `content` | "Chaque section doit avoir une propriété 'content' de type string." |
| Fichier introuvable | "Erreur HTTP 404: Not Found" |

## Gestion des erreurs

Si une erreur survient, un message d'erreur s'affiche automatiquement dans le conteneur avec les informations suivantes :

### Types d'erreurs gérées

1. **Erreur de chargement (HTTP)** : Fichier introuvable ou serveur inaccessible
2. **Erreur de parsing** : Structure YAML invalide
3. **Erreur de validation** : Structure ne correspond pas au schéma attendu
4. **Erreur de bibliothèque** : js-yaml non chargée

### Exemple de message d'erreur

```
❌ Erreur: Le fichier YAML doit contenir une propriété "sections" qui est un tableau.
```

## Style et personnalisation

### Classe CSS principales

```css
/* Conteneur principal */
.yaml-loader-container { }

/* Boutons de navigation */
.yaml-loader-button { }
.yaml-loader-button.active { }

/* Zone de contenu */
.yaml-loader-content { }

/* Messages d'erreur */
.yaml-loader-error { }

/* État de chargement */
.yaml-loader-loading { }
```

### Thème sombre

Les styles s'ajustent automatiquement selon le thème du navigateur (light/dark) grâce à la directive `@media (prefers-color-scheme: dark)`.

## Cas d'usage pratiques

### Cas 1 : Afficher une configuration de modèle

Vous avez un fichier `models-config.yaml` sur GitHub :

```markdown
## Configuration des modèles

Les modèles disponibles sont listés ci-dessous :

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/models-config.yaml"></div>
```

### Cas 2 : Documentation avec plusieurs fichiers YAML

Vous pouvez afficher plusieurs fichiers YAML sur la même page :

```markdown
## Configuration de base

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../config1.yaml"></div>

## Configuration avancée

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../config2.yaml"></div>
```

## Limitations et bonnes pratiques

### ✅ Ce que la solution supporte

- Fichiers YAML publics uniquement (sans authentification)
- URLs brutes GitHub (raw.githubusercontent.com)
- Contenu texte brut (pas de formatage Markdown)
- Navigateurs modernes (Chrome, Firefox, Safari, Edge)

### ⚠️ Limitations

- Le fichier YAML doit être **public** et accessible sans authentification
- Nécessite une **connexion internet** pour charger les fichiers
- Les sections n'ont pas de hiérarchie (boutons plats uniquement)
- Pas de cache local permanent
- Limites de taille : ~100 KB par fichier (limite CDN jsDelivr)

### 🔒 Sécurité

- ✅ L'échappement HTML est activé pour prévenir les injections
- ✅ Validation stricte de la structure YAML
- ✅ Utilisation de CDN vérifié (jsDelivr)
- ✅ Pas d'exécution de code JavaScript depuis le YAML

## Dépannage

### Le conteneur affiche "Chargement..." indéfiniment

**Causa probable** : 
- Le serveur CORS de GitHub bloque la requête
- La connexion internet est perdue
- L'URL est incorrecte

**Solution** :
- Vérifiez que l'URL commence par `https://raw.githubusercontent.com/`
- Testez l'URL directement dans le navigateur
- Vérifiez votre connexion internet

### Message : "La bibliothèque js-yaml n'est pas chargée"

**Causa probable** : Le fichier `mkdocs.yml` n'est pas correctement configuré

**Solution** :
```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
  - javascripts/yaml-loader.js
```

### Aucun bouton ne s'affiche

**Causa probable** : Le fichier YAML ne respecte pas la structure requise

**Solution** :
1. Vérifiez la structure de votre fichier YAML (doit avoir `sections` > `title` et `content`)
2. Consultez les erreurs affichées dans le navigateur (F12 > Console)

### Les boutons ne changent pas de section

**Causa probable** : Conflit CSS ou JavaScript

**Solution** :
- Vérifiez que le fichier CSS est chargé : [stylesheets/yaml-loader.css](stylesheets/yaml-loader.css)
- Testez dans un nouveau terminal de navigateur en mode privé

## Exemple complet

Voici un exemple complet avec un fichier YAML de test :

### Fichier YAML (exemple-test.yaml)

```yaml
sections:
  - title: "Configuration de base"
    content: |
      Ce fichier définit les paramètres par défaut.
      Les valeurs doivent être modifiées manuellement.
      Paramètres :
        - param1: valeur1
        - param2: valeur2
  - title: "Options avancées"
    content: |
      Les options avancées sont réservées aux utilisateurs experts.
      À utiliser avec précaution.
      Options :
        - advanced_option_1: true
        - advanced_option_2: "custom_value"
  - title: "Documentation supplémentaire"
    content: |
      Pour plus d'informations, consultez la documentation officielle.
      Lien : https://github.com/AntaresSimulatorTeam/GEMS
```

### Utilisation dans Markdown

```markdown
# Exemple de configuration

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/owner/repo/branch/example-test.yaml"></div>

Cliquez sur les boutons pour afficher les différentes sections.
```

## API JavaScript

Si vous avez besoin d'un contrôle avancé, vous pouvez utiliser directement la fonction JavaScript :

```javascript
// Charger un fichier YAML dans un conteneur
const container = document.getElementById('my-container');
const yamlUrl = 'https://raw.githubusercontent.com/.../file.yaml';
window.loadYAMLFile(container, yamlUrl);
```

## Support et contribution

Pour toute question ou problème :

1. Consultez la [FAQ](../../6_Support_Contributing/1_faq.md)
2. Ouvrez une [issue GitHub](https://github.com/AntaresSimulatorTeam/GEMS/issues)
3. Contactez l'équipe via [support](../../6_Support_Contributing/2_contact.md)

---

**Dernière mise à jour** : 17 février 2026
