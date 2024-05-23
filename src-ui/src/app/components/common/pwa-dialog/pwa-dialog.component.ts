import { Component, Input } from '@angular/core'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'
import { SettingsService } from 'src/app/services/settings.service'

@Component({
  selector: 'app-pwa-dialog',
  templateUrl: './pwa-dialog.component.html',
  styleUrls: ['./pwa-dialog.component.scss']
})
export class PwaDialogComponent {
  constructor(
    public activeModal: NgbActiveModal,
    private settingsService: SettingsService
  ) {
  }

  @Input() title = $localize`Upload files`
  @Input() message = $localize`Do you want to install Upload files application ?`
  @Input() data!: { promptEvent?: any }

  public installPwa(): void {
    this.data.promptEvent.prompt()
    this.close()
  }

  public close() {
    this.settingsService.displayedInstallationModale()
    this.activeModal.close()
  }
}
