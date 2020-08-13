import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderTypeStepComponent } from './docapi-settings-builder-type-step.component';

describe('DocapiSettingsBuilderTypeStepComponent', () => {
  let component: DocapiSettingsBuilderTypeStepComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderTypeStepComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderTypeStepComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderTypeStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
