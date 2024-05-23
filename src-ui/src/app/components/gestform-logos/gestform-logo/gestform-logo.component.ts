import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-gestform-logo',
  templateUrl: './gestform-logo.component.html',
  styleUrls: ['./gestform-logo.component.scss']
})
export class GestformLogoComponent {
  @Input() width: number;
  @Input() height: number;
  }
