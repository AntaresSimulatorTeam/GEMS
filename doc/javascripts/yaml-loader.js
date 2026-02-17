/**
 * YAML Dynamic Loader for MkDocs
 * 
 * Permet le chargement dynamique de fichiers YAML depuis GitHub et leur affichage
 * dans la documentation avec génération automatique de boutons par section.
 * 
 * Auteur: GEMS Documentation
 * License: MIT
 */

(function() {
    /**
     * Configuration globale
     */
    const CONFIG = {
        CONTAINER_CLASS: 'yaml-loader-container',
        BUTTON_CLASS: 'yaml-loader-button',
        CONTENT_CLASS: 'yaml-loader-content',
        ERROR_CLASS: 'yaml-loader-error',
        LOADING_CLASS: 'yaml-loader-loading',
    };

    /**
     * Détecte le type de structure YAML
     * @param {Object} data - Données parsées du YAML
     * @returns {string} 'sections' ou 'library' ou 'unknown'
     */
    function detectYAMLType(data) {
        if (!data || typeof data !== 'object') {
            return 'unknown';
        }
        
        if (Array.isArray(data.sections)) {
            return 'sections';
        }
        
        if (data.library && typeof data.library === 'object') {
            return 'library';
        }
        
        return 'unknown';
    }

    /**
     * Transforme une bibliothèque GEMS en sections pour affichage
     * @param {Object} data - Données du fichier library
     * @returns {Object} {sections: Array}
     */
    function transformGEMSLibraryToSections(data) {
        const sections = [];
        const lib = data.library || {};

        // Section 1: Vue d'ensemble de la librairie
        const overview = {
            title: `📚 ${lib.id || 'Bibliothèque'}`,
            content: `ID: ${lib.id || 'N/A'}\n\nDescription:\n${lib.description || 'Aucune description disponible.'}${lib.version ? `\n\nVersion: ${lib.version}` : ''}`
        };
        sections.push(overview);

        // Section 2: Types de ports
        if (lib['port-types'] && Object.keys(lib['port-types']).length > 0) {
            let portContent = '';
            Object.entries(lib['port-types']).forEach(([portName, portDef]) => {
                portContent += `\n📌 ${portName}:\n`;
                if (typeof portDef === 'object') {
                    portContent += JSON.stringify(portDef, null, 2);
                } else {
                    portContent += portDef;
                }
            });
            sections.push({
                title: '🔌 Types de Ports',
                content: portContent.trim()
            });
        }

        // Sections 3+: Modèles
        if (lib.models && Object.keys(lib.models).length > 0) {
            Object.entries(lib.models).forEach(([modelName, modelDef]) => {
                let modelContent = `Modèle: ${modelName}\n`;
                
                if (modelDef.description) {
                    modelContent += `\n📝 Description:\n${modelDef.description}`;
                }
                
                if (modelDef.ports) {
                    modelContent += `\n\n🔗 Ports:\n`;
                    Object.entries(modelDef.ports).forEach(([portName, portType]) => {
                        modelContent += `  • ${portName}: ${portType}\n`;
                    });
                }
                
                if (modelDef.parameters) {
                    modelContent += `\n\n⚙️ Paramètres:\n`;
                    Object.entries(modelDef.parameters).forEach(([paramName, paramDef]) => {
                        const paramType = typeof paramDef === 'string' ? paramDef : paramDef.type;
                        modelContent += `  • ${paramName}: ${paramType}\n`;
                    });
                }
                
                if (modelDef.variables) {
                    modelContent += `\n\n📊 Variables:\n`;
                    Object.entries(modelDef.variables).forEach(([varName, varDef]) => {
                        const varType = typeof varDef === 'string' ? varDef : varDef.type;
                        modelContent += `  • ${varName}: ${varType}\n`;
                    });
                }
                
                if (modelDef.sets) {
                    modelContent += `\n\n🎯 Ensembles:\n`;
                    Object.entries(modelDef.sets).forEach(([setName, setContent]) => {
                        modelContent += `  • ${setName}\n`;
                    });
                }

                sections.push({
                    title: `🔧 ${modelName}`,
                    content: modelContent
                });
            });
        }

        if (sections.length === 1) {
            sections.push({
                title: '⚠️ Aucun modèle',
                content: 'Aucun modèle trouvé dans cette bibliothèque.'
            });
        }

        return { sections };
    }

    /**
     * Valide la structure du fichier YAML
     * @param {Object} data - Données parsées du YAML
     * @returns {Object} {valid: boolean, error: string|null}
     */
    function validateYAMLStructure(data) {
        if (!data || typeof data !== 'object') {
            return { valid: false, error: 'Le fichier YAML doit être un objet.' };
        }

        const type = detectYAMLType(data);

        if (type === 'sections') {
            if (!Array.isArray(data.sections) || data.sections.length === 0) {
                return { valid: false, error: 'Le tableau "sections" ne peut pas être vide.' };
            }

            // Vérifier chaque section
            for (let i = 0; i < data.sections.length; i++) {
                const section = data.sections[i];
                
                if (!section || typeof section !== 'object') {
                    return { 
                        valid: false, 
                        error: `La section ${i} n'est pas un objet valide.` 
                    };
                }

                if (!section.title || typeof section.title !== 'string') {
                    return { 
                        valid: false, 
                        error: `La section ${i} doit avoir une propriété "title" de type string.` 
                    };
                }

                if (!section.content || typeof section.content !== 'string') {
                    return { 
                        valid: false, 
                        error: `La section ${i} "${section.title}" doit avoir une propriété "content" de type string.` 
                    };
                }
            }

            return { valid: true, error: null };
        }

        if (type === 'library') {
            if (!data.library || typeof data.library !== 'object') {
                return { valid: false, error: 'Le format "library" doit contenir une propriété "library" qui est un objet.' };
            }
            return { valid: true, error: null, type: 'library' };
        }

        return { 
            valid: false, 
            error: 'Format YAML non reconnu. Utilisez "sections" (tableau) ou "library" (objet avec clé "library").' 
        };
    }

    /**
     * Charge et parse un fichier YAML depuis une URL
     * @param {string} yamlUrl - URL du fichier YAML brut (raw.githubusercontent.com)
     * @returns {Promise} Chaîne YAML en cas de succès, lance une erreur sinon
     */
    async function fetchYAML(yamlUrl) {
        try {
            const response = await fetch(yamlUrl);
            
            if (!response.ok) {
                throw new Error(`Erreur HTTP ${response.status}: ${response.statusText}`);
            }

            const text = await response.text();
            
            if (!text.trim()) {
                throw new Error('Le fichier YAML est vide.');
            }

            return text;
        } catch (error) {
            throw new Error(`Impossible de charger le fichier YAML: ${error.message}`);
        }
    }

    /**
     * Parse une chaîne YAML en objet JavaScript
     * Nécessite la bibliothèque js-yaml
     * @param {string} yamlString - Contenu du fichier YAML
     * @returns {Object} Données parsées
     */
    function parseYAML(yamlString) {
        if (typeof jsyaml === 'undefined') {
            throw new Error('La bibliothèque js-yaml n\'est pas chargée. Vérifiez que js-yaml.js est inclus dans mkdocs.yml.');
        }

        try {
            const data = jsyaml.load(yamlString);
            return data;
        } catch (error) {
            throw new Error(`Erreur lors du parsing YAML: ${error.message}`);
        }
    }

    /**
     * Génère les boutons et le contenu pour un conteneur YAML-Loader
     * @param {Object} data - Données parsées du YAML
     * @param {HTMLElement} container - Conteneur HTML cible
     */
    function renderYAMLContent(data, container) {
        // Vider le conteneur
        container.innerHTML = '';

        // Créer un wrapper pour les boutons
        const buttonsWrapper = document.createElement('div');
        buttonsWrapper.className = 'yaml-loader-buttons-wrapper';

        // Créer un wrapper pour le contenu
        const contentWrapper = document.createElement('div');
        contentWrapper.className = 'yaml-loader-sections-wrapper';

        let isFirstButton = true;

        // Créer un bouton et une section pour chaque item
        data.sections.forEach((section, index) => {
            const buttonId = `yaml-btn-${Date.now()}-${index}`;
            const contentId = `yaml-content-${Date.now()}-${index}`;

            // Créer le bouton
            const button = document.createElement('button');
            button.id = buttonId;
            button.className = CONFIG.BUTTON_CLASS;
            button.textContent = section.title;
            if (isFirstButton) {
                button.classList.add('active');
                isFirstButton = false;
            }

            // Créer le conteneur de contenu
            const contentDiv = document.createElement('div');
            contentDiv.id = contentId;
            contentDiv.className = CONFIG.CONTENT_CLASS;
            contentDiv.style.display = isFirstButton ? 'block' : 'none';
            contentDiv.innerHTML = `<pre><code>${escapeHtml(section.content)}</code></pre>`;

            // Ajouter un événement de clic au bouton
            button.addEventListener('click', () => {
                // Désactiver tous les boutons et masquer tout le contenu
                document.querySelectorAll(`#${buttonId.split('-')[0]}-${buttonId.split('-')[1]}-*`).forEach(btn => {
                    if (btn.classList.contains(CONFIG.BUTTON_CLASS)) {
                        btn.classList.remove('active');
                    }
                });

                // Masquer tout le contenu dans ce conteneur
                container.querySelectorAll(`.${CONFIG.CONTENT_CLASS}`).forEach(content => {
                    content.style.display = 'none';
                });

                // Activer le bouton cliqué et afficher le contenu correspondant
                button.classList.add('active');
                contentDiv.style.display = 'block';
            });

            buttonsWrapper.appendChild(button);
            contentWrapper.appendChild(contentDiv);
        });

        // Ajouter les éléments au conteneur
        container.appendChild(buttonsWrapper);
        container.appendChild(contentWrapper);
    }

    /**
     * Affiche un message d'erreur dans le conteneur
     * @param {HTMLElement} container - Conteneur cible
     * @param {string} message - Message d'erreur
     */
    function displayError(container, message) {
        container.innerHTML = '';
        const errorDiv = document.createElement('div');
        errorDiv.className = CONFIG.ERROR_CLASS;
        errorDiv.innerHTML = `<strong>❌ Erreur:</strong> ${escapeHtml(message)}`;
        container.appendChild(errorDiv);
    }

    /**
     * Échappe les caractères HTML pour éviter les injections
     * @param {string} text - Texte à échapper
     * @returns {string} Texte échappé
     */
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Fonction principale : charge et affiche le contenu YAML
     * @param {HTMLElement} container - Conteneur HTML pour afficher le contenu
     * @param {string} yamlUrl - URL du fichier YAML
     */
    async function loadYAML(container, yamlUrl) {
        // Afficher l'état de chargement
        container.classList.add(CONFIG.LOADING_CLASS);
        container.innerHTML = '<p>Chargement du fichier YAML...</p>';

        try {
            // Valider l'URL
            if (!yamlUrl || typeof yamlUrl !== 'string') {
                throw new Error('URL du fichier YAML invalide.');
            }

            // Charger le fichier YAML
            const yamlString = await fetchYAML(yamlUrl);

            // Parser le YAML
            let data = parseYAML(yamlString);

            // Valider la structure et déterminer le type
            const validation = validateYAMLStructure(data);
            if (!validation.valid) {
                throw new Error(validation.error);
            }

            // Transformer si c'est une libraryGEMS
            if (validation.type === 'library') {
                data = transformGEMSLibraryToSections(data);
            }

            // Retirer la classe de chargement et afficher le contenu
            container.classList.remove(CONFIG.LOADING_CLASS);
            renderYAMLContent(data, container);

        } catch (error) {
            container.classList.remove(CONFIG.LOADING_CLASS);
            displayError(container, error.message);
        }
    }

    /**
     * Initialise tous les conteneurs YAML-Loader sur la page
     */
    function initializeYAMLLoaders() {
        // Sélectionner tous les conteneurs avec l'attribut data-yaml-url
        document.querySelectorAll(`[data-yaml-url]`).forEach(container => {
            const yamlUrl = container.getAttribute('data-yaml-url');
            
            if (!yamlUrl) {
                displayError(container, 'Attribut data-yaml-url manquant.');
                return;
            }

            // Charger le YAML
            loadYAML(container, yamlUrl);
        });
    }

    // Initialiser quand le DOM est prêt
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeYAMLLoaders);
    } else {
        // Si le script est chargé après le DOM
        initializeYAMLLoaders();
    }

    // Exposer la fonction loadYAML globalement pour un usage manuel
    window.loadYAMLFile = loadYAML;
})();
