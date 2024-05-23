import {
  Input,
  OnInit,
  Directive,
  ViewContainerRef,
  TemplateRef,
} from '@angular/core'
import {
  PermissionAction,
  PermissionsService,
  PermissionType,
} from '../services/permissions.service'

@Directive({
  selector: '[appIfOneOfPermissions]',
})
export class IfOneOfPermissionsDirective implements OnInit {
  @Input()
  appIfOneOfPermissions:
    | Array<{ action: PermissionAction; type: PermissionType }>
    | { action: PermissionAction; type: PermissionType }

  /**
   * @param {ViewContainerRef} viewContainerRef -- The location where we need to render the templateRef
   * @param {TemplateRef<any>} templateRef -- The templateRef to be potentially rendered
   * @param {PermissionsService} permissionsService -- Will give us access to the permissions a user has
   */
  constructor(
    private viewContainerRef: ViewContainerRef,
    private templateRef: TemplateRef<any>,
    private permissionsService: PermissionsService
  ) { }

  public ngOnInit(): void {
    let isAllowed = false
    if (this.appIfOneOfPermissions) {
      [].concat(this.appIfOneOfPermissions).forEach(perm => {
        isAllowed = isAllowed ? isAllowed : this.permissionsService.currentUserCan(perm.action, perm.type)
      })
      if (isAllowed) {
        this.viewContainerRef.createEmbeddedView(this.templateRef)
      } else {
        this.viewContainerRef.clear()
      }
    } else {
      this.viewContainerRef.clear()
    }
  }
}
