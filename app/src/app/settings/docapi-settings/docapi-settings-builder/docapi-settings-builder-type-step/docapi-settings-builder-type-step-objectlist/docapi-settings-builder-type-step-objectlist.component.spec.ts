import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocapiSettingsBuilderTypeStepObjectlistComponent } from './docapi-settings-builder-type-step-objectlist.component';

describe('DocapiSettingsBuilderTypeStepObjectlistComponent', () => {
  let component: DocapiSettingsBuilderTypeStepObjectlistComponent;
  let fixture: ComponentFixture<DocapiSettingsBuilderTypeStepObjectlistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocapiSettingsBuilderTypeStepObjectlistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocapiSettingsBuilderTypeStepObjectlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
