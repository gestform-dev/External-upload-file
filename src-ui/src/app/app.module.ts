import { BrowserModule } from '@angular/platform-browser'
import { APP_INITIALIZER, NgModule } from '@angular/core'
import { AppRoutingModule } from './app-routing.module'
import { AppComponent } from './app.component'
import {
  NgbDateAdapter,
  NgbDateParserFormatter,
  NgbModule,
} from '@ng-bootstrap/ng-bootstrap'
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http'
import { DocumentListComponent } from './components/document-list/document-list.component'
import { DocumentDetailComponent } from './components/document-detail/document-detail.component'
import { DashboardComponent } from './components/dashboard/dashboard.component'
import { TagListComponent } from './components/manage/tag-list/tag-list.component'
import { DocumentTypeListComponent } from './components/manage/document-type-list/document-type-list.component'
import { CorrespondentListComponent } from './components/manage/correspondent-list/correspondent-list.component'
import { LogsComponent } from './components/manage/logs/logs.component'
import { SettingsComponent } from './components/manage/settings/settings.component'
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { DatePipe, registerLocaleData } from '@angular/common'
import { NotFoundComponent } from './components/not-found/not-found.component'
import { ConfirmDialogComponent } from './components/common/confirm-dialog/confirm-dialog.component'
import { CorrespondentEditDialogComponent } from './components/common/edit-dialog/correspondent-edit-dialog/correspondent-edit-dialog.component'
import { TagEditDialogComponent } from './components/common/edit-dialog/tag-edit-dialog/tag-edit-dialog.component'
import { DocumentTypeEditDialogComponent } from './components/common/edit-dialog/document-type-edit-dialog/document-type-edit-dialog.component'
import { TagComponent } from './components/common/tag/tag.component'
import { ClearableBadgeComponent } from './components/common/clearable-badge/clearable-badge.component'
import { PageHeaderComponent } from './components/common/page-header/page-header.component'
import { AppFrameComponent } from './components/app-frame/app-frame.component'
import { ToastsComponent } from './components/common/toasts/toasts.component'
import { FilterEditorComponent } from './components/document-list/filter-editor/filter-editor.component'
import { FilterableDropdownComponent } from './components/common/filterable-dropdown/filterable-dropdown.component'
import { ToggleableDropdownButtonComponent } from './components/common/filterable-dropdown/toggleable-dropdown-button/toggleable-dropdown-button.component'
import { DateDropdownComponent } from './components/common/date-dropdown/date-dropdown.component'
import { DocumentCardLargeComponent } from './components/document-list/document-card-large/document-card-large.component'
import { DocumentCardSmallComponent } from './components/document-list/document-card-small/document-card-small.component'
import { BulkEditorComponent } from './components/document-list/bulk-editor/bulk-editor.component'
import { NgxFileDropModule } from 'ngx-file-drop'
import { TextComponent } from './components/common/input/text/text.component'
import { SelectComponent } from './components/common/input/select/select.component'
import { CheckComponent } from './components/common/input/check/check.component'
import { PasswordComponent } from './components/common/input/password/password.component'
import { SaveViewConfigDialogComponent } from './components/document-list/save-view-config-dialog/save-view-config-dialog.component'
import { TagsComponent } from './components/common/input/tags/tags.component'
import { IfPermissionsDirective } from './directives/if-permissions.directive'
import { SortableDirective } from './directives/sortable.directive'
import { CookieService } from 'ngx-cookie-service'
import { CsrfInterceptor } from './interceptors/csrf.interceptor'
import { SavedViewWidgetComponent } from './components/dashboard/widgets/saved-view-widget/saved-view-widget.component'
import { StatisticsWidgetComponent } from './components/dashboard/widgets/statistics-widget/statistics-widget.component'
import { UploadFileWidgetComponent } from './components/dashboard/widgets/upload-file-widget/upload-file-widget.component'
import { WidgetFrameComponent } from './components/dashboard/widgets/widget-frame/widget-frame.component'
import { PdfViewerModule } from 'ng2-pdf-viewer'
import { WelcomeWidgetComponent } from './components/dashboard/widgets/welcome-widget/welcome-widget.component'
import { YesNoPipe } from './pipes/yes-no.pipe'
import { FileSizePipe } from './pipes/file-size.pipe'
import { FilterPipe } from './pipes/filter.pipe'
import { DocumentTitlePipe } from './pipes/document-title.pipe'
import { MetadataCollapseComponent } from './components/document-detail/metadata-collapse/metadata-collapse.component'
import { SelectDialogComponent } from './components/common/select-dialog/select-dialog.component'
import { NgSelectModule } from '@ng-select/ng-select'
import { NumberComponent } from './components/common/input/number/number.component'
import { SafeUrlPipe } from './pipes/safeurl.pipe'
import { SafeHtmlPipe } from './pipes/safehtml.pipe'
import { CustomDatePipe } from './pipes/custom-date.pipe'
import { DateComponent } from './components/common/input/date/date.component'
import { ISODateAdapter } from './utils/ngb-iso-date-adapter'
import { LocalizedDateParserFormatter } from './utils/ngb-date-parser-formatter'
import { ApiVersionInterceptor } from './interceptors/api-version.interceptor'
import { ColorSliderModule } from 'ngx-color/slider'
import { ColorComponent } from './components/common/input/color/color.component'
import { DocumentAsnComponent } from './components/document-asn/document-asn.component'
import { DocumentNotesComponent } from './components/document-notes/document-notes.component'
import { PermissionsGuard } from './guards/permissions.guard'
import { DirtyDocGuard } from './guards/dirty-doc.guard'
import { DirtySavedViewGuard } from './guards/dirty-saved-view.guard'
import { StoragePathListComponent } from './components/manage/storage-path-list/storage-path-list.component'
import { StoragePathEditDialogComponent } from './components/common/edit-dialog/storage-path-edit-dialog/storage-path-edit-dialog.component'
import { TasksComponent } from './components/manage/tasks/tasks.component'
import { TourNgBootstrapModule } from 'ngx-ui-tour-ng-bootstrap'
import { UserEditDialogComponent } from './components/common/edit-dialog/user-edit-dialog/user-edit-dialog.component'
import { GroupEditDialogComponent } from './components/common/edit-dialog/group-edit-dialog/group-edit-dialog.component'
import { PermissionsSelectComponent } from './components/common/permissions-select/permissions-select.component'
import { MailAccountEditDialogComponent } from './components/common/edit-dialog/mail-account-edit-dialog/mail-account-edit-dialog.component'
import { MailRuleEditDialogComponent } from './components/common/edit-dialog/mail-rule-edit-dialog/mail-rule-edit-dialog.component'
import { PermissionsUserComponent } from './components/common/input/permissions/permissions-user/permissions-user.component'
import { PermissionsGroupComponent } from './components/common/input/permissions/permissions-group/permissions-group.component'
import { IfOwnerDirective } from './directives/if-owner.directive'
import { IfObjectPermissionsDirective } from './directives/if-object-permissions.directive'
import { PermissionsDialogComponent } from './components/common/permissions-dialog/permissions-dialog.component'
import { PermissionsFormComponent } from './components/common/input/permissions/permissions-form/permissions-form.component'
import { PermissionsFilterDropdownComponent } from './components/common/permissions-filter-dropdown/permissions-filter-dropdown.component'
import { UsernamePipe } from './pipes/username.pipe'
import { GestformLogoComponent } from './components/gestform-logos/gestform-logo/gestform-logo.component'
import { OfflineComponent } from './components/offline/offline.component';
import { InitializeService } from './services/initialize.service'

