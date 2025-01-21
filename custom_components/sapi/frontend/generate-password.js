const DOMAIN = "sapi";

class PasswordGeneratorCard extends HTMLElement {
    static get properties() {
        return {
            hass: {},
            config: {}
        };
    }

    // Add type to make it show up in the card picker
    static getStubConfig(hass) {
        return {
            type: "custom:password-generator-card",
            title: "Password Generator",
            length: 12,
            special: true,
            editor: true
        };
    }

    // Add editor support
    static getConfigElement() {
        return document.createElement("password-generator-card-editor");
    }

    setConfig(config) {
        if (!config) {
            throw new Error("Invalid configuration");
        }
        this.config = {
            title: config.title || "Password Generator",
            length: config.length || 12,
            special: config.special !== undefined ? config.special : true
        };

        this.password = "";
        this.isLoading = false;
        this.render();
    }

    set hass(hass) {
        this._hass = hass;
    }

    async generatePassword() {
        this.isLoading = true;
        this.hintText = "";
        this.render();
        try {
            const result = await this._hass.callService(DOMAIN, 'generate_password', {
                length: this.config.length,
                special: this.config.special
            });

            // Access the response from the correct path in the result
            // You might need to adjust this based on your service's actual response structure
            // Log the result to see its structure

            // Wait for the state change after service call
            await new Promise(resolve => setTimeout(resolve, 100));

            // Get the latest generated password from an entity if your service updates one
            // If your service returns the password directly in the response, adjust accordingly
            const lastEntity = this._hass.states[`${DOMAIN}.generate_password`];
            if (lastEntity) {
                this.password = lastEntity.state;
            } else {
                // If your service returns the password directly in the result
                this.password = typeof result === 'string' ? result :
                    result?.password ||
                    result?.result ||
                    'Password generated but unable to display';
            }
            this.hintText = "Password generated successfully!";
            this.hintState = "success";
        } catch (error) {
            console.error("Error generating password:", error);
            this.password = "";
            this.hintText = "Failed to generate password.";
            this.hintState = "error";
        } finally {
            this.isLoading = false;
            this.render();
        }
    }

    copyToClipboard() {
        if (!this.password) return;

        this.hintText = "";
        this.render();

        navigator.clipboard.writeText(this.password).then(() => {
            this.hintText = "Password copied to clipboard!";
            this.hintState = "success";
        }).catch(() => {
            this.hintText = "Failed to copy password.";
            this.hintState = "error";
        }).finally(() => {
            this.render();
        });
    }

