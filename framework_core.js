export class Framework {
  constructor() {
    this.layers = {
      foundation: [],
      analysis: [],
      implementation: [],
      validation: []
    };
  }

  addComponent(layer, component) {
    if (this.layers[layer]) {
      this.layers[layer].push(component);
    }
  }

  getLayer(layer) {
    return this.layers[layer] || [];
  }
}