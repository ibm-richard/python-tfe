from tfe import TFEClient, TFEConfig


def main():
    client = TFEClient(TFEConfig.from_env())
    org = "tfe-xxxxx"
    for ws in client.workspaces.list(org):
        print("WS:", ws.name, ws.id)


if __name__ == "__main__":
    main()
