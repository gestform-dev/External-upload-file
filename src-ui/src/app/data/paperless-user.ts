import { PaperlessGroup } from 'src/app/data/paperless-group'
import { ObjectWithId } from './object-with-id'

export interface PaperlessUser extends ObjectWithId {
  username?: string;
  phone_number?: string;
  first_name?: string;
  last_name?: string;
  date_of_birth?: string;
  date_joined?: Date;
  is_staff?: boolean;
  is_active?: boolean;
  is_superuser?: boolean;
  groups?: number[]; // PaperlessGroup[]
  user_permissions?: string[];
  inherited_permissions?: string[];
}
