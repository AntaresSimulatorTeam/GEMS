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
     * Escapes special characters in regex pattern
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    function escapeRegex(text) {
        return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    /**
     * Creates text and operator nodes with operators bolded and port references as clickable buttons
     * @param {string} text - Text to parse
     * @param {HTMLElement} container - Container to append nodes to
     * @param {Object} modelDef - Model definition object containing ports
     */
    function appendParsedText(text, container, modelDef) {
        // Get port names for matching port.field references
        const portNames = modelDef && modelDef.ports ? 
            modelDef.ports.map(p => p.id).filter(Boolean) : [];
        
        // Pattern to detect:
        // 1. Port references: portName.fieldName
        // 2. sum_<subscript> patterns
        // 3. Mathematical operators: <=, >=, ==, !=, =, <, >, +, -, *, /, (, ), [, ]
        // 4. Function names: word followed by parenthesis
        
        // First pass: detect port.field
        const portFieldPattern = new RegExp(
            `\\b(${portNames.map(escapeRegex).join('|')})\\.(\\w+)`,
            'g'
        );
        
        // Pattern to detect sum_<something>
        const sumPattern = /\bsum_(\w+)/g;
        
        const operatorFunctionPattern = /(<=|>=|==|!=|[=<>+\-*/()\[\]]|[a-zA-Z_][a-zA-Z0-9_]*(?=\())/g;
        
        let lastIndex = 0;
        let portMatch;
        
        // Create a map of all port.field positions
        const portMatches = [];
        while ((portMatch = portFieldPattern.exec(text)) !== null) {
            portMatches.push({
                start: portMatch.index,
                end: portFieldPattern.lastIndex,
                portName: portMatch[1],
                fieldName: portMatch[2],
                fullMatch: portMatch[0]
            });
        }
        
        // Create a map of all sum_<subscript> positions
        const sumMatches = [];
        let sumMatch;
        while ((sumMatch = sumPattern.exec(text)) !== null) {
            sumMatches.push({
                start: sumMatch.index,
                end: sumPattern.lastIndex,
                subscript: sumMatch[1],
                fullMatch: sumMatch[0]
            });
        }
        
        // Process text considering port.field, sum_ and operators
        lastIndex = 0;
        
        for (let i = 0; i < text.length; ) {
            // Check if we are at the start of a sum_ reference
            const sumRef = sumMatches.find(sm => sm.start === i);
            
            if (sumRef) {
                // Create the Σ symbol with subscript
                const span = document.createElement('span');
                span.style.fontWeight = 'bold';
                span.innerHTML = '∑<sub>' + escapeHtml(sumRef.subscript) + '</sub>';
                container.appendChild(span);
                i = sumRef.end;
                continue;
            }
            
            // Check if we are at the start of a port.field reference
            const portRef = portMatches.find(pm => pm.start === i);
            
            if (portRef) {
                // Create a button for the port.field reference
                const btn = document.createElement('button');
                btn.className = 'yaml-item-button';
                btn.textContent = portRef.fullMatch;
                
                btn.addEventListener('click', (e) => {
                    const port = modelDef.ports && modelDef.ports.find(p => p.id === portRef.portName);
                    if (port) {
                        showPortPopup(port, e.currentTarget);
                    }
                });
                
                container.appendChild(btn);
                i = portRef.end;
            } else {
                // Search for the next operator/function from position i
                const substring = text.substring(i);
                const operatorMatch = operatorFunctionPattern.exec(substring);
                
                if (operatorMatch && operatorMatch.index === 0) {
                    // We have an operator/function at the start
                    const span = document.createElement('span');
                    span.style.fontWeight = 'bold';
                    // Replace 'sum' with the ∑ symbol
                    span.textContent = operatorMatch[0] === 'sum' ? '∑' : operatorMatch[0];
                    container.appendChild(span);
                    i += operatorMatch[0].length;
                    operatorFunctionPattern.lastIndex = 0;
                } else if (operatorMatch) {
                    // Text before the operator
                    container.appendChild(document.createTextNode(substring.substring(0, operatorMatch.index)));
                    i += operatorMatch.index;
                    operatorFunctionPattern.lastIndex = 0;
                } else {
                    // No operator found, add the rest
                    if (substring.length > 0) {
                        container.appendChild(document.createTextNode(substring));
                    }
                    i = text.length;
                }
            }
        }
    }

    /**
     * Shows a popup with variable details
     * @param {Object} variable - Variable definition object
     * @param {HTMLElement} triggerElement - The element that triggered the popup
     */
    function showVariablePopup(variable, triggerElement) {
        // Remove any existing popup
        const existingPopup = document.querySelector('.yaml-variable-popup');
        if (existingPopup) {
            existingPopup.remove();
        }

        const popup = document.createElement('div');
        popup.className = 'yaml-variable-popup';

        // Popup header
        const header = document.createElement('div');
        header.className = 'yaml-variable-popup-header';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'yaml-variable-popup-close';
        closeBtn.textContent = '✕';
        closeBtn.addEventListener('click', () => popup.remove());
        header.appendChild(closeBtn);

        popup.appendChild(header);

        // Popup content
        const content = document.createElement('div');
        content.className = 'yaml-variable-popup-content';

        // Create YAML-style display
        const yamlContent = document.createElement('pre');
        yamlContent.style.margin = '0';
        yamlContent.style.fontFamily = 'Arial';
        yamlContent.style.fontSize = '13px';
        yamlContent.style.lineHeight = '1.5';
        
        let yamlText = `id: ${escapeHtml(variable.id || 'Unknown Variable')}`;
        
        if (variable['variable-type']) {
            yamlText += `\nvariable-type: ${escapeHtml(variable['variable-type'])}`;
        }
        
        if (variable['lower-bound'] !== undefined) {
            yamlText += `\nlower-bound: ${escapeHtml(String(variable['lower-bound']))}`;
        }
        
        if (variable['upper-bound'] !== undefined) {
            yamlText += `\nupper-bound: ${escapeHtml(String(variable['upper-bound']))}`;
        }
        
        if (variable['time-dependent']) {
            yamlText += `\ntime-dependent: true`;
        }
        
        if (variable['scenario-dependent']) {
            yamlText += `\nscenario-dependent: true`;
        }
        
        yamlContent.textContent = yamlText;
        content.appendChild(yamlContent);

        popup.appendChild(content);

        document.body.appendChild(popup);

        // Position popup near the trigger element (fixed in document, not viewport)
        popup.style.position = 'absolute';
        const rect = triggerElement.getBoundingClientRect();
        popup.style.top = (rect.bottom + window.scrollY + 5) + 'px';
        popup.style.left = (rect.left + window.scrollX) + 'px';

        // Close popup when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeOnOutside(e) {
                if (!popup.contains(e.target) && e.target !== triggerElement && !triggerElement.contains(e.target)) {
                    popup.remove();
                    document.removeEventListener('click', closeOnOutside);
                }
            });
        }, 0);
    }

    /**
     * Shows a popup with parameter details
     * @param {Object} param - Parameter definition object
     * @param {HTMLElement} triggerElement - The element that triggered the popup
     */
    function showParameterPopup(param, triggerElement) {
        // Remove any existing popup
        const existingPopup = document.querySelector('.yaml-variable-popup');
        if (existingPopup) {
            existingPopup.remove();
        }

        const popup = document.createElement('div');
        popup.className = 'yaml-variable-popup';

        // Popup header
        const header = document.createElement('div');
        header.className = 'yaml-variable-popup-header';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'yaml-variable-popup-close';
        closeBtn.textContent = '✕';
        closeBtn.addEventListener('click', () => popup.remove());
        header.appendChild(closeBtn);

        popup.appendChild(header);

        // Popup content
        const content = document.createElement('div');
        content.className = 'yaml-variable-popup-content';

        // Create YAML-style display
        const yamlContent = document.createElement('pre');
        yamlContent.style.margin = '0';
        yamlContent.style.fontFamily = 'Arial';
        yamlContent.style.fontSize = '13px';
        yamlContent.style.lineHeight = '1.5';
        
        let yamlText = `id: ${escapeHtml(param.id || 'Unknown Parameter')}`;
        
        if (param['time-dependent']) {
            yamlText += `\ntime-dependent: true`;
        }
        
        if (param['scenario-dependent']) {
            yamlText += `\nscenario-dependent: true`;
        }
        
        yamlContent.textContent = yamlText;
        content.appendChild(yamlContent);

        popup.appendChild(content);

        document.body.appendChild(popup);

        // Position popup near the trigger element (fixed in document, not viewport)
        popup.style.position = 'absolute';
        const rect = triggerElement.getBoundingClientRect();
        popup.style.top = (rect.bottom + window.scrollY + 5) + 'px';
        popup.style.left = (rect.left + window.scrollX) + 'px';

        // Close popup when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeOnOutside(e) {
                if (!popup.contains(e.target) && e.target !== triggerElement && !triggerElement.contains(e.target)) {
                    popup.remove();
                    document.removeEventListener('click', closeOnOutside);
                }
            });
        }, 0);
    }

    /**
     * Shows a popup with constraint details
     * @param {Object} constraint - Constraint definition object
     * @param {HTMLElement} triggerElement - The element that triggered the popup
     */
    function showConstraintPopup(constraint, triggerElement) {
        // Remove any existing popup
        const existingPopup = document.querySelector('.yaml-variable-popup');
        if (existingPopup) {
            existingPopup.remove();
        }

        const popup = document.createElement('div');
        popup.className = 'yaml-variable-popup';

        // Popup header
        const header = document.createElement('div');
        header.className = 'yaml-variable-popup-header';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'yaml-variable-popup-close';
        closeBtn.textContent = '✕';
        closeBtn.addEventListener('click', () => popup.remove());
        header.appendChild(closeBtn);

        popup.appendChild(header);

        // Popup content
        const content = document.createElement('div');
        content.className = 'yaml-variable-popup-content';

        // Create YAML-style display
        const yamlContent = document.createElement('pre');
        yamlContent.style.margin = '0';
        yamlContent.style.fontFamily = 'Arial';
        yamlContent.style.fontSize = '13px';
        yamlContent.style.lineHeight = '1.4';
        
        let yamlText = `id: ${escapeHtml(constraint.id || 'Unknown Constraint')}`;
        
        if (constraint.expression) {
            yamlText += `\nexpression: ${escapeHtml(constraint.expression)}`;
        }
        
        if (constraint['time-dependent']) {
            yamlText += `\ntime-dependent: true`;
        }
        
        if (constraint['scenario-dependent']) {
            yamlText += `\nscenario-dependent: true`;
        }
        
        yamlContent.textContent = yamlText;
        content.appendChild(yamlContent);

        popup.appendChild(content);

        document.body.appendChild(popup);

        // Position popup near the trigger element (fixed in document, not viewport)
        popup.style.position = 'absolute';
        const rect = triggerElement.getBoundingClientRect();
        popup.style.top = (rect.bottom + window.scrollY + 5) + 'px';
        popup.style.left = (rect.left + window.scrollX) + 'px';

        // Close popup when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeOnOutside(e) {
                if (!popup.contains(e.target) && e.target !== triggerElement && !triggerElement.contains(e.target)) {
                    popup.remove();
                    document.removeEventListener('click', closeOnOutside);
                }
            });
        }, 0);
    }

    /**
     * Shows a popup with port field definition details
     * @param {Object} pfd - Port field definition object
     * @param {HTMLElement} triggerElement - The element that triggered the popup
     */
    function showPortFieldDefPopup(pfd, triggerElement) {
        // Remove any existing popup
        const existingPopup = document.querySelector('.yaml-variable-popup');
        if (existingPopup) {
            existingPopup.remove();
        }

        const popup = document.createElement('div');
        popup.className = 'yaml-variable-popup';

        // Popup header
        const header = document.createElement('div');
        header.className = 'yaml-variable-popup-header';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'yaml-variable-popup-close';
        closeBtn.textContent = '✕';
        closeBtn.addEventListener('click', () => popup.remove());
        header.appendChild(closeBtn);

        popup.appendChild(header);

        // Popup content
        const content = document.createElement('div');
        content.className = 'yaml-variable-popup-content';

        // Create YAML-style display
        const yamlContent = document.createElement('pre');
        yamlContent.style.margin = '0';
        yamlContent.style.fontFamily = 'Arial';
        yamlContent.style.fontSize = '13px';
        yamlContent.style.lineHeight = '1.5';
        
        let yamlText = `${escapeHtml(pfd.port || 'Unknown')}.${escapeHtml(pfd.field || 'Unknown')} = ${escapeHtml(pfd.definition || 'Unknown')}`;
        
        yamlContent.textContent = yamlText;
        content.appendChild(yamlContent);

        popup.appendChild(content);

        document.body.appendChild(popup);

        // Position popup near the trigger element (fixed in document, not viewport)
        popup.style.position = 'absolute';
        const rect = triggerElement.getBoundingClientRect();
        popup.style.top = (rect.bottom + window.scrollY + 5) + 'px';
        popup.style.left = (rect.left + window.scrollX) + 'px';

        // Close popup when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeOnOutside(e) {
                if (!popup.contains(e.target) && e.target !== triggerElement && !triggerElement.contains(e.target)) {
                    popup.remove();
                    document.removeEventListener('click', closeOnOutside);
                }
            });
        }, 0);
    }

    /**
     * Shows a popup with port details
     * @param {Object} port - Port definition object
     * @param {HTMLElement} triggerElement - The element that triggered the popup
     */
    function showPortPopup(port, triggerElement) {
        // Remove any existing popup
        const existingPopup = document.querySelector('.yaml-variable-popup');
        if (existingPopup) {
            existingPopup.remove();
        }

        const popup = document.createElement('div');
        popup.className = 'yaml-variable-popup';

        // Popup header
        const header = document.createElement('div');
        header.className = 'yaml-variable-popup-header';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'yaml-variable-popup-close';
        closeBtn.textContent = '✕';
        closeBtn.addEventListener('click', () => popup.remove());
        header.appendChild(closeBtn);

        popup.appendChild(header);

        // Popup content
        const content = document.createElement('div');
        content.className = 'yaml-variable-popup-content';

        // Create YAML-style display
        const yamlContent = document.createElement('pre');
        yamlContent.style.margin = '0';
        yamlContent.style.fontFamily = 'Arial';
        yamlContent.style.fontSize = '13px';
        yamlContent.style.lineHeight = '1.5';
        
        let yamlText = `id: ${escapeHtml(port.id || 'Unknown Port')}`;
        
        if (port.type) {
            yamlText += `\ntype: ${escapeHtml(port.type)}`;
        }
        
        yamlContent.textContent = yamlText;
        content.appendChild(yamlContent);

        popup.appendChild(content);

        document.body.appendChild(popup);

        // Position popup near the trigger element (fixed in document, not viewport)
        popup.style.position = 'absolute';
        const rect = triggerElement.getBoundingClientRect();
        popup.style.top = (rect.bottom + window.scrollY + 5) + 'px';
        popup.style.left = (rect.left + window.scrollX) + 'px';

        // Close popup when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeOnOutside(e) {
                if (!popup.contains(e.target) && e.target !== triggerElement && !triggerElement.contains(e.target)) {
                    popup.remove();
                    document.removeEventListener('click', closeOnOutside);
                }
            });
        }, 0);
    }

    /**
     * Renders the GEMS library structure
     * @param {Object} data - Library file data
     * @param {HTMLElement} container - Target container
     */
    function renderGEMSLibrary(data, container) {
        // Preserve the library selector if it exists
        const selector = container.querySelector('.yaml-library-selector');
        const yamlUrl = container.getAttribute('data-yaml-url');
        container.innerHTML = '';
        
        // Re-add the selector if it existed
        if (selector) {
            container.appendChild(selector.cloneNode(true));
        }
        
        const lib = data.library || {};
        if (!lib || Object.keys(lib).length === 0) {
            container.innerHTML += '<p style="color: red;">Error: The library is empty</p>';
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
        
        // GitHub link button next to library name
        if (yamlUrl) {
            const githubLink = document.createElement('a');
            githubLink.href = yamlUrl.replace('raw.githubusercontent.com', 'github.com').replace('/main/', '/blob/main/');
            githubLink.target = '_blank';
            githubLink.rel = 'noopener noreferrer';
            githubLink.className = 'yaml-github-link-btn';
            githubLink.innerHTML = '🔗 GitHub';
            githubLink.title = 'View on GitHub';
            libLevel1.appendChild(githubLink);
        }
        
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
            portTitle.className = 'yaml-section-title';
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
            // Title
            const modelTitle = document.createElement('h3');
            modelTitle.className = 'yaml-section-title';
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
                    portsTitle.textContent = '🔌 Ports:';
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
                
                if (modelDef['port-field-definitions'] && Array.isArray(modelDef['port-field-definitions']) && modelDef['port-field-definitions'].length > 0) {
                    const portFieldDefsDiv = document.createElement('div');
                    portFieldDefsDiv.style.marginTop = '15px';
                    
                    const portFieldDefsTitle = document.createElement('strong');
                    portFieldDefsTitle.textContent = '📑 Port Field Definitions:';
                    portFieldDefsDiv.appendChild(portFieldDefsTitle);
                    
                    const portFieldDefsList = document.createElement('ul');
                    modelDef['port-field-definitions'].forEach(pfd => {
                        const portName = pfd.port || 'Unknown';
                        
                        const pfdLi = document.createElement('li');
                        
                        // Create button for port field definition
                        const pfdBtn = document.createElement('button');
                        pfdBtn.className = 'yaml-item-button';
                        pfdBtn.textContent = escapeHtml(portName);
                        
                        pfdBtn.addEventListener('click', (e) => {
                            showPortFieldDefPopup(pfd, e.currentTarget);
                        });
                        
                        pfdLi.appendChild(pfdBtn);
                        portFieldDefsList.appendChild(pfdLi);
                    });
                    portFieldDefsDiv.appendChild(portFieldDefsList);
                    modelContentDiv.appendChild(portFieldDefsDiv);
                }
                
                if (modelDef.parameters && Array.isArray(modelDef.parameters) && modelDef.parameters.length > 0) {
                    const paramsDiv = document.createElement('div');
                    paramsDiv.style.marginTop = '15px';
                    
                    const paramsTitle = document.createElement('strong');
                    paramsTitle.textContent = '📊 Parameters:';
                    paramsDiv.appendChild(paramsTitle);
                    
                    const paramsList = document.createElement('ul');
                    modelDef.parameters.forEach(param => {
                        const paramName = param.id || 'Unknown';
                        
                        const paramLi = document.createElement('li');
                        
                        // Create button for parameter name
                        const paramBtn = document.createElement('button');
                        paramBtn.className = 'yaml-item-button';
                        paramBtn.textContent = escapeHtml(paramName);
                        
                        paramBtn.addEventListener('click', (e) => {
                            showParameterPopup(param, e.currentTarget);
                        });
                        
                        paramLi.appendChild(paramBtn);
                        paramsList.appendChild(paramLi);
                    });
                    paramsDiv.appendChild(paramsList);
                    modelContentDiv.appendChild(paramsDiv);
                }
                
                if (modelDef.variables && Array.isArray(modelDef.variables) && modelDef.variables.length > 0) {
                    const varsDiv = document.createElement('div');
                    varsDiv.style.marginTop = '15px';
                    
                    const varsTitle = document.createElement('strong');
                    varsTitle.textContent = '🔢 Variables:';
                    varsDiv.appendChild(varsTitle);
                    
                    const varsList = document.createElement('ul');
                    modelDef.variables.forEach(variable => {
                        const varName = variable.id || 'Unknown';
                        
                        const varLi = document.createElement('li');
                        
                        // Create button for variable name
                        const varBtn = document.createElement('button');
                        varBtn.className = 'yaml-item-button';
                        varBtn.textContent = escapeHtml(varName);
                        
                        varBtn.addEventListener('click', (e) => {
                            showVariablePopup(variable, e.currentTarget);
                        });
                        
                        varLi.appendChild(varBtn);
                        varsList.appendChild(varLi);
                    });
                    varsDiv.appendChild(varsList);
                    modelContentDiv.appendChild(varsDiv);
                }
                
                if (modelDef['objective-contributions'] && Array.isArray(modelDef['objective-contributions']) && modelDef['objective-contributions'].length > 0) {
                    const objectiveDiv = document.createElement('div');
                    objectiveDiv.style.marginTop = '15px';
                    
                    const objectiveTitle = document.createElement('strong');
                    objectiveTitle.textContent = '🎯 Objective Contributions:';
                    objectiveDiv.appendChild(objectiveTitle);
                    
                    const objectiveList = document.createElement('ul');
                    modelDef['objective-contributions'].forEach(obj => {
                        const objName = obj.id || 'Unknown';
                        const objExpression = obj.expression || '';
                        
                        const objLi = document.createElement('li');
                        objLi.style.marginBottom = '12px';
                        
                        // Objective name
                        const nameSpan = document.createElement('span');
                        nameSpan.style.fontWeight = 'bold';
                        nameSpan.textContent = escapeHtml(objName);
                        objLi.appendChild(nameSpan);
                        
                        // Expression with clickable variables
                        if (objExpression) {
                            const exprSpan = document.createElement('div');
                            exprSpan.className = 'yaml-constraint-expression';
                            
                            // Parse expression and create clickable variable/parameter buttons
                            const exprText = objExpression;
                            const variableNames = Array.from(
                                new Set(modelDef.variables ? modelDef.variables.map(v => v.id).filter(Boolean) : [])
                            );
                            const parameterNames = Array.from(
                                new Set(modelDef.parameters ? modelDef.parameters.map(p => p.id).filter(Boolean) : [])
                            );
                            const allNames = [...variableNames, ...parameterNames];
                            
                            if (allNames.length > 0) {
                                // Sort by length descending to match longer names first
                                allNames.sort((a, b) => b.length - a.length);
                                
                                // Create regex pattern for all variable and parameter names
                                const pattern = new RegExp(`\\b(${allNames.map(escapeRegex).join('|')})\\b`, 'g');
                                const parts = exprText.split(pattern);
                                
                                parts.forEach((part, idx) => {
                                    if (allNames.includes(part)) {
                                        const isVariable = variableNames.includes(part);
                                        const isParameter = parameterNames.includes(part);
                                        
                                        const btn = document.createElement('button');
                                        btn.className = 'yaml-item-button';
                                        btn.textContent = escapeHtml(part);
                                        btn.dataset.name = part;
                                        btn.dataset.type = isVariable ? 'variable' : 'parameter';
                                        
                                        // Add click listener
                                        btn.addEventListener('click', (e) => {
                                            const name = e.currentTarget.dataset.name;
                                            const type = e.currentTarget.dataset.type;
                                            if (type === 'variable') {
                                                const variable = modelDef.variables && modelDef.variables.find(v => v.id === name);
                                                if (variable) {
                                                    showVariablePopup(variable, e.currentTarget);
                                                }
                                            } else if (type === 'parameter') {
                                                const parameter = modelDef.parameters && modelDef.parameters.find(p => p.id === name);
                                                if (parameter) {
                                                    showParameterPopup(parameter, e.currentTarget);
                                                }
                                            }
                                        });
                                        
                                        exprSpan.appendChild(btn);
                                    } else {
                                        appendParsedText(part, exprSpan, modelDef);
                                    }
                                });
                            } else {
                                exprSpan.textContent = escapeHtml(exprText);
                            }
                            
                            objLi.appendChild(exprSpan);
                        }
                        
                        objectiveList.appendChild(objLi);
                    });
                    objectiveDiv.appendChild(objectiveList);
                    modelContentDiv.appendChild(objectiveDiv);
                }
                
                if (modelDef['binding-constraints'] && Array.isArray(modelDef['binding-constraints']) && modelDef['binding-constraints'].length > 0) {
                    const constraintsDiv = document.createElement('div');
                    constraintsDiv.style.marginTop = '15px';
                    
                    const constraintsTitle = document.createElement('strong');
                    constraintsTitle.textContent = '⚖️ Binding Constraints:';
                    constraintsDiv.appendChild(constraintsTitle);
                    
                    const constraintsList = document.createElement('ul');
                    modelDef['binding-constraints'].forEach(constraint => {
                        const constraintName = constraint.id || 'Unknown';
                        const constraintExpression = constraint.expression || '';
                        
                        const constraintLi = document.createElement('li');
                        constraintLi.style.marginBottom = '12px';
                        
                        // Constraint name
                        const nameSpan = document.createElement('span');
                        nameSpan.style.fontWeight = 'bold';
                        nameSpan.textContent = escapeHtml(constraintName);
                        constraintLi.appendChild(nameSpan);
                        
                        // Expression with clickable variables
                        if (constraintExpression) {
                            const exprSpan = document.createElement('div');
                            exprSpan.className = 'yaml-constraint-expression';
                            
                            // Parse expression and create clickable variable/parameter buttons
                            const exprText = constraintExpression;
                            const variableNames = Array.from(
                                new Set(modelDef.variables ? modelDef.variables.map(v => v.id).filter(Boolean) : [])
                            );
                            const parameterNames = Array.from(
                                new Set(modelDef.parameters ? modelDef.parameters.map(p => p.id).filter(Boolean) : [])
                            );
                            const allNames = [...variableNames, ...parameterNames];
                            
                            if (allNames.length > 0) {
                                // Sort by length descending to match longer names first
                                allNames.sort((a, b) => b.length - a.length);
                                
                                // Create regex pattern for all variable and parameter names
                                const pattern = new RegExp(`\\b(${allNames.map(escapeRegex).join('|')})\\b`, 'g');
                                const parts = exprText.split(pattern);
                                
                                parts.forEach((part, idx) => {
                                    if (allNames.includes(part)) {
                                        const isVariable = variableNames.includes(part);
                                        const isParameter = parameterNames.includes(part);
                                        
                                        const btn = document.createElement('button');
                                        btn.className = 'yaml-item-button';
                                        btn.textContent = escapeHtml(part);
                                        btn.dataset.name = part;
                                        btn.dataset.type = isVariable ? 'variable' : 'parameter';
                                        
                                        // Add click listener
                                        btn.addEventListener('click', (e) => {
                                            const name = e.currentTarget.dataset.name;
                                            const type = e.currentTarget.dataset.type;
                                            if (type === 'variable') {
                                                const variable = modelDef.variables && modelDef.variables.find(v => v.id === name);
                                                if (variable) {
                                                    showVariablePopup(variable, e.currentTarget);
                                                }
                                            } else if (type === 'parameter') {
                                                const parameter = modelDef.parameters && modelDef.parameters.find(p => p.id === name);
                                                if (parameter) {
                                                    showParameterPopup(parameter, e.currentTarget);
                                                }
                                            }
                                        });
                                        
                                        exprSpan.appendChild(btn);
                                    } else {
                                        appendParsedText(part, exprSpan, modelDef);
                                    }
                                });
                            } else {
                                exprSpan.textContent = escapeHtml(exprText);
                            }
                            
                            constraintLi.appendChild(exprSpan);
                        }
                        
                        constraintsList.appendChild(constraintLi);
                    });
                    constraintsDiv.appendChild(constraintsList);
                    modelContentDiv.appendChild(constraintsDiv);
                }
                
                if (modelDef.constraints && Array.isArray(modelDef.constraints) && modelDef.constraints.length > 0) {
                    const constraintsDiv = document.createElement('div');
                    constraintsDiv.style.marginTop = '15px';
                    
                    const constraintsTitle = document.createElement('strong');
                    constraintsTitle.textContent = '⚖️ Constraints:';
                    constraintsDiv.appendChild(constraintsTitle);
                    
                    const constraintsList = document.createElement('ul');
                    modelDef.constraints.forEach(constraint => {
                        const constraintName = constraint.id || 'Unknown';
                        const constraintExpression = constraint.expression || '';
                        
                        const constraintLi = document.createElement('li');
                        constraintLi.style.marginBottom = '12px';
                        
                        // Constraint name
                        const nameSpan = document.createElement('span');
                        nameSpan.style.fontWeight = 'bold';
                        nameSpan.textContent = escapeHtml(constraintName);
                        constraintLi.appendChild(nameSpan);
                        
                        // Expression with clickable variables
                        if (constraintExpression) {
                            const exprSpan = document.createElement('div');
                            exprSpan.className = 'yaml-constraint-expression';
                            
                            // Parse expression and create clickable variable/parameter buttons
                            const exprText = constraintExpression;
                            const variableNames = Array.from(
                                new Set(modelDef.variables ? modelDef.variables.map(v => v.id).filter(Boolean) : [])
                            );
                            const parameterNames = Array.from(
                                new Set(modelDef.parameters ? modelDef.parameters.map(p => p.id).filter(Boolean) : [])
                            );
                            const allNames = [...variableNames, ...parameterNames];
                            
                            if (allNames.length > 0) {
                                // Sort by length descending to match longer names first
                                allNames.sort((a, b) => b.length - a.length);
                                
                                // Create regex pattern for all variable and parameter names
                                const pattern = new RegExp(`\\b(${allNames.map(escapeRegex).join('|')})\\b`, 'g');
                                const parts = exprText.split(pattern);
                                
                                parts.forEach((part, idx) => {
                                    if (allNames.includes(part)) {
                                        const isVariable = variableNames.includes(part);
                                        const isParameter = parameterNames.includes(part);
                                        
                                        const btn = document.createElement('button');
                                        btn.className = 'yaml-item-button';
                                        btn.textContent = escapeHtml(part);
                                        btn.dataset.name = part;
                                        btn.dataset.type = isVariable ? 'variable' : 'parameter';
                                        
                                        // Add click listener
                                        btn.addEventListener('click', (e) => {
                                            const name = e.currentTarget.dataset.name;
                                            const type = e.currentTarget.dataset.type;
                                            if (type === 'variable') {
                                                const variable = modelDef.variables && modelDef.variables.find(v => v.id === name);
                                                if (variable) {
                                                    showVariablePopup(variable, e.currentTarget);
                                                }
                                            } else if (type === 'parameter') {
                                                const parameter = modelDef.parameters && modelDef.parameters.find(p => p.id === name);
                                                if (parameter) {
                                                    showParameterPopup(parameter, e.currentTarget);
                                                }
                                            }
                                        });
                                        
                                        exprSpan.appendChild(btn);
                                    } else {
                                        appendParsedText(part, exprSpan, modelDef);
                                    }
                                });
                            } else {
                                exprSpan.textContent = escapeHtml(exprText);
                            }
                            
                            constraintLi.appendChild(exprSpan);
                        }
                        
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
        
        // Click on library button (reset everything)
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
                
                // Toggle port content
                const portContent = libContent.querySelector(`.yaml-library-port-content[data-port="${portData}"]`);
                const isCurrentlyVisible = portContent && portContent.style.display === 'block';
                
                if (isCurrentlyVisible) {
                    // Hide the port if already visible
                    portContent.style.display = 'none';
                    e.currentTarget.classList.remove('active');
                } else {
                    // Hide all ports, then show the selected one
                    libContent.querySelectorAll('.yaml-library-port-content').forEach(el => el.style.display = 'none');
                    libContent.querySelectorAll('.yaml-library-button-port').forEach(btn => btn.classList.remove('active'));
                    
                    if (portContent) {
                        portContent.style.display = 'block';
                        e.currentTarget.classList.add('active');
                    }
                }
                
                // Hide library info when viewing specific content
                if (portContent && portContent.style.display === 'block') {
                    libInfo.style.display = 'none';
                    libButton.classList.remove('active');
                }
            });
        });
        
        libContent.querySelectorAll('.yaml-library-button-model').forEach(modelBtn => {
            modelBtn.addEventListener('click', (e) => {
                const modelData = e.currentTarget.dataset.model;
                
                // Toggle model content
                const modelContent = libContent.querySelector(`.yaml-library-model-content[data-model="${modelData}"]`);
                const isCurrentlyVisible = modelContent && modelContent.style.display === 'block';
                
                if (isCurrentlyVisible) {
                    // Hide the model if already visible
                    modelContent.style.display = 'none';
                    e.currentTarget.classList.remove('active');
                } else {
                    // Hide all models, then show the selected one
                    libContent.querySelectorAll('.yaml-library-model-content').forEach(el => el.style.display = 'none');
                    libContent.querySelectorAll('.yaml-library-button-model').forEach(btn => btn.classList.remove('active'));
                    
                    if (modelContent) {
                        modelContent.style.display = 'block';
                        e.currentTarget.classList.add('active');
                    }
                }
                
                // Hide library info when viewing specific content
                if (modelContent && modelContent.style.display === 'block') {
                    libInfo.style.display = 'none';
                    libButton.classList.remove('active');
                }
            });
        });
        
        libContent.querySelectorAll('.yaml-port-reference').forEach(portRef => {
            portRef.addEventListener('click', (e) => {
                const portRefData = e.currentTarget.dataset.portRef;
                const correspondingPortBtn = libContent.querySelector(`.yaml-library-button-port[data-port="${portRefData}"]`);
                const portContent = libContent.querySelector(`.yaml-library-port-content[data-port="${portRefData}"]`);
                
                if (correspondingPortBtn && portContent) {
                    // Force display without toggle - hide other ports only
                    libContent.querySelectorAll('.yaml-library-port-content').forEach(el => {
                        if (el.dataset.port !== portRefData) {
                            el.style.display = 'none';
                        }
                    });
                    libContent.querySelectorAll('.yaml-library-button-port').forEach(btn => {
                        if (btn.dataset.port !== portRefData) {
                            btn.classList.remove('active');
                        }
                    });
                    
                    // Always show the referenced port
                    portContent.style.display = 'block';
                    correspondingPortBtn.classList.add('active');
                    
                    // Hide library info
                    libInfo.style.display = 'none';
                    libButton.classList.remove('active');
                    
                    // Scroll to button
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
     * Gets cached YAML data from localStorage
     * @param {string} yamlUrl - URL of the YAML file
     * @returns {string|null} Cached YAML string or null if not found
     */
    function getFromCache(yamlUrl) {
        try {
            const cacheKey = `yaml-loader-cache-${btoa(yamlUrl)}`;
            const cached = localStorage.getItem(cacheKey);
            if (cached) {
                const data = JSON.parse(cached);
                // Check if cache is still valid (24 hours)
                if (Date.now() - data.timestamp < 24 * 60 * 60 * 1000) {
                    return data.content;
                } else {
                    localStorage.removeItem(cacheKey);
                }
            }
        } catch (error) {
            console.warn('Cache read error:', error);
        }
        return null;
    }

    /**
     * Saves YAML data to localStorage cache
     * @param {string} yamlUrl - URL of the YAML file
     * @param {string} content - YAML content to cache
     */
    function saveToCache(yamlUrl, content) {
        try {
            const cacheKey = `yaml-loader-cache-${btoa(yamlUrl)}`;
            const data = {
                content: content,
                timestamp: Date.now()
            };
            localStorage.setItem(cacheKey, JSON.stringify(data));
        } catch (error) {
            console.warn('Cache write error:', error);
        }
    }

    /**
     * Loads and parses a YAML file from a URL
     * @param {string} yamlUrl - URL of the raw YAML file (raw.githubusercontent.com)
     * @returns {Promise} YAML string on success, throws error otherwise
     */
    async function fetchYAML(yamlUrl) {
        try {
            // Try to get from cache first
            const cached = getFromCache(yamlUrl);
            if (cached) {
                return cached;
            }

            const response = await fetch(yamlUrl);
            
            if (!response.ok) {
                throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
            }

            const text = await response.text();
            
            if (!text.trim()) {
                throw new Error('The YAML file is empty.');
            }

            // Save to cache
            saveToCache(yamlUrl, text);

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
     * Displays a loading spinner in the container
     * @param {HTMLElement} container - Target container
     * @param {string} libraryName - Name of the library being loaded
     */
    function displayLoadingSpinner(container, libraryName) {
        // Preserve the library selector if it exists
        const selector = container.querySelector('.yaml-library-selector');
        const selectorClone = selector ? selector.cloneNode(true) : null;
        
        container.innerHTML = '';
        container.classList.add(CONFIG.LOADING_CLASS);
        
        // Re-add the selector if it existed
        if (selectorClone) {
            container.appendChild(selectorClone);
        }
        
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'yaml-loader-spinner-wrapper';
        
        const spinner = document.createElement('div');
        spinner.className = 'yaml-loader-spinner';
        
        const text = document.createElement('p');
        text.className = 'yaml-loader-loading-text';
        text.textContent = `Loading ${libraryName} libraries...`;
        
        loadingDiv.appendChild(spinner);
        loadingDiv.appendChild(text);
        container.appendChild(loadingDiv);
    }

    /**
     * Main function: loads and displays YAML content
     * @param {HTMLElement} container - HTML container to display content
     * @param {string} yamlUrl - URL of the YAML file
     */
    async function loadYAML(container, yamlUrl) {
        const libraryName = container.getAttribute('data-library-name') || 'YAML';
        
        // Show loading state with spinner
        displayLoadingSpinner(container, libraryName);

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

            // Reinitialize library nav buttons if they exist
            initializeLibraryNavButtons();

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

    /**
     * Initializes library navigation buttons
     */
    function initializeLibraryNavButtons() {
        const navButtons = document.querySelectorAll('.yaml-library-nav-btn');
        const mainContainer = document.getElementById('yaml-loader-main');

        if (!mainContainer || navButtons.length === 0) {
            return;
        }

        navButtons.forEach(button => {
            button.addEventListener('click', () => {
                const yamlUrl = button.getAttribute('data-url');
                const libraryName = button.getAttribute('data-name');

                // Update active button
                navButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                // Update container attributes and reload
                mainContainer.setAttribute('data-yaml-url', yamlUrl);
                mainContainer.setAttribute('data-library-name', libraryName);

                // Load the new YAML
                loadYAML(mainContainer, yamlUrl);

                // Scroll to container
                mainContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initializeYAMLLoaders();
            initializeLibraryNavButtons();
        });
    } else {
        // If script is loaded after DOM
        initializeYAMLLoaders();
        initializeLibraryNavButtons();
    }

    // Expose loadYAML function globally for manual usage
    window.loadYAMLFile = loadYAML;
})();
