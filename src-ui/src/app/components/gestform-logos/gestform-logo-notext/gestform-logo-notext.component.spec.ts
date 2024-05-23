import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestformLogoNotextComponent } from './gestform-logo-notext.component';

describe('GestformLogoNotextComponent', () => {
  let component: GestformLogoNotextComponent;
  let fixture: ComponentFixture<GestformLogoNotextComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GestformLogoNotextComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestformLogoNotextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
