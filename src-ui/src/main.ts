import { enableProdMode } from '@angular/core'
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic'
import { AppModule } from './app/app.module'
import { environment } from './environments/environment'
import * as Sentry from "@sentry/angular-ivy";
import { captureConsoleIntegration, httpClientIntegration } from '@sentry/integrations'

if (environment.production) {
  console.log(environment.version);
  enableProdMode()
  Sentry.init({
    dsn: environment.SENTRY_PATH,
    environment: environment.name,
    release: environment.version,
    debug: true,
    integrations: [
      captureConsoleIntegration({levels :  ['warn', 'error']}),
      Sentry.browserTracingIntegration(),
      httpClientIntegration({failedRequestStatusCodes: [400, 599]})
    ],
  });
}

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .catch((err) => console.error(err))
