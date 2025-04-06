from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


def main():
    global cog_endpoint
    global cog_key

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = 'https://azml0608.cognitiveservices.azure.com/' #os.getenv('COG_SERVICE_ENDPOINT')
        key_vault_name = 'azkv0608' #os.getenv('KEY_VAULT')
        app_tenant = '3e04753a-ae5b-42d4-a86d-d6f05460f9e4' #os.getenv('TENANT_ID')
        app_id = '2a71841f-f58f-46f9-847e-e78287910918' #os.getenv('APP_ID')
        app_password = 'v1l_nL.rcb-SSVFlO7W0cw0v~WClvdeY87' #os.getenv('APP_PASSWORD')

        # Get cognitive services key from keyvault using the service principal credentials
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
        credential = ClientSecretCredential(app_tenant, app_id, app_password)
        keyvault_client = SecretClient(key_vault_uri, credential)
        secret_key = keyvault_client.get_secret("Cognitive-Services-Key")
        cog_key = secret_key.value

        # Get user input (until they enter "quit")
        userText =''
        while userText.lower() != 'quit':
            userText = input('\nEnter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                language = GetLanguage(userText)
                print('Language:', language)

    except Exception as ex:
        print(ex)

def GetLanguage(text):

    # Create client using endpoint and key
    credential = AzureKeyCredential(cog_key)
    client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

    # Call the service to get the detected language
    detectedLanguage = client.detect_language(documents = [text])[0]
    return detectedLanguage.primary_language.name


if __name__ == "__main__":
    main()