import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FAQ_API_SUFFIX_URL } from 'src/app/constants/faq-default.config';
import { environment } from 'src/environments/environment';


@Injectable()
export class FaqConfigService {
    constructor(private http: HttpClient) { }
    faqConfig: any;
    faqApiURL: string = `${environment.apiBaseUrl}${FAQ_API_SUFFIX_URL}`;
    getFaqConfigData(): Observable<any> {
        return this.http.get<any>(this.faqApiURL);
    }
}