const { DialogflowClient } = require('@google-cloud/dialogflow-cx');

class NLInterface {
  constructor(projectId, location) {
    this.client = new DialogflowClient({
      projectId: projectId,
      location: location,
    });
  }

  // Create a new intents entity type
  async createEntityTypeName(name, values) {
    const [response] = await this.client.createEntityType(
      'projects/${projectId}/locations/${location}/agents/default_agent',
      {
        name: name,
        values: values.map(val => ({ value: val })),
        kind: 'VALUE',
      }
    );
    return response;
  }

  // Create a new intent
  async createIntent(displayName, trainingExamples) {
    const [response] = await this.client.createIntent(
      'projects/${projectId}/locations/${location}/agents/default_agent/intents',
      {
        displayName: displayName,
        trainingExamples: trainingExamples.map(example => ({
          content: example,
          intent: 'projects/${projectId}/locations/${location}/agents/default_agent/intents/${intentId}',
        })),
      }
    );
    return response;
  }
}

module.exports = NLInterface;