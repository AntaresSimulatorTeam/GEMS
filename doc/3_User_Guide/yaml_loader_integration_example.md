# Exemple d'intégration : YAML Dynamic Loader

Ce document fournit un exemple complet d'intégration du YAML Dynamic Loader dans votre documentation MkDocs.

## 📌 Rappel rapide

Pour afficher un fichier YAML dans votre documentation, utilisez :

```html
<div class="yaml-loader-container" data-yaml-url="URL_DU_FICHIER_YAML"></div>
```

## 📂 Structure de vos fichiers YAML

Supposons que vous ayez un fichier `basic_models_library.yml` dans le dépôt GEMS sur GitHub.

**URL brute publique :**
```
https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml
```

## 💡 Exemple 1 : Afficher une bibliothèque de modèles

### Fichier Markdown : `doc/3_User_Guide/3_GEMS_File_Structure/2_library.md`

```markdown
# Fichier Bibliothèque

Le fichier bibliothèque contient la définition de tous les modèles disponibles pour votre système.

## Organisation des modèles

Consultez les modèles disponibles :

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml"></div>

### Description

Chaque section du fichier ci-dessus contient :
- **Titre** : Nom la catégorie de modèle
- **Contenu** : Définition YAML du modèle

Cliquez sur les boutons pour explorer les différentes configurations disponibles.
```

### Résultat affiché

- ✅ Bouton 1 : "Modèle 1"
- ✅ Bouton 2 : "Modèle 2"
- ✅ Bouton 3 : "Modèle 3"
- (Contenu du YAML affichéau clic)

---

## 💡 Exemple 2 : Afficher une configuration de système

### Cas : Documentation pour les fichiers de configuration

```markdown
## Configuration du système

Voici un exemple de fichier de configuration système :

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/examples/system-config.yaml"></div>

### Section "Paramètres de base"

Contient les éléments essentiels :
- Nom du système
- Résolution temporelle
- Calendrier

### Section "Options avancées"

Pour utilisateurs experts :
- Algorithme d'optimisation
- Tolérances numériques
```

---

## 💡 Exemple 3 : Intégration multiple

### Même page, plusieurs fichiers YAML

```markdown
# Interopérabilité PyPSA ↔ GEMS

## Fichiers de configuration PyPSA

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../pypsa-config.yaml"></div>

## Fichiers de configuration GEMS équivalents

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/.../gems-config.yaml"></div>

## Comparaison

Les deux fichiers ci-dessus montrent comment mapper les configurations PyPSA vers GEMS.
```

---

## 📝 Template prêt à utiliser

Copien-collez ce code dans votre fichier Markdown et adaptez l'URL :

```html
<!-- ========================================
     YAML Dynamic Loader
     Remplacez l'URL par celle de votre fichier
     ======================================== -->

<div class="yaml-loader-container" data-yaml-url="https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/file.yaml"></div>

<!-- Texte explicatif optionnel -->
<p>
  <small>Les sections ci-dessus sont chargées dynamiquement depuis 
  <a href="https://github.com/{owner}/{repo}/blob/{branch}/{path}/file.yaml">
    le dépôt GitHub
  </a>
</small>
</p>
```

---

## 🔗 Références d'URLs

### Format général
```
https://raw.githubusercontent.com/{USERNAME}/{REPOSITORY}/{BRANCH}/{PATH}/file.yaml
```

### Exemples pour GEMS

**URL basique:**
```
https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/libraries/basic_models_library.yml
```

**URL avec chemin complet:**
```
https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/main/doc/examples/configuration.yaml
```

**À partir d'une feature branch:**
```
https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/feature/my-branch/libraries/models.yaml
```

---

## ✅ Checklist d'intégration

Avant d'utiliser YAML Dynamic Loader dans votre documentation :

- [ ] Vérifier que `mkdocs.yml` inclut :
  ```yaml
  extra_javascript:
    - https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js
    - javascripts/yaml-loader.js
  extra_css:
    - stylesheets/yaml-loader.css
  ```

- [ ] Vérifier que le fichier YAML sur GitHub est **public**

- [ ] Vérifier la structure YAML :
  ```yaml
  sections:
    - title: "..."
      content: |
        ...
  ```

- [ ] Copier l'URL brute du fichier (raw.githubusercontent.com)

- [ ] Utiliser le format HTML dans Markdown :
  ```html
  <div class="yaml-loader-container" data-yaml-url="..."></div>
  ```

- [ ] Tester en local : `mkdocs serve`

- [ ] Vérifier qu'aucun message d'erreur n'apparaît

---

## 🐛 Problèmes courants

### Problème : "Erreur HTTP 404"

**Cause** : URL incorrecte ou fichier supprimé

**Solution** :
1. Testez l'URL directement dans le navigateur
2. Utilisez `raw.githubusercontent.com` (pas `github.com`)
3. Vérifiez le chemin du fichier

### Problème : "Le YAML doit contenir une propriété 'sections'"

**Cause** : Structure YAML invalide

**Solution** :
1. Validez votre YAML sur [yamllint.com](https://www.yamllint.com/)
2. Assurez-vous d'avoir une propriété `sections` au niveau racine
3. Chaque section doit avoir `title` et `content`

### Problème : Rien n'aparaît

**Cause** : js-yaml non chargée ou connexion internet

**Solution** :
1. Vérifiez votre connexion internet
2. Vérifiez la console navigateur (F12)
3. Rechargez la page (Ctrl+F5)

---

## 🎓 Bonnes pratiques

### ✅ À faire

- ✅ Utiliser toujours `raw.githubusercontent.com`
- ✅ Mettre à jour la documentation quand le YAML change
- ✅ Tester les URLs avant de publier
- ✅ Valider la structure YAML
- ✅ Ajouter un lien vers le fichier source sur GitHub

### ❌ À éviter

- ❌ URLs depuis d'autres domaines (problèmes CORS)
- ❌ Fichiers privés sans authentification
- ❌ Fichiers > 100 KB sans raison
- ❌ Structures YAML non valides
- ❌ Chemins relatifs au lieu d'URLs absolues

---

## 📚 Ressources

- [Guide d'utilisation complet](yaml_loader_guide.md)
- [Documentation technique](../YAML_LOADER_TECHNICAL.md)
- [README principal](../../YAML_LOADER_README.md)
- [Fichier YAML d'exemple](../../resources/yaml-loader-example.yaml)

---

## 🚀 Prochaines étapes

1. **Choisir un fichier YAML** à afficher dans votre documentation
2. **Mettre à jour le fichier Markdown** relevant
3. **Ajouter le conteneur HTML** avec l'URL appropriée
4. **Tester en local** avec `mkdocs serve`
5. **Valider et publier** votre documentation

---

**Besoin d'aide ?** Consultez la [documentation complète](../YAML_LOADER_TECHNICAL.md) ou créez une [issue GitHub](https://github.com/AntaresSimulatorTeam/GEMS/issues).
