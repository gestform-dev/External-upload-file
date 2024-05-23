import {Component, OnInit} from '@angular/core'
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CHANGE_SAVED, ERROR_EMPTY_EMAIL, RELOAD_PAGE, ROUTE_DASHBOARD } from 'src/app/constants/account-settings.const';
import { AccountSettingsService } from 'src/app/services/rest/account-settings.service';
import { UserService } from 'src/app/services/rest/user.service';
import { SettingsService } from 'src/app/services/settings.service';
import { ToastService } from 'src/app/services/toast.service';
import { catchError, filter, first, map, Observable, of, switchMap, tap } from 'rxjs'
import { PaperlessUiSettings } from '../../../data/paperless-uisettings'
import { EX_NUMBER_PHONE } from 'src/app/constants/placeholder.const';

@Component({
  selector: 'app-account-settings',
  templateUrl: './account-settings.component.html',
  styleUrls: ['./account-settings.component.scss'],
})

export class AccountSettingsComponent implements OnInit {
  placeholderNumberOfThePhone: string = EX_NUMBER_PHONE;
  error = null;
  userForm: FormGroup = this.fb.group({
    username: [this.settingsService.currentUser.username || '', Validators.required],
    phone_number: [this.settingsService.currentUser.phone_number || ''],
    first_name: [{ value: this.settingsService.currentUser.first_name || '', disabled: true }],
    last_name: [{ value: this.settingsService.currentUser.last_name || '', disabled: true }],
    date_of_birth: [{ value: this.settingsService.currentUser.date_of_birth || '', disabled: true }]
  });

  constructor(
    private fb: FormBuilder,
    private toastService: ToastService,
    protected service: UserService,
    private readonly settingsService: SettingsService,
    private readonly accountSettingsService: AccountSettingsService,
    private router: Router,
  ) {
  }

  reloadForm(): Observable<PaperlessUiSettings> {
   return this.settingsService.initializeSettings()
      .pipe(
        first(),
        tap(paperlessUiSettings => {
          this.userForm.patchValue(paperlessUiSettings.user);
        })
      );
  }
  ngOnInit(): void  {
    this.reloadForm().subscribe();
  }

  save() {
    if (!this.userForm.valid) {
       this.error = { username: ERROR_EMPTY_EMAIL }
      return;
    }
    let data_to_update = {
      username: this.userForm.controls.username.getRawValue(),
      phone_number : this.userForm.controls.phone_number.getRawValue()
    }

    this.error = null;
    this.accountSettingsService.patchEditProfile(data_to_update)
      .pipe(
        map(() => true),
        catchError((e) => {
          this.error = e.error;
          return of(false);
        }),
        filter(success => !!success),
        switchMap(() => this.reloadForm()),
        tap(() => {
          this.toastService.showInfo(CHANGE_SAVED)
          this.error = null
        })
      )
      .subscribe();
  }

  cancel() {
    this.toastService.showInfo(RELOAD_PAGE);
    this.error = null;
    this.userForm.controls.username.setValue(this.settingsService.currentUser.username)
    this.router.navigate([ROUTE_DASHBOARD])
  }
}
