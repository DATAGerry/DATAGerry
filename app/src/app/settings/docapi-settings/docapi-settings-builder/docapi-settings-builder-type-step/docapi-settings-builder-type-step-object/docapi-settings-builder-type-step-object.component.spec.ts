import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderTypeStepObjectComponent } from './docapi-settings-builder-type-step-object.component';

describe('DocapiSettingsBuilderTypeStepObjectComponent', () => {
  let component: DocapiSettingsBuilderTypeStepObjectComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderTypeStepObjectComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderTypeStepObjectComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderTypeStepObjectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
