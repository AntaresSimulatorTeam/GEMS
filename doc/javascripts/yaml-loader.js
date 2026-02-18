/**
 * YAML Dynamic Loader for MkDocs
 * 
 * Allows dynamic loading of YAML files from GitHub and their display
 * in documentation with automatic button generation per section.
 */

(function() {
    /**
     * Global configuration
     */
    const CONFIG = {
        CONTAINER_CLASS: 'yaml-loader-container',
        BUTTON_CLASS: 'yaml-loader-button',
        CONTENT_CLASS: 'yaml-loader-content',
        ERROR_CLASS: 'yaml-loader-error',
        LOADING_CLASS: 'yaml-loader-loading',
    };

    /**
     * Detects the type of YAML structure
     * @param {Object} data - Parsed YAML data
     * @returns {string} 'sections' or 'library' or 'unknown'
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
     * Renders a hierarchical interface for a GEMS library
     * @param {Object} data - Library file data
     * @param {HTMLElement} container - Target container
     */
    function renderGEMSLibrary(data, container) {
        container.innerHTML = '';
        
        const lib = data.library || {};
        if (!lib || Object.keys(lib).length === 0) {
            container.innerHTML = '<p style="color: red;">Error: The library is empty</p>';
            return;
        }
        
        // Main wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'yaml-library-wrapper';
        
        // === LEVEL 1: LIBRARY ===
        const libLevel1 = document.createElement('div');
        libLevel1.className = 'yaml-library-level-1';
        
        const libButton = document.createElement('button');
        libButton.className = 'yaml-library-button yaml-library-button-lib active';
        libButton.innerHTML = `📚 <strong>${escapeHtml(lib.id || 'Library')}</strong>`;
        libLevel1.appendChild(libButton);
        
        // === LIBRARY CONTENT ===
        const libContent = document.createElement('div');
        libContent.className = 'yaml-library-content';
        
        const libInfo = document.createElement('div');
        libInfo.className = 'library-info';
        
        const idP = document.createElement('p');
        idP.innerHTML = `<strong>ID:</strong> ${escapeHtml(lib.id || 'N/A')}`;
        libInfo.appendChild(idP);
        
        const descP = document.createElement('p');
        descP.innerHTML = `<strong>Description:</strong> ${escapeHtml(lib.description || 'No description available.')}`;
        libInfo.appendChild(descP);
        
        if (lib.version) {
            const verP = document.createElement('p');
            verP.innerHTML = `<strong>Version:</strong> ${escapeHtml(lib.version)}`;
            libInfo.appendChild(verP);
        }
        
        libContent.appendChild(libInfo);
        
        // === LEVEL 2: PORT TYPES ===
        if (lib['port-types'] && Array.isArray(lib['port-types']) && lib['port-types'].length > 0) {
            // Title
            const portTitle = document.createElement('h3');
            portTitle.style.marginTop = '20px';
            portTitle.style.borderBottom = '2px solid #0066cc';
            portTitle.style.paddingBottom = '10px';
            portTitle.textContent = '🔌 Port Types';
            libContent.appendChild(portTitle);
            
            // Port buttons
            const portButtonsWrapper = document.createElement('div');
            portButtonsWrapper.className = 'yaml-library-level-2';
            portButtonsWrapper.style.display = 'flex';
            portButtonsWrapper.style.flexWrap = 'wrap';
            portButtonsWrapper.style.gap = '10px';
            portButtonsWrapper.style.margin = '10px 0';
            
            lib['port-types'].forEach((portDef, index) => {
                const portName = portDef.id || `port_${index}`;
                const sanitizedPortName = portName.replace(/[^a-z0-9]/gi, '-').toLowerCase();
                
                const portBtn = document.createElement('button');
                portBtn.className = 'yaml-library-button yaml-library-button-port';
                portBtn.dataset.port = sanitizedPortName;
                portBtn.textContent = escapeHtml(portName);
                portButtonsWrapper.appendChild(portBtn);
            });
            
            libContent.appendChild(portButtonsWrapper);
            
            // Port content
            lib['port-types'].forEach((portDef, index) => {
                const portName = portDef.id || `port_${index}`;
                const sanitizedPortName = portName.replace(/[^a-z0-9]/gi, '-').toLowerCase();
                
                const portContentDiv = document.createElement('div');
                portContentDiv.className = 'yaml-library-port-content';
                portContentDiv.dataset.port = sanitizedPortName;
                portContentDiv.style.display = 'none';
                
                const portNameH4 = document.createElement('h4');
                portNameH4.textContent = escapeHtml(portName);
                portContentDiv.appendChild(portNameH4);
                
                if (portDef.description) {
                    const descriptionP = document.createElement('p');
                    descriptionP.innerHTML = `<strong>Description:</strong> ${escapeHtml(portDef.description)}`;
                    portContentDiv.appendChild(descriptionP);
                }
                
                if (portDef.fields && Array.isArray(portDef.fields)) {
                    const fieldsDiv = document.createElement('div');
                    fieldsDiv.style.marginTop = '15px';
                    
                    const fieldsTitle = document.createElement('strong');
                    fieldsTitle.textContent = '📋 Fields:';
                    fieldsDiv.appendChild(fieldsTitle);
                    
                    const fieldsList = document.createElement('ul');
                    portDef.fields.forEach(field => {
                        const fieldLi = document.createElement('li');
                        const fieldCode = document.createElement('code');
                        fieldCode.textContent = escapeHtml(field.id || 'Unknown');
                        fieldLi.appendChild(fieldCode);
                        fieldsList.appendChild(fieldLi);
                    });
                    fieldsDiv.appendChild(fieldsList);
                    portContentDiv.appendChild(fieldsDiv);
                }
                
                libContent.appendChild(portContentDiv);
            });
        }
        
        // === LEVEL 2: MODELS ===
        if (lib.models && Array.isArray(lib.models) && lib.models.length > 0) {
            // Title
            const modelTitle = document.createElement('h3');
            modelTitle.style.marginTop = '20px';
            modelTitle.style.borderBottom = '2px solid #0066cc';
            modelTitle.style.paddingBottom = '10px';
            modelTitle.textContent = '🔧 Models';
            libContent.appendChild(modelTitle);
            
            // Model buttons
            const modelButtonsWrapper = document.createElement('div');
            modelButtonsWrapper.className = 'yaml-library-level-2';
            modelButtonsWrapper.style.display = 'flex';
            modelButtonsWrapper.style.flexWrap = 'wrap';
            modelButtonsWrapper.style.gap = '10px';
            modelButtonsWrapper.style.margin = '10px 0';
            
            lib.models.forEach((modelDef, index) => {
                const modelName = modelDef.id || `model_${index}`;
                const sanitizedModelName = modelName.replace(/[^a-z0-9]/gi, '-').toLowerCase();
                
                const modelBtn = document.createElement('button');
                modelBtn.className = 'yaml-library-button yaml-library-button-model';
                modelBtn.dataset.model = sanitizedModelName;
                modelBtn.textContent = escapeHtml(modelName);
                modelButtonsWrapper.appendChild(modelBtn);
            });
            
            libContent.appendChild(modelButtonsWrapper);
            
            // Model content
            lib.models.forEach((modelDef, index) => {
                const modelName = modelDef.id || `model_${index}`;
                const sanitizedModelName = modelName.replace(/[^a-z0-9]/gi, '-').toLowerCase();
                
                const modelContentDiv = document.createElement('div');
                modelContentDiv.className = 'yaml-library-model-content';
                modelContentDiv.dataset.model = sanitizedModelName;
                modelContentDiv.style.display = 'none';
                
                const modelNameH4 = document.createElement('h4');
                modelNameH4.textContent = escapeHtml(modelName);
                modelContentDiv.appendChild(modelNameH4);
                
                if (modelDef.description) {
                    const descriptionP = document.createElement('p');
                    descriptionP.innerHTML = `<strong>Description:</strong> ${escapeHtml(modelDef.description)}`;
                    modelContentDiv.appendChild(descriptionP);
                }
                
                if (modelDef.ports && Array.isArray(modelDef.ports) && modelDef.ports.length > 0) {
                    const portsDiv = document.createElement('div');
                    portsDiv.style.marginTop = '15px';
                    
                    const portsTitle = document.createElement('strong');
                    portsTitle.textContent = '🔗 Ports:';
                    portsDiv.appendChild(portsTitle);
                    
                    const portsSpanDiv = document.createElement('div');
                    portsSpanDiv.style.display = 'flex';
                    portsSpanDiv.style.flexWrap = 'wrap';
                    portsSpanDiv.style.gap = '8px';
                    portsSpanDiv.style.margin = '8px 0';
                    
                    modelDef.ports.forEach(port => {
                        const portName = port.id || 'Unknown Port';
                        const portType = port.type || 'Unknown Type';
                        const sanitizedPortRef = portType.replace(/[^a-z0-9]/gi, '-').toLowerCase();
                        
                        const portSpan = document.createElement('span');
                        portSpan.className = 'yaml-port-reference';
                        portSpan.dataset.portRef = sanitizedPortRef;
                        portSpan.innerHTML = `${escapeHtml(portName)} <em>(${escapeHtml(portType)})</em>`;
                        portsSpanDiv.appendChild(portSpan);
                    });
                    
                    portsDiv.appendChild(portsSpanDiv);
                    modelContentDiv.appendChild(portsDiv);
                }
                
                if (modelDef.parameters && Array.isArray(modelDef.parameters) && modelDef.parameters.length > 0) {
                    const paramsDiv = document.createElement('div');
                    paramsDiv.style.marginTop = '15px';
                    
                    const paramsTitle = document.createElement('strong');
                    paramsTitle.textContent = '⚙️ Parameters:';
                    paramsDiv.appendChild(paramsTitle);
                    
                    const paramsList = document.createElement('ul');
                    modelDef.parameters.forEach(param => {
                        const paramName = param.id || 'Unknown';
                        const timeDependent = param['time-dependent'] ? ' [time-dependent]' : '';
                        const scenarioDependent = param['scenario-dependent'] ? ' [scenario-dependent]' : '';
                        
                        const paramLi = document.createElement('li');
                        const paramCode = document.createElement('code');
                        paramCode.textContent = escapeHtml(paramName);
                        paramLi.appendChild(paramCode);
                        paramLi.innerHTML += `${timeDependent}${scenarioDependent}`;
                        paramsList.appendChild(paramLi);
                    });
                    paramsDiv.appendChild(paramsList);
                    modelContentDiv.appendChild(paramsDiv);
                }
                
                if (modelDef.variables && Array.isArray(modelDef.variables) && modelDef.variables.length > 0) {
                    const varsDiv = document.createElement('div');
                    varsDiv.style.marginTop = '15px';
                    
                    const varsTitle = document.createElement('strong');
                    varsTitle.textContent = '📊 Variables:';
                    varsDiv.appendChild(varsTitle);
                    
                    const varsList = document.createElement('ul');
                    modelDef.variables.forEach(variable => {
                        const varName = variable.id || 'Unknown';
                        const varType = variable['variable-type'] || 'Unknown';
                        const lowerBound = variable['lower-bound'] !== undefined ? ` [${variable['lower-bound']}` : '';
                        const upperBound = variable['upper-bound'] !== undefined ? `, ${variable['upper-bound']}]` : '';
                        
                        const varLi = document.createElement('li');
                        const varCode = document.createElement('code');
                        varCode.textContent = escapeHtml(varName);
                        varLi.appendChild(varCode);
                        varLi.innerHTML += `: ${escapeHtml(varType)}${lowerBound}${upperBound}`;
                        varsList.appendChild(varLi);
                    });
                    varsDiv.appendChild(varsList);
                    modelContentDiv.appendChild(varsDiv);
                }
                
                if (modelDef['binding-constraints'] && Array.isArray(modelDef['binding-constraints']) && modelDef['binding-constraints'].length > 0) {
                    const constraintsDiv = document.createElement('div');
                    constraintsDiv.style.marginTop = '15px';
                    
                    const constraintsTitle = document.createElement('strong');
                    constraintsTitle.textContent = '🔗 Constraints:';
                    constraintsDiv.appendChild(constraintsTitle);
                    
                    const constraintsList = document.createElement('ul');
                    modelDef['binding-constraints'].forEach(constraint => {
                        const constraintName = constraint.id || 'Unknown';
                        
                        const constraintLi = document.createElement('li');
                        const constraintCode = document.createElement('code');
                        constraintCode.textContent = escapeHtml(constraintName);
                        constraintLi.appendChild(constraintCode);
                        constraintsList.appendChild(constraintLi);
                    });
                    constraintsDiv.appendChild(constraintsList);
                    modelContentDiv.appendChild(constraintsDiv);
                }
                
                libContent.appendChild(modelContentDiv);
            });
        }
        
        // Add everything to wrapper
        wrapper.appendChild(libLevel1);
        wrapper.appendChild(libContent);
        container.appendChild(wrapper);
        
        // === EVENT LISTENERS ===
        
        // Clic sur bouton port
        libButton.addEventListener('click', () => {
            libContent.querySelectorAll('.yaml-library-port-content').forEach(el => el.style.display = 'none');
            libContent.querySelectorAll('.yaml-library-model-content').forEach(el => el.style.display = 'none');
            libInfo.style.display = 'block';
            
            libButton.classList.add('active');
            libContent.querySelectorAll('.yaml-library-button-port, .yaml-library-button-model').forEach(btn => {
                btn.classList.remove('active');
            });
        });
        
        libContent.querySelectorAll('.yaml-library-button-port').forEach(portBtn => {
            portBtn.addEventListener('click', (e) => {
                const portData = e.currentTarget.dataset.port;
                libContent.querySelectorAll('.yaml-library-port-content').forEach(el => el.style.display = 'none');
                libContent.querySelectorAll('.yaml-library-model-content').forEach(el => el.style.display = 'none');
                
                const portContent = libContent.querySelector(`.yaml-library-port-content[data-port="${portData}"]`);
                if (portContent) portContent.style.display = 'block';
                
                libButton.classList.remove('active');
                libContent.querySelectorAll('.yaml-library-button-port').forEach(btn => btn.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });
        
        libContent.querySelectorAll('.yaml-library-button-model').forEach(modelBtn => {
            modelBtn.addEventListener('click', (e) => {
                const modelData = e.currentTarget.dataset.model;
                libContent.querySelectorAll('.yaml-library-port-content').forEach(el => el.style.display = 'none');
                libContent.querySelectorAll('.yaml-library-model-content').forEach(el => el.style.display = 'none');
                
                const modelContent = libContent.querySelector(`.yaml-library-model-content[data-model="${modelData}"]`);
                if (modelContent) modelContent.style.display = 'block';
                
                libButton.classList.remove('active');
                libContent.querySelectorAll('.yaml-library-button-model').forEach(btn => btn.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });
        
        libContent.querySelectorAll('.yaml-port-reference').forEach(portRef => {
            portRef.addEventListener('click', (e) => {
                const portRefData = e.currentTarget.dataset.portRef;
                const correspondingPortBtn = libContent.querySelector(`.yaml-library-button-port[data-port="${portRefData}"]`);
                if (correspondingPortBtn) {
                    correspondingPortBtn.click();
                    correspondingPortBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
        });
    }

    /**
     * Validates the YAML file structure
     * @param {Object} data - Parsed YAML data
     * @returns {Object} {valid: boolean, error: string|null}
     */
    function validateYAMLStructure(data) {
        if (!data || typeof data !== 'object') {
            return { valid: false, error: 'The YAML file must be an object.' };
        }

        const type = detectYAMLType(data);

        if (type === 'sections') {
            if (!Array.isArray(data.sections) || data.sections.length === 0) {
                return { valid: false, error: 'The "sections" array cannot be empty.' };
            }

            // Check each section
            for (let i = 0; i < data.sections.length; i++) {
                const section = data.sections[i];
                
                if (!section || typeof section !== 'object') {
                    return { 
                        valid: false, 
                        error: `Section ${i} is not a valid object.` 
                    };
                }

                if (!section.title || typeof section.title !== 'string') {
                    return { 
                        valid: false, 
                        error: `Section ${i} must have a "title" property of type string.` 
                    };
                }

                if (!section.content || typeof section.content !== 'string') {
                    return { 
                        valid: false, 
                        error: `Section ${i} "${section.title}" must have a "content" property of type string.` 
                    };
                }
            }

            return { valid: true, error: null };
        }

        if (type === 'library') {
            if (!data.library || typeof data.library !== 'object') {
                return { valid: false, error: 'The "library" format must contain a "library" property that is an object.' };
            }
            return { valid: true, error: null, type: 'library' };
        }

        return { 
            valid: false, 
            error: 'Unrecognized YAML format. Use "sections" (array) or "library" (object with "library" key).' 
        };
    }

    /**
     * Loads and parses a YAML file from a URL
     * @param {string} yamlUrl - URL of the raw YAML file (raw.githubusercontent.com)
     * @returns {Promise} YAML string on success, throws error otherwise
     */
    async function fetchYAML(yamlUrl) {
        try {
            const response = await fetch(yamlUrl);
            
            if (!response.ok) {
                throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
            }

            const text = await response.text();
            
            if (!text.trim()) {
                throw new Error('The YAML file is empty.');
            }

            return text;
        } catch (error) {
            throw new Error(`Unable to load YAML file: ${error.message}`);
        }
    }

    /**
     * Parses a YAML string into a JavaScript object
     * Requires the js-yaml library
     * @param {string} yamlString - Content of the YAML file
     * @returns {Object} Parsed data
     */
    function parseYAML(yamlString) {
        if (typeof jsyaml === 'undefined') {
            throw new Error('The js-yaml library is not loaded. Check that js-yaml.js is included in mkdocs.yml.');
        }

        try {
            const data = jsyaml.load(yamlString);
            return data;
        } catch (error) {
            throw new Error(`Error during YAML parsing: ${error.message}`);
        }
    }

    /**
     * Generates buttons and content for a YAML-Loader container
     * @param {Object} data - Parsed YAML data
     * @param {HTMLElement} container - Target HTML container
     */
    function renderYAMLContent(data, container) {
        // Empty the container
        container.innerHTML = '';

        // Create a wrapper for buttons
        const buttonsWrapper = document.createElement('div');
        buttonsWrapper.className = 'yaml-loader-buttons-wrapper';

        // Create a wrapper for content
        const contentWrapper = document.createElement('div');
        contentWrapper.className = 'yaml-loader-sections-wrapper';

        let isFirstButton = true;

        // Create a button and section for each item
        data.sections.forEach((section, index) => {
            const buttonId = `yaml-btn-${Date.now()}-${index}`;
            const contentId = `yaml-content-${Date.now()}-${index}`;

            // Create the button
            const button = document.createElement('button');
            button.id = buttonId;
            button.className = CONFIG.BUTTON_CLASS;
            button.textContent = section.title;
            if (isFirstButton) {
                button.classList.add('active');
                isFirstButton = false;
            }

            // Create the content container
            const contentDiv = document.createElement('div');
            contentDiv.id = contentId;
            contentDiv.className = CONFIG.CONTENT_CLASS;
            contentDiv.style.display = isFirstButton ? 'block' : 'none';
            contentDiv.innerHTML = `<pre><code>${escapeHtml(section.content)}</code></pre>`;

            // Add click event to button
            button.addEventListener('click', () => {
                // Deactivate all buttons and hide all content
                document.querySelectorAll(`#${buttonId.split('-')[0]}-${buttonId.split('-')[1]}-*`).forEach(btn => {
                    if (btn.classList.contains(CONFIG.BUTTON_CLASS)) {
                        btn.classList.remove('active');
                    }
                });

                // Hide all content in this container
                container.querySelectorAll(`.${CONFIG.CONTENT_CLASS}`).forEach(content => {
                    content.style.display = 'none';
                });

                // Activate clicked button and display corresponding content
                button.classList.add('active');
                contentDiv.style.display = 'block';
            });

            buttonsWrapper.appendChild(button);
            contentWrapper.appendChild(contentDiv);
        });

        // Add elements to container
        container.appendChild(buttonsWrapper);
        container.appendChild(contentWrapper);
    }

    /**
     * Displays an error message in the container
     * @param {HTMLElement} container - Target container
     * @param {string} message - Error message
     */
    function displayError(container, message) {
        container.innerHTML = '';
        const errorDiv = document.createElement('div');
        errorDiv.className = CONFIG.ERROR_CLASS;
        errorDiv.innerHTML = `<strong>❌ Error:</strong> ${escapeHtml(message)}`;
        container.appendChild(errorDiv);
    }

    /**
     * Escapes HTML characters to prevent injections
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
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
     * Main function: loads and displays YAML content
     * @param {HTMLElement} container - HTML container to display content
     * @param {string} yamlUrl - URL of the YAML file
     */
    async function loadYAML(container, yamlUrl) {
        // Show loading state
        container.classList.add(CONFIG.LOADING_CLASS);
        container.innerHTML = '<p>Loading YAML file...</p>';

        try {
            // Validate the URL
            if (!yamlUrl || typeof yamlUrl !== 'string') {
                throw new Error('Invalid YAML file URL.');
            }

            // Load the YAML file
            const yamlString = await fetchYAML(yamlUrl);

            // Parse the YAML
            let data = parseYAML(yamlString);

            // Validate structure and determine type
            const validation = validateYAMLStructure(data);
            if (!validation.valid) {
                throw new Error(validation.error);
            }

            // Remove loading class and display content
            container.classList.remove(CONFIG.LOADING_CLASS);
            
            // Render based on type
            if (validation.type === 'library') {
                renderGEMSLibrary(data, container);
            } else {
                renderYAMLContent(data, container);
            }

        } catch (error) {
            container.classList.remove(CONFIG.LOADING_CLASS);
            displayError(container, error.message);
        }
    }

    /**
     * Initializes all YAML-Loader containers on the page
     */
    function initializeYAMLLoaders() {
        // Select all containers with the data-yaml-url attribute
        document.querySelectorAll(`[data-yaml-url]`).forEach(container => {
            const yamlUrl = container.getAttribute('data-yaml-url');
            
            if (!yamlUrl) {
                displayError(container, 'Missing data-yaml-url attribute.');
                return;
            }

            // Load the YAML
            loadYAML(container, yamlUrl);
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeYAMLLoaders);
    } else {
        // If script is loaded after DOM
        initializeYAMLLoaders();
    }

    // Expose loadYAML function globally for manual usage
    window.loadYAMLFile = loadYAML;
})();
