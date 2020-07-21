import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderStyleStepComponent } from './docapi-settings-builder-style-step.component';

describe('DocapiSettingsBuilderStyleStepComponent', () => {
  let component: DocapiSettingsBuilderStyleStepComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderStyleStepComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderStyleStepComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderStyleStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
