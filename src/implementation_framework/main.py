# Main entry point for the implementation framework

from .core import AnalysisFramework
from .strategies import deployment_strategies

__all__ = ['run_analysis', 'deploy']

def run_analysis(config_path: str) -> Dict[str, Any]:
    """Entry point for running analysis."""
    # Load configuration
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    # Create and run analysis framework
    analysis_framework = AnalysisFramework(config)
    results = analysis_framework.run_analysis()
    
    # Print summary
    print(analysis_framework.get_summary())
    
    return results


def deploy(config_path: str, strategy: str = 'rolling'):
    """Entry point for deployment."""
    from kubernetes import client, config
    
    # Load kube config
    config.load_kubernetes_config()
    
    # Create API client
    api_instance = client.AppsV1Api()
    batch_api = client.BatchV1Api()
    
    # Load deployment config
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        
    # Generate deployment spec
    deployment_spec = deployment_strategies[strategy](config)
    
    # Create or update deployment
    try:
        api_response = api_instance.replace_namespaced_deployment(
            name=config['service_name'],
            namespace='default',
            body=deployment_spec
        )
        print(f"Deployment updated: {api_response.metadata.name}")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            print("Deployment not found, creating new...")
            api_response = api_instance.create_namespaced_deployment(
                namespace='default',
                body=deployment_spec
            )
            print(f"Deployment created: {api_response.metadata.name}")
        else:
            print(f"Exception when calling API: {e}")
            raise

    return api_response