import sys
import boto3
from boto3.dynamodb.conditions import Key

# Global setting for language
lang = "E"

# Retrieve a string in the data store by its key
def get_app_string(string_key):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Bölgeyi buraya ekle
    table = dynamodb.Table('app_strings')
    response = table.query(KeyConditionExpression=Key("string_key").eq(string_key))
    return response["Items"][0]["string_value"]

def welcome_message():
    global lang
    # Retrieve and print welcome message
    welcome_key = f"str0001{lang}"
    developer_key = f"str0002{lang}"
    print(get_app_string(welcome_key))  # Welcome message
    print(get_app_string(developer_key))  # Developer message

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ('F', 'f', 'fr', 'FR', 'fra', 'FRA'):
            lang = 'F'
        elif sys.argv[1] in ('S', 's', 'sp', 'SP', 'spa', 'SPA'):
            lang = 'S'
        elif sys.argv[1] in ('E', 'e', 'en', 'EN'):
            lang = 'E'
    welcome_message()
