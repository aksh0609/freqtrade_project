import json
import os
import glob


def template_config(file_path):
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Skipping {file_path}: {e}")
            return

    # Redact sensitive info
    if "exchange" in data:
        if "key" in data["exchange"]:
            data["exchange"]["key"] = "YOUR_BYBIT_KEY"
        if "secret" in data["exchange"]:
            data["exchange"]["secret"] = "YOUR_BYBIT_SECRET"

    if "api_server" in data:
        if "jwt_secret_key" in data["api_server"]:
            data["api_server"]["jwt_secret_key"] = "YOUR_JWT_SECRET"
        if "ws_token" in data["api_server"]:
            data["api_server"]["ws_token"] = "YOUR_WS_TOKEN"
        if "password" in data["api_server"]:
            data["api_server"]["password"] = "YOUR_BOT_PASSWORD"

    example_path = file_path + ".example"
    with open(example_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Created template: {example_path}")


# Run for all user configs
configs = glob.glob("user_data/config_*.json")
for cfg in configs:
    template_config(cfg)
