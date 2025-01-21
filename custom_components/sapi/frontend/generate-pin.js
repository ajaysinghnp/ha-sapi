const DOMAIN = "sapi";

class PinGeneratorCard extends HTMLElement {
    static get properties() {
        return {
            hass: {},
            config: {}
        };
    }

    // Add type to make it show up in the card picker
    static getStubConfig(hass) {
        return {
            type: "sapi:pin-generator-card",
            title: "PIN Generator",
            length: 4,
            editor: true
        };
    }

    // Add editor support
    static getConfigElement() {
        return document.createElement("pin-generator-card-editor");
    }

    setConfig(config) {
        if (!config) {
            throw new Error("Invalid configuration");
        }
        this.config = {
            title: config.title || "PIN Generator",
            length: config.length || 4
        };

        this.pin = "";
        this.isLoading = false;
        this.render();
    }

    set hass(hass) {
        this._hass = hass;
    }

    async generatePin() {
        this.isLoading = true;
        this.hintText = "";
        this.render();
        try {
            const result = await this._hass.callService(DOMAIN, 'generate_pin', {
                length: this.config.length
            });

            // Access the response from the correct path in the result
            // You might need to adjust this based on your service's actual response structure
            const lastEntity = this._hass.states[`${DOMAIN}.generate_pin`];
            if (lastEntity) {
                this.pin = lastEntity.state;
            } else {
                // If your service returns the pin directly in the result
                this.pin = typeof result === 'string' ? result :
                    result?.pin ||
                    result?.result ||
                    'PIN generated but unable to display';
            }
            this.hintText = "PIN generated successfully!";
            this.hintState = "success";
        } catch (error) {
            console.error("Error generating PIN:", error);
            this.pin = "";
            this.hintText = "Failed to generate PIN.";
            this.hintState = "error";
        } finally {
            this.isLoading = false;
            this.render();
        }
    }

    copyToClipboard() {
        if (!this.pin) return;

        this.hintText = "";
        this.render();

        navigator.clipboard.writeText(this.pin).then(() => {
            this.hintText = "PIN copied to clipboard!";
            this.hintState = "success";
        }).catch(() => {
            this.hintText = "Failed to copy PIN.";
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
                        <div class="pin-output">${this.pin || "Generated PIN will appear here"}</div>
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
                        .pin-output {
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
            this.pinOutput = this.querySelector(".pin-output");
            this.hintTextElement = this.querySelector(".hint");

            this.generateButton.addEventListener("click", () => this.generatePin());
            this.copyButton.addEventListener("click", () => this.copyToClipboard());
        }

        if (this.pinOutput) {
            this.pinOutput.textContent = this.pin || "Generated PIN will appear here";
        }

        if (this.generateButton) {
            this.generateButton.disabled = this.isLoading;
            this.generateButton.classList.toggle("loading", this.isLoading);
        }

        if (this.copyButton) {
            this.copyButton.disabled = !this.pin || this.isLoading;
        }

        if (this.hintTextElement) {
            this.hintTextElement.textContent = this.hintText || "";
            this.hintTextElement.className = `hint ${this.hintState || ""}`;
        }
    }
}

class PinGeneratorCardEditor extends HTMLElement {
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
                    ${this._createField("length", "PIN Length", "number")}
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
        this.querySelector("[id='length']").value = this.config.length || 6;
    }

    _createField(id, label, type) {
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
            type: "custom:pin-generator-card" // Ensure type is preserved
        };

        if (field.type === "number") {
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
customElements.define("pin-generator-card", PinGeneratorCard);
customElements.define("pin-generator-card-editor", PinGeneratorCardEditor);
