import { ComponentFixture, TestBed } from '@angular/core/testing'
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'
import { NgSelectModule } from '@ng-select/ng-select'
import { SelectComponent } from '../input/select/select.component'
import { PwaDialogComponent } from './pwa-dialog.component'

describe('PwaDialogComponent', () => {
  let component: PwaDialogComponent
  let fixture: ComponentFixture<PwaDialogComponent>
  let modal: NgbActiveModal

  beforeEach(async () => {
    TestBed.configureTestingModule({
      declarations: [PwaDialogComponent, SelectComponent],
      providers: [NgbActiveModal],
      imports: [NgSelectModule, FormsModule, ReactiveFormsModule],
    }).compileComponents()

    modal = TestBed.inject(NgbActiveModal)
    fixture = TestBed.createComponent(PwaDialogComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should close modal on cancel', () => {
    const closeSpy = jest.spyOn(modal, 'close')
    component.close()
    expect(closeSpy).toHaveBeenCalled()
  })
})
