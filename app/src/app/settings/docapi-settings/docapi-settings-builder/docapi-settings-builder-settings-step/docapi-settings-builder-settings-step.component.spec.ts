import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderSettingsStepComponent } from './docapi-settings-builder-settings-step.component';

describe('DocapiSettingsBuilderSettingsStepComponent', () => {
  let component: DocapiSettingsBuilderSettingsStepComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderSettingsStepComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderSettingsStepComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderSettingsStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
