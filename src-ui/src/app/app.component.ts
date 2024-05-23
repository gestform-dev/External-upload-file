import { Component, OnDestroy, OnInit, Renderer2 } from '@angular/core'
import { Router } from '@angular/router'
import { NgxFileDropEntry } from 'ngx-file-drop'
import { TourService } from 'ngx-ui-tour-ng-bootstrap'
import { Subject, first, takeUntil } from 'rxjs'
import {
  ACTION_OPEN_DOCUMENT,
  DEFAULT_TIMER_TOASTER_DELAY,
  INITIATING_UPLOAD,
  NEW_DOCUMENT_DETECTED,
  ROUTE_DOCUMENT,
  TITLE_DOCUMENT_ADDED
} from './constants/toaster.const'
import {
  CONTENT_DOCUMENTS_VIEWS,
  CONTENT_FILTER_EDITOR,
  ENDBTNTITLE, NEXTBTNTITLE, PREVBTNTITLE,
  TOUR_ANCHOR_ID_DASHBOARD,
  TOUR_ANCHOR_ID_DOCUMENTS,
  TOUR_ANCHOR_ID_DOCUMENTS_VIEWS,
  TOUR_ANCHOR_ID_FILTER_EDITOR,
  TOUR_ANCHOR_ID_OUTRO,
  TOUR_ANCHOR_ID_SETTINGS,
  TOUR_ANCHOR_ID_TAGS,
  TOUR_ANCHOR_ID_TASKS,
  TOUR_ANCHOR_ID_UPLOAD_WIDGET,
  TOUR_BOTTOM_PLACEMENT,
  TOUR_CONTENT_DASHBOARD, TOUR_CONTENT_DOCUMENTS,
  TOUR_CONTENT_OUTRO,
  TOUR_CONTENT_SETTINGS,
  TOUR_CONTENT_TAGS,
  TOUR_CONTENT_TASKS,
  TOUR_CONTENT_UPLOAD_WIDGET,
  TOUR_ROUTE_DASHBOARD,
  TOUR_ROUTE_DOCUMENTS,
  TOUR_ROUTE_SETTINGS,
  TOUR_ROUTE_TAGS,
  TOUR_ROUTE_TASKS,
  TOUR_TITLE_OUTRO
} from './constants/tourService.const'
import { SETTINGS_KEYS } from './data/paperless-uisettings'
import { ConsumerStatusService } from './services/consumer-status.service'
import {
  PermissionAction,
  PermissionType,
  PermissionsService
} from './services/permissions.service'
import { SettingsService } from './services/settings.service'
import { TasksService } from './services/tasks.service'
import { ToastService } from './services/toast.service'
import { UploadDocumentsService } from './services/upload-documents.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  private _unsubscribe$ = new Subject()

  private fileLeaveTimeoutID: any
  fileIsOver: boolean = false
  hidden: boolean = true

  constructor(
    private settings: SettingsService,
    private consumerStatusService: ConsumerStatusService,
    private toastService: ToastService,
    private router: Router,
    private uploadDocumentsService: UploadDocumentsService,
    private tasksService: TasksService,
    public tourService: TourService,
    private renderer: Renderer2,
    private permissionsService: PermissionsService
  ) {
    let anyWindow = window as any
    anyWindow.pdfWorkerSrc = 'assets/js/pdf.worker.min.js'
    this.settings.updateAppearanceSettings()
  }

  ngOnDestroy(): void {
    this.consumerStatusService.disconnect()
    this._unsubscribe$.next(null)
    this._unsubscribe$.unsubscribe()
  }

  private showNotification(key) {
    if (
      this.router.url == TOUR_ROUTE_DASHBOARD &&
      this.settings.get(
        SETTINGS_KEYS.NOTIFICATIONS_CONSUMER_SUPPRESS_ON_DASHBOARD
      )
    ) {
      return false
    }
    return this.settings.get(key)
  }

  ngOnInit(): void {
    this.consumerStatusService.connect()

    this.consumerStatusService
      .onDocumentConsumptionFinished()
      .pipe(takeUntil(this._unsubscribe$))
      .subscribe((status) => {
        this.tasksService.reload()
        if (
          this.showNotification(SETTINGS_KEYS.NOTIFICATIONS_CONSUMER_SUCCESS)
        ) {
          if (
            this.permissionsService.currentUserCan(
              PermissionAction.View,
              PermissionType.Document
            )
          ) {
            this.toastService.show({
              title: TITLE_DOCUMENT_ADDED,
              delay: DEFAULT_TIMER_TOASTER_DELAY,
              content: $localize`Document ${status.filename} was added.`,
              actionName: ACTION_OPEN_DOCUMENT,
              action: () => {
                this.router.navigate([ROUTE_DOCUMENT, status.documentId])
              }
            })
          } else {
            this.toastService.show({
              title: TITLE_DOCUMENT_ADDED,
              delay: DEFAULT_TIMER_TOASTER_DELAY,
              content: $localize`Document ${status.filename} was added.`
            })
          }
        }
      })

    this.consumerStatusService
      .onDocumentConsumptionFailed()
      .pipe(takeUntil(this._unsubscribe$))
      .subscribe((status) => {
        this.tasksService.reload()
        if (
          this.showNotification(SETTINGS_KEYS.NOTIFICATIONS_CONSUMER_FAILED)
        ) {
          this.toastService.showError(
            $localize`Could not add ${status.filename}` + $localize`\: ${status.message}`
          )
        }
      })

    this.consumerStatusService
      .onDocumentDetected()
      .pipe(takeUntil(this._unsubscribe$))
      .subscribe((status) => {
        this.tasksService.reload()
        if (
          this.showNotification(
            SETTINGS_KEYS.NOTIFICATIONS_CONSUMER_NEW_DOCUMENT
          )
        ) {
          this.toastService.show({
            title: NEW_DOCUMENT_DETECTED,
            delay: 5000,
            content: $localize`Document ${status.filename} is being processed.`
          })
        }
      })

    const prevBtnTitle = PREVBTNTITLE
    const nextBtnTitle = NEXTBTNTITLE
    const endBtnTitle = ENDBTNTITLE

    this.tourService.initialize([
      {
        anchorId: TOUR_ANCHOR_ID_DASHBOARD,
        content: TOUR_CONTENT_DASHBOARD,
        route: TOUR_ROUTE_DASHBOARD,
        enableBackdrop: true,
        delayAfterNavigation: 500,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_UPLOAD_WIDGET,
        content: TOUR_CONTENT_UPLOAD_WIDGET,
        route: TOUR_ROUTE_DASHBOARD,
        enableBackdrop: true,
        isOptional: true,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_DOCUMENTS,
        content: TOUR_CONTENT_DOCUMENTS,
        route: TOUR_ROUTE_DOCUMENTS,
        delayAfterNavigation: 500,
        placement: TOUR_BOTTOM_PLACEMENT,
        enableBackdrop: true,
        disableScrollToAnchor: true,
        isOptional: true,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_FILTER_EDITOR,
        content: CONTENT_FILTER_EDITOR,
        route: TOUR_ROUTE_DOCUMENTS,
        placement: TOUR_BOTTOM_PLACEMENT,
        enableBackdrop: true,
        isOptional: true,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_DOCUMENTS_VIEWS,
        content: CONTENT_DOCUMENTS_VIEWS,
        route: TOUR_ROUTE_DOCUMENTS,
        enableBackdrop: true,
        isOptional: true,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_TAGS,
        content: TOUR_CONTENT_TAGS,
        route: TOUR_ROUTE_TAGS,
        enableBackdrop: true,
        isOptional: true,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_TASKS,
        content: TOUR_CONTENT_TASKS,
        route: TOUR_ROUTE_TASKS,
        enableBackdrop: true,
        isOptional: true,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_SETTINGS,
        content: TOUR_CONTENT_SETTINGS,
        route: TOUR_ROUTE_SETTINGS,
        enableBackdrop: true,
        isOptional: true,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      },
      {
        anchorId: TOUR_ANCHOR_ID_OUTRO,
        title: TOUR_TITLE_OUTRO,
        content: TOUR_CONTENT_OUTRO,
        route: TOUR_ROUTE_DASHBOARD,
        prevBtnTitle,
        nextBtnTitle,
        endBtnTitle
      }
    ])

    this.tourService.start$
      .pipe(takeUntil(this._unsubscribe$))
      .subscribe(() => {
        this.renderer.addClass(document.body, 'tour-active')

        this.tourService.end$.pipe(first()).subscribe(() => {
          this.settings.completeTour()
          // animation time
          setTimeout(() => {
            this.renderer.removeClass(document.body, 'tour-active')
          }, 500)
        })
      })
  }

  public get dragDropEnabled(): boolean {
    return (
      !this.router.url.includes('dashboard') &&
      this.permissionsService.currentUserCan(
        PermissionAction.Add,
        PermissionType.Document
      )
    )
  }

  public fileOver() {
    // allows transition
    setTimeout(() => {
      this.fileIsOver = true
    }, 1)
    this.hidden = false
    // stop fileLeave timeout
    clearTimeout(this.fileLeaveTimeoutID)
  }

  public fileLeave(immediate: boolean = false) {
    const ms = immediate ? 0 : 500

    this.fileLeaveTimeoutID = setTimeout(() => {
      this.fileIsOver = false
      // await transition completed
      setTimeout(() => {
        this.hidden = true
      }, 150)
    }, ms)
  }

  public dropped(files: NgxFileDropEntry[]) {
    this.fileLeave(true)
    this.uploadDocumentsService.uploadFiles(files)
    this.toastService.showInfo(INITIATING_UPLOAD, 3000)
  }
}
