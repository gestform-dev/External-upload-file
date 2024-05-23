import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-gestform-logo-notext',
  templateUrl: './gestform-logo-notext.component.html',
  styleUrls: ['./gestform-logo-notext.component.scss']
})
export class GestformLogoNotextComponent {
  @Input() width: number;
  @Input() height: number;
}
