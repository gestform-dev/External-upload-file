export interface WebsocketConsumerStatusMessage {
  user_id?: number
  filename?: string
  task_id?: string
  current_progress?: number
  max_progress?: number
  status?: string
  message?: string
  document_id: number
  config_info?:{ [key: string]: string }
}
