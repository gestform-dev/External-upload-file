import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { FaqConfigService } from 'src/app/services/faq-config-service';
import { DEFAULT_FAQ_CONFIG } from 'src/app/constants/faq-default.config'
import { FaqConfigData } from 'src/app/data/faqConfigData';

@Component({
  selector: 'app-account-settings',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.scss'],
})
export class FaqPageComponent implements OnInit {
  constructor(
    public faqConfigService: FaqConfigService,
    private sanitizer: DomSanitizer
  ) { }
  apiData: FaqConfigData[];
  faqConfig: FaqConfigData[] = DEFAULT_FAQ_CONFIG
  async ngOnInit() {
    await this.faqConfigService.getFaqConfigData().subscribe(
      data => {
        try {
          this.apiData = data;
          console.log(this.apiData["faq"])
          if (this.apiData["faq"].length > 0) {
            this.faqConfig = [...this.faqConfig, ...this.apiData["faq"]];
          } else {
            this.faqConfig = [...this.faqConfig]
          }
          for (let faq of this.apiData) {
            faq.isVisible = false;
          }
        } catch (e) {
        }
      }
    );
  }
  toggleVisibility(index) {
    this.faqConfig.forEach((faq, i) => {
      if (index === i) {
        faq.isVisible = !faq.isVisible;
      } else {
        faq.isVisible = false;
      }
    });
  }
  transformToSafeHtml(stringToCkeck: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(stringToCkeck);
  }
}
