import { jest } from '@jest/globals'
if (process.env.NODE_ENV === 'test') {
  require('jest-preset-angular/setup-jest')
}
import '@angular/localize/init'
import { TextEncoder, TextDecoder } from 'util'
global.TextEncoder = TextEncoder
global.TextDecoder = TextDecoder

import { registerLocaleData } from '@angular/common'
import localeEnGb from '@angular/common/locales/en-GB'
import localeFr from '@angular/common/locales/fr'

registerLocaleData(localeEnGb)
registerLocaleData(localeFr)

/* global mocks for jsdom */
const mock = () => {
  let storage: { [key: string]: string } = {}
  return {
    getItem: (key: string) => (key in storage ? storage[key] : null),
    setItem: (key: string, value: string) => (storage[key] = value || ''),
    removeItem: (key: string) => delete storage[key],
    clear: () => (storage = {}),
  }
}

Object.defineProperty(window, 'localStorage', { value: mock() })
Object.defineProperty(window, 'sessionStorage', { value: mock() })
Object.defineProperty(window, 'getComputedStyle', {
  value: () => ['-webkit-appearance'],
})

Object.defineProperty(window, 'ResizeObserver', { value: mock() })

Object.defineProperty(document.body.style, 'transform', {
  value: () => {
    return {
      enumerable: true,
      configurable: true,
    }
  },
})

HTMLCanvasElement.prototype.getContext = <
  typeof HTMLCanvasElement.prototype.getContext
>jest.fn()
