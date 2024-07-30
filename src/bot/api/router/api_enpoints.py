class APIEndpoints:
    class WebHook:
        Prefix = "/bot_webhook"
        Get: str = "/"

    class WebApp:
        Prefix = "/auth"
        Me = "/me/"

    class Home:
        Prefix = "/home"
        Get: str = "/"
