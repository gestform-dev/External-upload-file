import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestformLogoComponent } from './gestform-logo.component';

describe('GestformLogoComponent', () => {
  let component: GestformLogoComponent;
  let fixture: ComponentFixture<GestformLogoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GestformLogoComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestformLogoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
