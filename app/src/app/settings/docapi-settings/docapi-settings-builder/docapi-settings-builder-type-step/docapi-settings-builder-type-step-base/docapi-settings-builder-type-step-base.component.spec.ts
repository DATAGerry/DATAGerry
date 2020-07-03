import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderTypeStepBaseComponent } from './docapi-settings-builder-type-step-base.component';

describe('DocapiSettingsBuilderTypeStepBaseComponent', () => {
  let component: DocapiSettingsBuilderTypeStepBaseComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderTypeStepBaseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderTypeStepBaseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderTypeStepBaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