import localeEnGb from '@angular/common/locales/en-GB'
import localeFr from '@angular/common/locales/fr'
import { GestformLogoNotextComponent } from './components/gestform-logos/gestform-logo-notext/gestform-logo-notext.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { AccountSettingsComponent } from './components/manage/account-settings/account-settings.component';
import { FaqPageComponent } from './components/manage/faq/faq.component';
import { ChangePasswordComponent } from './components/manage/change-password/change-password.component';
import { environment } from "../environments/environment";
import { API_BASE_URL } from "../app/constants/variables"
import { IfOneOfPermissionsDirective } from './directives/if-one-of-permissions.directive'
import { PwaDialogComponent } from './components/common/pwa-dialog/pwa-dialog.component'
import { PrivacyAndTermsComponent } from './components/manage/privacy-and-terms/privacy-and-terms.component'
import { FaqConfigService } from './services/faq-config-service'
import * as Sentry from "@sentry/angular-ivy";
import { Router } from '@angular/router'

registerLocaleData(localeEnGb)
registerLocaleData(localeFr)

function initializeApp(initializeService: InitializeService) {
  return () => {
    return initializeService.initialize()
  }
}

@NgModule({
  declarations: [
    AppComponent,
    DocumentListComponent,
    DocumentDetailComponent,
    DashboardComponent,
    TagListComponent,
    DocumentTypeListComponent,
    CorrespondentListComponent,
    StoragePathListComponent,
    LogsComponent,
    SettingsComponent,
    NotFoundComponent,
    CorrespondentEditDialogComponent,
    ConfirmDialogComponent,
    TagEditDialogComponent,
    DocumentTypeEditDialogComponent,
    StoragePathEditDialogComponent,
    TagComponent,
    ClearableBadgeComponent,
    PageHeaderComponent,
    AppFrameComponent,
    ToastsComponent,
    FilterEditorComponent,
    FilterableDropdownComponent,
    ToggleableDropdownButtonComponent,
    DateDropdownComponent,
    DocumentCardLargeComponent,
    DocumentCardSmallComponent,
    BulkEditorComponent,
    TextComponent,
    SelectComponent,
    CheckComponent,
    PasswordComponent,
    SaveViewConfigDialogComponent,
    TagsComponent,
    IfPermissionsDirective,
    IfOneOfPermissionsDirective,
    SortableDirective,
    SavedViewWidgetComponent,
    StatisticsWidgetComponent,
    UploadFileWidgetComponent,
    WidgetFrameComponent,
    WelcomeWidgetComponent,
    YesNoPipe,
    FileSizePipe,
    FilterPipe,
    DocumentTitlePipe,
    MetadataCollapseComponent,
    SelectDialogComponent,
    NumberComponent,
    SafeUrlPipe,
    SafeHtmlPipe,
    CustomDatePipe,
    DateComponent,
    ColorComponent,
    DocumentAsnComponent,
    DocumentNotesComponent,
    TasksComponent,
    UserEditDialogComponent,
    GroupEditDialogComponent,
    PermissionsSelectComponent,
    MailAccountEditDialogComponent,
    MailRuleEditDialogComponent,
    PermissionsUserComponent,
    PermissionsGroupComponent,
    IfOwnerDirective,
    IfObjectPermissionsDirective,
    PermissionsDialogComponent,
    PermissionsFormComponent,
    PermissionsFilterDropdownComponent,
    UsernamePipe,
    GestformLogoComponent,
    GestformLogoNotextComponent,
    OfflineComponent,
    AccountSettingsComponent,
    FaqPageComponent,
    ChangePasswordComponent,
    PwaDialogComponent,
    PrivacyAndTermsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    NgxFileDropModule,
    PdfViewerModule,
    NgSelectModule,
    ColorSliderModule,
    TourNgBootstrapModule,
    ServiceWorkerModule.register('ngsw-worker.js', {
      registrationStrategy: 'registerWhenStable:30000'
    }),
  ],
  providers: [
    { provide: API_BASE_URL, useValue: environment.apiBaseUrl },
    {
      provide: APP_INITIALIZER,
      useFactory: initializeApp,
      deps: [InitializeService],
      multi: true,
    },
    DatePipe,
    FaqConfigService,
    CookieService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: CsrfInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ApiVersionInterceptor,
      multi: true,
    },
    FilterPipe,
    DocumentTitlePipe,
    { provide: NgbDateAdapter, useClass: ISODateAdapter },
    { provide: NgbDateParserFormatter, useClass: LocalizedDateParserFormatter },
    PermissionsGuard,
    DirtyDocGuard,
    DirtySavedViewGuard,
    UsernamePipe,
    {
      provide: Sentry.TraceService,
      deps: [Router],
    },
    {
      provide: APP_INITIALIZER,
      useFactory: () => () => {},
      deps: [Sentry.TraceService],
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {
}
