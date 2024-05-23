import { Injectable } from '@angular/core';

@Injectable({
    providedIn:'root',
})
export class RedirectionGuard {
  canActivate(): boolean {
    window.location.href = `accounts/logout/`;
    return false;
  }
}
