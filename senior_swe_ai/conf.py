"""config sys module to get the system information"""
import os
import platform
import getpass
from typing import Any
import openai
import toml
from inquirer import Confirm, prompt, List
from senior_swe_ai.consts import EmbeddingsModel


def get_config_path() -> str:
    """ Get the configuration file path """
    sys: str = platform.system()

    if sys in ('Linux', 'Darwin'):
        config_dir: str = os.path.expanduser('~/.config/senior_swe_ai')
    elif sys == 'Windows':
        config_dir: str = os.path.expanduser('~/AppData/Roaming/senior_swe_ai')
    else:
        raise NotImplementedError(f'Unsupported system: {sys}')

    conf_file_path: str = os.path.join(config_dir, 'conf.toml')
    return conf_file_path


def config_init() -> None:
    """ Initialize the app """

    conf_file_path: str = get_config_path()

    if os.path.exists(conf_file_path):
        print('The app has already been initialized')
        questions: list[Confirm] = [
            Confirm('overwrite',
                    message='Do you want to overwrite the configuration?')
        ]
        answers: dict[Any, Any] | None = prompt(questions)

        if not answers['overwrite']:
            return

    os.makedirs(os.path.dirname(conf_file_path), exist_ok=True)

    try:

        api_key: str = os.environ['OPENAI_API_KEY']

    except KeyError:

        api_validate = False

        while api_validate is False:
            api_key: str = getpass.getpass('Enter your OpenAI API key: ')
            api_validate: bool = validate_api_key(api_key.strip())
            if api_validate is False:
                print('Invalid API key. Please try again.')

    question: list[Confirm] = [
        List(
            'embed_model',
            message='Choose the embeddings model',
            choices=[
                EmbeddingsModel.OPENAI_TEXT_EMBEDDING_ADA_002.value,
                EmbeddingsModel.OPENAI_TEXT_EMBEDDING_3_SMALL.value
            ],
            default=EmbeddingsModel.OPENAI_TEXT_EMBEDDING_ADA_002.value
        ),
    ]
    answers: dict[str, str] = prompt(question)

    conf: dict[str, str] = {
        'api_key': api_key,
        'username': get_username(),
        'embed_model': answers['embed_model'],
        'chat_model': 'gpt-3.5-turbo'
    }
    save_conf(conf)


def validate_api_key(api_key: str) -> bool:
    """ Validate the OpenAI API key"""

    try:
        # Make a simple request to the API
        client = openai.OpenAI(api_key=api_key)
        # openai.api_key = api_key
        client.embeddings.create(
            input="A test request to validate the API key",
            model="text-embedding-ada-002"
        )
        return True
    except openai.AuthenticationError as e:
        # If an AuthenticationError is raised, the API key is invalid
        print(f"AuthenticationError: {e}")
        return False
    except openai.OpenAIError as e:
        print(f"OpenAIError: {e}")
        return False


def save_conf(conf) -> None:
    """ Save the configuration to the file """
    conf_file_path: str = get_config_path()
    with open(conf_file_path, 'w', encoding='utf-8') as conf_file:
        toml.dump(conf, conf_file)


def append_conf(conf: dict[Any, Any]) -> None:
    """ Append the configuration to the file """
    conf_file_path: str = get_config_path()
    conf_item: dict[Any, Any] = load_conf()

    # Update the existing configuration with the new configuration
    conf_item.update(conf)

    # Write the updated configuration back to the file
    with open(conf_file_path, 'w', encoding='utf-8') as conf_file:
        toml.dump(conf_item, conf_file)


def load_conf() -> dict[Any, Any]:
    """ Load the configuration from the file """
    conf_file_path: str = get_config_path()
    try:
        with open(conf_file_path, 'r', encoding='utf-8') as conf_file:
            conf: dict[Any, Any] = toml.load(conf_file)
            return conf
    except FileNotFoundError as e:
        raise FileNotFoundError(
            'Configuration file not found, `init` the app first.') from e


def get_username() -> str:
    """ Get the username """
    return getpass.getuser()