    render() {
        if (!this.content) {
            this.innerHTML = `
                <ha-card>
                    <div class="row">
                        <span class="title">${this.config.title}</span>
                        <mwc-button raised class="generate-button" title="Generate">
                            <ha-icon icon="mdi:refresh"></ha-icon>
                        </mwc-button>
                    </div>
                    <div class="row">
                        <div class="password-output">${this.password || "Generated password will appear here"}</div>
                        <mwc-button raised class="copy-button" title="Copy" disabled>
                            <ha-icon icon="mdi:content-copy"></ha-icon>
                        </mwc-button>
                    </div>
                    <div class="hint">${this.hintText || ""}</div>
                    <style>
                        ha-card {
                            padding: 16px;
                            display: flex;
                            flex-direction: column;
                            gap: 12px;
                            font-family: Arial, sans-serif;
                            line-height: 1.5;
                        }
                        .row {
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        }
                        .title {
                            font-size: 1.2em;
                            font-weight: bold;
                        }
                        .password-output {
                            font-family: monospace;
                            padding: 8px;
                            background: var(--primary-background-color);
                            border: 1px solid var(--divider-color);
                            border-radius: 4px;
                            flex: 1;
                            margin-right: 8px;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        }
                        .hint {
                            font-size: 0.9em;
                            text-align: center;
                            color: var(--secondary-text-color);
                        }
                        .hint.success {
                            color: var(--success-color);
                        }
                        .hint.error {
                            color: var(--error-color);
                        }
                        mwc-button[disabled] {
                            position: relative;
                        }
                        mwc-button[disabled].loading ha-icon {
                            display: none;
                        }
                        mwc-button[disabled].loading::after {
                            content: '';
                            border: 3px solid transparent;
                            border-top-color: var(--primary-color);
                            border-radius: 50%;
                            width: 16px;
                            height: 16px;
                            animation: spin 1s linear infinite;
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                        }
                        @keyframes spin {
                            from { transform: translate(-50%, -50%) rotate(0deg); }
                            to { transform: translate(-50%, -50%) rotate(360deg); }
                        }
                    </style>
                </ha-card>
            `;

            this.generateButton = this.querySelector(".generate-button");
            this.copyButton = this.querySelector(".copy-button");
            this.passwordOutput = this.querySelector(".password-output");
            this.hintTextElement = this.querySelector(".hint");

            this.generateButton.addEventListener("click", () => this.generatePassword());
            this.copyButton.addEventListener("click", () => this.copyToClipboard());
        }

        if (this.passwordOutput) {
            this.passwordOutput.textContent = this.password || "Generated password will appear here";
        }

        if (this.generateButton) {
            this.generateButton.disabled = this.isLoading;
            this.generateButton.classList.toggle("loading", this.isLoading);
        }

        if (this.copyButton) {
            this.copyButton.disabled = !this.password || this.isLoading;
        }

        if (this.hintTextElement) {
            this.hintTextElement.textContent = this.hintText || "";
            this.hintTextElement.className = `hint ${this.hintState || ""}`;
        }
    }

}

class PasswordGeneratorCardEditor extends HTMLElement {
    setConfig(config) {
        this.config = { ...config };
        this.render();
    }

    set hass(hass) {
        this._hass = hass;
    }

    render() {
        if (!this.innerHTML) {
            this.innerHTML = `
                <form class="form">
                    ${this._createField("title", "Title", "text")}
                    ${this._createField("length", "Password Length", "number")}
                    ${this._createField("special", "Include Special Characters", "checkbox")}
                </form>
                <style>
                    .form {
                        display: flex;
                        flex-direction: column;
                        gap: 12px;
                    }
                    .form-field {
                        display: flex;
                        flex-direction: column;
                    }
                </style>
            `;

            // Add event listeners
            const fields = this.querySelectorAll("ha-textfield, ha-switch");
            fields.forEach(field => {
                field.addEventListener("change", () => this._valueChanged(field));
            });
        }

        // Set initial values
        this.querySelector("[id='title']").value = this.config.title || "";
        this.querySelector("[id='length']").value = this.config.length || 12;
        this.querySelector("[id='special']").checked = this.config.special !== undefined ? this.config.special : true;
    }

    _createField(id, label, type) {
        if (type === "checkbox") {
            return `
                <div class="form-field">
                    <ha-switch
                        id="${id}"
                        label="${label}"
                        .checked="${this.config[id] || false}"
                    ></ha-switch>
                    <label>${label}</label>
                </div>
            `;
        }
        return `
            <div class="form-field">
                <ha-textfield
                    id="${id}"
                    label="${label}"
                    type="${type}"
                    .value="${this.config[id] || ''}"
                ></ha-textfield>
            </div>
        `;
    }

    _valueChanged(field) {
        if (!this.config || !this._hass) return;

        const newConfig = {
            ...this.config,
            type: "custom:password-generator-card" // Ensure type is preserved
        };

        if (field.type === "checkbox") {
            newConfig[field.id] = field.checked;
        } else if (field.type === "number") {
            newConfig[field.id] = parseInt(field.value);
        } else {
            newConfig[field.id] = field.value;
        }

        // Fire the config changed event
        const event = new CustomEvent("config-changed", {
            detail: { config: newConfig },
            bubbles: true,
            composed: true
        });
        this.dispatchEvent(event);
    }
}

// Register both the card and its editor
customElements.define("password-generator-card", PasswordGeneratorCard);
customElements.define("password-generator-card-editor", PasswordGeneratorCardEditor);
