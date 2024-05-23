import { Component, OnInit } from '@angular/core'
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import {
  CHANGE_PASSWORD_REDIRECT_DELAY_3500_MS,
  API_URI_ACCOUNT_SETTINGS,
  API_URI_LOGOUT,
  CONFIRM_PASSWORD,
  NEW_PASSWORD,
  NOT_SAME_PASSWORD_ERROR,
  PASSWORD,
  PASSWORD_SAVED,
  TOAST_DELAY,
  TOAST_EMPTY_FIELD_CONTENT,
  TOAST_PASSWORD_EMPTY_FIELD_TITLE,
  TOAST_PASSWORD_UPDATE_FAILED,
} from 'src/app/constants/change-password.const'
import { AccountSettingsService } from 'src/app/services/rest/account-settings.service';
import { ToastService } from 'src/app/services/toast.service';



@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss']
})
export class ChangePasswordComponent implements OnInit {
  constructor(
    private fb: FormBuilder,
    private toastService: ToastService,
    private router: Router,
    private readonly accountSettingsService: AccountSettingsService,) {
  }

  passwordForm: FormGroup;

  error = null;
  ngOnInit(): void {
    this.passwordForm = this.fb.group({
      newPassword: ['', Validators.required],
      confirmPassword: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  cleanAllFields() {
    this.passwordForm.reset();
  }

  validate(): boolean{
    let isValid:boolean = true;
    if (!this.passwordForm.valid) {
      this.toastService.showError(TOAST_PASSWORD_EMPTY_FIELD_TITLE, TOAST_DELAY, TOAST_EMPTY_FIELD_CONTENT);
      isValid = false;
    }
    if(this.passwordForm.get(NEW_PASSWORD).value != this.passwordForm.get(CONFIRM_PASSWORD).value) {
      this.error = { newPassword: NOT_SAME_PASSWORD_ERROR, confirmPassword: NOT_SAME_PASSWORD_ERROR };
      this.cleanAllFields();
      isValid = false;
    }
    return isValid;
  };

  save() {
    if (this.validate()) {
      const passwords = {
        newPassword: this.passwordForm.get(NEW_PASSWORD).value,
        password: this.passwordForm.get(PASSWORD).value
      }
      this.accountSettingsService.patchChangePassword(passwords)
        .subscribe({
          next: () => {
            this.error = null;
            this.toastService.showInfo(PASSWORD_SAVED);
            setTimeout(() : void => {
              this.router.navigate([API_URI_LOGOUT]);
            }, CHANGE_PASSWORD_REDIRECT_DELAY_3500_MS)
          },
          error: (e) : void => {
            this.error = e.error;
            this.toastService.showError(TOAST_PASSWORD_UPDATE_FAILED, TOAST_DELAY);
          }
        });
    } else {
      this.cleanAllFields();
    }
  }

  cancel() {
    this.router.navigate([API_URI_ACCOUNT_SETTINGS]);
  }
}
