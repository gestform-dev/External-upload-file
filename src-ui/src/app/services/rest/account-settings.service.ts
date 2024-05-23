import { HttpClient } from "@angular/common/http";
import { Inject, Injectable } from "@angular/core";
import { API_URI_EDIT_PROFILE } from "src/app/constants/account-settings.const";
import { API_URI_EDIT_PASSWORD } from "src/app/constants/change-password.const";
import { API_BASE_URL } from "src/app/constants/variables";
import { PaperlessUser } from "src/app/data/paperless-user";



@Injectable({
    providedIn: 'root',
})
export class AccountSettingsService{
  constructor(
    @Inject(API_BASE_URL) private readonly apiBaseUrl : string,
    private readonly http: HttpClient){
    }

    apiEditProfileUrl = this.apiBaseUrl + API_URI_EDIT_PROFILE;
    apiChangePasswordUrl = this.apiBaseUrl + API_URI_EDIT_PASSWORD ;

    patchEditProfile(new_user: PaperlessUser){
      return this.http.patch(this.apiEditProfileUrl, new_user);
    }

    patchChangePassword(passwords){
      return this.http.patch(this.apiChangePasswordUrl, passwords);
    }
}