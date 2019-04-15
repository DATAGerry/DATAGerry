export class ConnectionResult {
  title: string;
  version: string;
  connected: boolean;

  constructor(title, version, connected) {
    this.title = title;
    this.version = version;
    this.connected = connected;
  }

  public get isConnected() {
    return this.connected;
  }
}
