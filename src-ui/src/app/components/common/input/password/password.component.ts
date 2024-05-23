import { Component, forwardRef } from '@angular/core'
import { NG_VALUE_ACCESSOR } from '@angular/forms'
import { AbstractInputComponent } from '../abstract-input'

@Component({
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => PasswordComponent),
      multi: true,
    },
  ],
  selector: 'app-input-password',
  templateUrl: './password.component.html',
  styleUrls: ['./password.component.scss'],
})
export class PasswordComponent extends AbstractInputComponent<string> {
  constructor() {
    super()
  }
  showPassword: boolean = false;
  showEye: boolean = false;
  show_password() {
    this.showPassword = !this.showPassword;
  };
  evaluate_if_eye_shown(){
    let error_message = document.getElementById("error-message-feedback")
    return (this.showEye==true && error_message == null)
  }
}
