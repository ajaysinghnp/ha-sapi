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
        } catch (error) {
            console.error("Error generating password:", error);
            this.password = "Error generating password";
            this.render();
        } finally {
            this.isLoading = false;
            this.render();
        }
    }

    copyToClipboard() {
        navigator.clipboard.writeText(this.password).then(() => {
            alert("Password copied to clipboard!");
        });
    }

    render() {
        if (!this.content) {
            this.innerHTML = `
                <ha-card header="${this.config.title}">
                    <div class="card-content">
                        <div class="password-output">${this.password || "Click 'Generate' to create a password"}</div>
                        <div class="button-container">
                            <mwc-button raised class="generate-button">Generate</mwc-button>
                            <mwc-button raised class="copy-button" disabled>Copy</mwc-button>
                        </div>
                    </div>
                    <style>
                        .card-content {
                            padding: 16px;
                            text-align: center;
                        }
                        .password-output {
                            font-family: monospace;
                            padding: 12px;
                            margin: 16px 0;
                            background: var(--card-background-color);
                            border-radius: 8px;
                            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
                            min-height: 24px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                        }
                        .loading {
                            animation: spin 1s linear infinite;
                            border: 4px solid transparent;
                            border-top: 4px solid var(--primary-color);
                            border-radius: 50%;
                            width: 24px;
                            height: 24px;
                            margin: auto;
                        }
                        .button-container {
                            display: flex;
                            justify-content: space-evenly;
                            align-items: center;
                        }
                        @keyframes spin {
                            from { transform: rotate(0deg); }
                            to { transform: rotate(360deg); }
                        }
                    </style>
                </ha-card>
            `;

            this.content = this.querySelector(".password-output");
            this.generateButton = this.querySelector(".generate-button");
            this.copyButton = this.querySelector(".copy-button");

            this.generateButton.addEventListener("click", () => this.generatePassword());
            this.copyButton.addEventListener("click", () => this.copyToClipboard());
        }

        if (this.content) {
            this.content.innerHTML = this.isLoading
                ? '<div class="loading"></div>'
                : this.password || "Click 'Generate' to create a password";
        }

        if (this.generateButton) {
            this.generateButton.disabled = this.isLoading; // Disable while loading
        }

        if (this.copyButton) {
            this.copyButton.disabled = !this.password || this.isLoading;
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
