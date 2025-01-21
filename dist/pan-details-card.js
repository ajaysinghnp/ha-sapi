const DOMAIN = "sapi";

class PanDetailsCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  setConfig(config) {
    if (!config.service) {
      throw new Error("Please define a service");
    }
    this.config = config;

    this.shadowRoot.innerHTML = `
        <ha-card header="PAN Details">
          <div class="card-content">
            <div class="input-row">
              <paper-input
                label="Enter PAN Number"
                .value="${this._panNumber || ""}"
                @change="${this._handleInputChange}"
              ></paper-input>
              <mwc-button @click="${this._fetchPanDetails}">
                Fetch Details
              </mwc-button>
            </div>
            <div class="details-container" id="detailsContainer">
              <!-- Results will be populated here -->
            </div>
          </div>
        </ha-card>

        <style>
          ha-card {
            padding: 16px;
          }
          .card-content {
            padding: 16px;
          }
          .input-row {
            display: flex;
            gap: 16px;
            margin-bottom: 16px;
          }
          paper-input {
            flex-grow: 1;
          }
          .details-container {
            margin-top: 16px;
          }
          .detail-item {
            padding: 8px 0;
            border-bottom: 1px solid var(--divider-color);
          }
          .detail-item:last-child {
            border-bottom: none;
          }
        </style>
      `;
  }

  _handleInputChange(e) {
    this._panNumber = e.target.value;
  }

  async _fetchPanDetails() {
    if (!this._panNumber) {
      this._showError("Please enter a PAN number");
      return;
    }

    const detailsContainer = this.shadowRoot.getElementById("detailsContainer");
    detailsContainer.innerHTML = "<div>Loading...</div>";

    try {
      const response = await this._hass.callService(
        this.config.service.split(".")[0],
        this.config.service.split(".")[1],
        { pan_number: this._panNumber }
      );

      if (response) {
        detailsContainer.innerHTML = this._formatPanDetails(response);
      } else {
        this._showError("No data received");
      }
    } catch (error) {
      this._showError(`Error: ${error.message}`);
    }
  }

  _formatPanDetails(details) {
    return Object.entries(details)
      .map(
        ([key, value]) => `
          <div class="detail-item">
            <strong>${key.replace(/_/g, " ").toUpperCase()}:</strong> ${value}
          </div>
        `
      )
      .join("");
  }

  _showError(message) {
    const detailsContainer = this.shadowRoot.getElementById("detailsContainer");
    detailsContainer.innerHTML = `<div style="color: var(--error-color)">${message}</div>`;
  }

  set hass(hass) {
    this._hass = hass;
  }

  static getStubConfig() {
    return {
      service: `${DOMAIN}.get_pan_details`,
    };
  }
}

export default PanDetailsCard;
