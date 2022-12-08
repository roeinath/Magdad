from TalpiBot.ExternalAPIs.Mail import MailClient


def main():
    client = MailClient()
    client.connect()
    client.send_mail("avichayrad.39.talpiot@gmail.com", "Test2 Subject", "Test2 Content")
    client.close()


if __name__ == '__main__':
    main()
