import { Injectable } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { take, timer } from 'rxjs';
import { PwaDialogComponent } from '../components/common/pwa-dialog/pwa-dialog.component';
import { IOS_PLATFORMS_LIST, MACOS_PLATFORMS_LIST, PLATFORM_ANDROID, PLATFORM_IOS, PLATFORM_LINUX, PLATFORM_MACOS, PLATFORM_WINDOWS, WINDOWS_PLATFORMS_LIST } from '../constants/platforms.const';

@Injectable({
  providedIn: 'root'
})
export class PwaService {
  private promptEvent: any;

  constructor(
    private modalService: NgbModal,
  ) { }

  getOS() {
    var userAgent = window.navigator.userAgent,
      platform = window.navigator.platform,
      macosPlatforms = MACOS_PLATFORMS_LIST,
      windowsPlatforms = WINDOWS_PLATFORMS_LIST,
      iosPlatforms = IOS_PLATFORMS_LIST,
      os = null;

    if (macosPlatforms.indexOf(platform) !== -1) {
      os = PLATFORM_MACOS;
    } else if (iosPlatforms.indexOf(platform) !== -1) {
      os = PLATFORM_IOS;
    } else if (windowsPlatforms.indexOf(platform) !== -1) {
      os = PLATFORM_WINDOWS;
    } else if (/Android/.test(userAgent)) {
      os = PLATFORM_ANDROID;
    } else if (!os && /Linux/.test(platform)) {
      os = PLATFORM_LINUX;
    }

    return os;
  }

  public initPwaPrompt(hasSeenModale: boolean) {
    const os = this.getOS();
    
    if (!hasSeenModale && os === PLATFORM_ANDROID) {
      window.addEventListener('beforeinstallprompt', (event: any) => {
        event.preventDefault();
        this.promptEvent = event;
        this.openPromptComponent();
      });
    }
  }

  private openPromptComponent() {
    timer(3000)
      .pipe(take(1))
      .subscribe(() => {
        const modal = this.modalService.open(PwaDialogComponent, { backdrop: 'static' })
        modal.componentInstance.data = { promptEvent: this.promptEvent }
      });
  }
}