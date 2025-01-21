class TestCard extends HTMLElement {
    setConfig(config) {
        const root = this.attachShadow({ mode: "open" });
        root.innerHTML = `<ha-card><h1>Hello from Test Card!</h1></ha-card>`;
    }
}
export default TestCard;
