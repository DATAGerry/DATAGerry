import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderContentStepComponent } from './docapi-settings-builder-content-step.component';

describe('DocapiSettingsBuilderContentStepComponent', () => {
  let component: DocapiSettingsBuilderContentStepComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderContentStepComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderContentStepComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderContentStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
