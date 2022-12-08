from APIs import settings
from APIs.TalpiotSystem import Vault


def main():
    settings.load_settings()
    Vault.get_vault().connect_all_dbs()


if __name__ == "__main__":
    main()
