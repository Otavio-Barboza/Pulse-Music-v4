# imports gerais
import lyricsgenius, os, dotenv


def ler_env():
    dotenv.load_dotenv(r'Assets\App\Env\.env')
    try:
        return os.getenv('CLIENT_ACCESS_TOKEN')
    except Exception as e:
        print(e)
        return None


class Genius(lyricsgenius.Genius):
    def __init__(
        self,
        access_token = ler_env(),
        response_format = "plain",
        timeout = 15,
        sleep_time = 0.2,
        remove_section_headers = True,
        skip_non_songs = True,
        excluded_terms = ["(Remix)", "(Live)"],
        replace_default_terms = False,
        retries = 0,
        user_agent = "",
        proxy = None,
        # per_page=5
    ):
        super().__init__(
            access_token = access_token,
            response_format = response_format,
            timeout = timeout,
            sleep_time = sleep_time,
            remove_section_headers = remove_section_headers,
            skip_non_songs = skip_non_songs,
            excluded_terms = excluded_terms,
            replace_default_terms = replace_default_terms,
            retries = retries,
            user_agent = user_agent,
            proxy = proxy,
            # per_page=per_page
        )