import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { InitializeService } from '../../services/initialize.service';

@Component({
  selector: 'app-offline',
  templateUrl: './offline.component.html',
  styleUrls: ['./offline.component.scss'],
})
export class OfflineComponent {
  constructor(
    private router: Router,
    private initializeService: InitializeService
  ) {}

  retry(){
    const paperlessUiSettings = this.initializeService.initialize();

    if(paperlessUiSettings !== undefined) {
      this.router.navigate(['dashboard']);
    }

  }
}
