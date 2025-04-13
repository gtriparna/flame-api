from vault_rehydration_daemon import VaultDaemon

daemon = VaultDaemon(refresh=False, interval=10)
daemon.run()