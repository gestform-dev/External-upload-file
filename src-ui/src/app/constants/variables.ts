import { InjectionToken } from '@angular/core';

export const API_BASE_URL = new InjectionToken<string>('apiBaseURL');
export const CONFIDENTIALITY_POLICY_FILE_PATH = 'assets/static/empty_confidentiality_policy.pdf'