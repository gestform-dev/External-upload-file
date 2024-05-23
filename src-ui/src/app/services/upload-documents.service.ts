import { Injectable } from '@angular/core'
import { HttpEventType } from '@angular/common/http'
import { FileSystemFileEntry, NgxFileDropEntry } from 'ngx-file-drop'
import {
  ConsumerStatusService,
  FileStatusPhase,
} from './consumer-status.service'
import { DocumentService } from './rest/document.service'
import { Subscription } from 'rxjs'
import { ConfigService } from './config.service'

@Injectable({
  providedIn: 'root',
})
export class UploadDocumentsService {
  private uploadSubscriptions: Array<Subscription> = []

  constructor(
    private documentService: DocumentService,
    private consumerStatusService: ConsumerStatusService,
    private configService: ConfigService
  ) {}

  uploadFiles(files: NgxFileDropEntry[]) {
    for (const droppedFile of files) {
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry
        fileEntry.file((file: File) => {
          let formData = new FormData()
          formData.append('document', file, file.name)
          let status = this.consumerStatusService.newFileUpload(file.name)

          status.message = $localize`Connecting...`

          this.uploadSubscriptions[file.name] = this.documentService
            .uploadDocument(formData)
            .subscribe({
              next: (event) => {
                if (event.type == HttpEventType.UploadProgress) {
                  status.updateProgress(
                    FileStatusPhase.UPLOADING,
                    event.loaded,
                    event.total
                  )
                  status.message = $localize`Uploading...`
                } else if (event.type == HttpEventType.Response) {
                  status.taskId = event.body['task_id']
                  status.message = $localize`Upload complete, waiting...`
                  this.uploadSubscriptions[file.name]?.complete()
                }
              },
              error: (error) => {
                switch (error.status) {
                  case 400: {
                    this.consumerStatusService.fail(
                      status,
                      error.error.document
                    )
                    break
                  }
                  case 403: {
                    this.consumerStatusService.fail(
                      status,
                      $localize`Cannot consume: File's name too long`
                    )
                    break
                  }
                  case 413: {
                    this.configService.get_max_allowed_file_size_in_megabytes().subscribe(max_size => {
                      this.consumerStatusService.fail(
                        status,
                        $localize`Cannot consume "${file.name}": file size is too large; maximum allowed size: ${max_size}MB`
                      );
                    });
                    break
                  }
                  case 500: {
                    this.consumerStatusService.fail(
                      status,
                      $localize`unexpected error occurred`
                    )
                    break
                  }
                  case 504: {
                    this.consumerStatusService.fail(
                      status,
                      $localize`delay too long, please try again`
                    )
                    break
                  }
                  default: {
                    this.consumerStatusService.fail(
                      status,
                      $localize`HTTP error: ${error.status} ${error.statusText}`
                    )
                    break
                  }
                }
                this.uploadSubscriptions[file.name]?.complete()
              },
            })
        })
      }
    }
  }
}
