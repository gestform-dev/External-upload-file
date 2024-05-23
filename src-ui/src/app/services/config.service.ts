import { Injectable } from '@angular/core';
import { Observable } from 'rxjs'
import { HttpClient } from '@angular/common/http'
import { MAX_ALLOWED_SIZE_IN_MB_API_URI } from './constants/config-service.const'
import { environment } from '../../environments/environment'

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  constructor(private http: HttpClient) { }

  get_max_allowed_file_size_in_megabytes(): Observable<number>  {
    return this.http.get<number>(environment.apiBaseUrl + MAX_ALLOWED_SIZE_IN_MB_API_URI);
  }
}
