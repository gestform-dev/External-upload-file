const base_url = new URL(document.baseURI)

export const environment = {
  production: true,
  name: document.baseURI.includes('staging') ? 'staging' : 'production',
  apiBaseUrl: document.baseURI + 'api/',
  apiVersion: '3',
  appTitle: 'Paperless',
  version: require('../../../package.json')['version'],
  webSocketHost: window.location.host,
  webSocketProtocol: window.location.protocol == 'https:' ? 'wss:' : 'ws:',
  webSocketBaseUrl: base_url.pathname + 'ws/',
  SENTRY_PATH: 'https://sentry-path.com/'
}
