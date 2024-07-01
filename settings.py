def load_settings(settings_path: str) -> dict:
    with open(settings_path) as f:
        settings_as_dict = {}
        for settings_line in f.read().splitlines():
            settings_line_as_list = settings_line.split("=", 1)
            if len(settings_line_as_list) == 2:
                settings_as_dict[settings_line_as_list[0].strip()] = settings_line_as_list[
                    1
                ].strip()
        return settings_as_dict


settings = load_settings("settings.dat")

TV_DB_API = settings["TV_DB_API"]
TOKEN = settings["TOKEN"]
JWT_EXPIRATION_DATETIME = settings["JWT_EXPIRATION_DATETIME"]