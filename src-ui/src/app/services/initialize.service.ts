import { Injectable } from '@angular/core';
import { SettingsService } from './settings.service'
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { PaperlessUiSettings } from '../data/paperless-uisettings';
import { PwaService } from './pwa.service';

@Injectable({providedIn: 'root',})
export class InitializeService  {
    constructor(
        private settingsService: SettingsService,
        private router: Router
        ) {};

    initialize():Observable<PaperlessUiSettings>{
        if (navigator.onLine){
            return this.settingsService.initializeSettings();
        }
        else{
            this.router.navigate(['offline']);
        }
    }
}